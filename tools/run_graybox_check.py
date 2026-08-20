from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

UV_VERSION = "0.12.5"


class GrayboxReceipt(TypedDict):
    receipt_version: int
    base_git_sha: str
    artifact_sha256: str
    remote_artifact_sha256: str
    artifact_digest_verified: bool
    container_image_id: str
    container_network: str
    workspace_mount: str
    execution_command: str
    preparation_returncode: int
    preparation_output: str
    execution_returncode: int
    execution_output: str
    rerun_returncode: int
    rerun_output: str
    rerun_consistent: bool


def _run(
    command: list[str],
    *,
    input_data: bytes | None = None,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command, input=input_data, capture_output=True, check=False, env=environment
    )


def _required_output(command: list[str], *, environment: dict[str, str] | None = None) -> bytes:
    result = _run(command, environment=environment)
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"command failed ({' '.join(command)}): {detail}")
    return result.stdout


def _remote(
    host: str, command: str, *, input_data: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    return _run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", host, command],
        input_data=input_data,
    )


def _remote_required(host: str, command: str, *, input_data: bytes | None = None) -> bytes:
    result = _remote(host, command, input_data=input_data)
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"remote command failed: {detail}")
    return result.stdout


def _remote_digest(host: str, archive: bytes, workspace: str) -> str:
    archive_path = f"{workspace}/artifact.tar"
    _remote_required(host, f"cat > {_shell(archive_path)}", input_data=archive)
    digest = _remote_required(host, f"sha256sum {_shell(archive_path)}").decode().split()[0]
    _remote_required(host, f"tar -xf {_shell(archive_path)} -C {_shell(workspace)}")
    _remote_required(host, f"rm -f {_shell(archive_path)}")
    return digest


def _decode_output(result: subprocess.CompletedProcess[bytes]) -> str:
    return (result.stdout + result.stderr).decode("utf-8", errors="replace").strip()


def _shell(command: str) -> str:
    return shlex.quote(command)


def _artifact_metadata(repo_root: Path) -> tuple[str, bytes, str]:
    git = ["git", "-c", f"safe.directory={repo_root}", "-C", str(repo_root)]
    base_sha = _required_output([*git, "rev-parse", "HEAD"]).decode().strip()
    files = _required_output(
        [
            *git,
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            ":(exclude)docs/traceability/G6_G7_GRAYBOX_RECEIPT.md",
        ]
    )
    archive_result = _run(["tar", "-cf", "-", "--null", "--files-from=-"], input_data=files)
    if archive_result.returncode:
        detail = archive_result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"artifact archive failed: {detail}")
    archive = archive_result.stdout
    return base_sha, archive, hashlib.sha256(archive).hexdigest()


def _receipt(
    *,
    base_sha: str,
    artifact_sha256: str,
    remote_artifact_sha256: str,
    container_image_id: str,
    preparation_output: str,
    execution_output: str,
    execution_returncode: int,
    rerun_output: str,
    rerun_returncode: int,
) -> GrayboxReceipt:
    return {
        "receipt_version": 1,
        "base_git_sha": base_sha,
        "artifact_sha256": artifact_sha256,
        "remote_artifact_sha256": remote_artifact_sha256,
        "artifact_digest_verified": artifact_sha256 == remote_artifact_sha256,
        "container_image_id": container_image_id,
        "container_network": "none",
        "workspace_mount": "read-only",
        "execution_command": "make UV=/workspace/.venv/bin/uv check",
        "preparation_returncode": 0,
        "preparation_output": preparation_output,
        "execution_returncode": execution_returncode,
        "execution_output": execution_output,
        "rerun_returncode": rerun_returncode,
        "rerun_output": rerun_output,
        "rerun_consistent": execution_returncode == rerun_returncode == 0,
    }


def run(
    repo_root: Path,
    host: str,
    image: str,
) -> GrayboxReceipt:
    base_sha, archive, artifact_sha256 = _artifact_metadata(repo_root)

    _remote_required(host, "~/bin/gb-guard check ~/scratch")
    remote_root = _remote_required(host, "~/bin/gb-guard place scratch").decode().strip()
    remote_workspace = (
        _remote_required(
            host, f"mktemp -d {_shell(remote_root.rstrip('/') + '/cortex-ascend-graybox-XXXXXX')}"
        )
        .decode()
        .strip()
    )
    _remote_required(host, f"~/bin/gb-guard check {_shell(remote_workspace)}")

    remote_artifact_sha256 = _remote_digest(host, archive, remote_workspace)
    if remote_artifact_sha256 != artifact_sha256:
        raise RuntimeError(
            f"artifact digest mismatch: local={artifact_sha256} remote={remote_artifact_sha256}"
        )
    _remote_required(
        host,
        " && ".join(
            (
                f"git -C {_shell(remote_workspace)} init -q",
                f"git -C {_shell(remote_workspace)} config user.email graybox@localhost",
                f"git -C {_shell(remote_workspace)} config user.name graybox",
                f"git -C {_shell(remote_workspace)} add --all",
                f"git -C {_shell(remote_workspace)} commit -qm base-artifact",
            )
        ),
    )

    image_id = (
        _remote_required(host, f"podman image inspect --format '{{{{.Id}}}}' {_shell(image)}")
        .decode()
        .strip()
    )
    preparation = _remote(host, _prepare_command(remote_workspace, image))
    if preparation.returncode:
        raise RuntimeError(f"dependency preparation failed: {_decode_output(preparation)}")

    execution = _remote(host, _execution_command(remote_workspace, image))
    rerun = _remote(host, _execution_command(remote_workspace, image))
    return _receipt(
        base_sha=base_sha,
        artifact_sha256=artifact_sha256,
        remote_artifact_sha256=remote_artifact_sha256,
        container_image_id=image_id,
        preparation_output=_decode_output(preparation),
        execution_output=_decode_output(execution),
        execution_returncode=execution.returncode,
        rerun_output=_decode_output(rerun),
        rerun_returncode=rerun.returncode,
    )


def _prepare_command(workspace: str, image: str) -> str:
    bootstrap = (
        "python -m venv .venv && "
        f".venv/bin/python -m pip install --disable-pip-version-check uv=={UV_VERSION} && "
        ".venv/bin/uv sync --frozen"
    )
    return f"podman run --rm --network bridge -v {_shell(workspace)}:/workspace:Z -w /workspace {_shell(image)} sh -ec {_shell(bootstrap)}"


def _execution_command(workspace: str, image: str) -> str:
    check = "make UV=/workspace/.venv/bin/uv check"
    return (
        f"podman run --rm --network none --tmpfs /tmp:rw,size=512m "
        f"-e HOME=/tmp -e UV_OFFLINE=1 -e UV_NO_SYNC=1 -e RUFF_CACHE_DIR=/tmp/ruff-cache "
        f"-e MYPY_CACHE_DIR=/tmp/mypy-cache "
        f"-e PYTHONDONTWRITEBYTECODE=1 "
        f"-v {_shell(workspace)}:/workspace:ro,Z -w /workspace {_shell(image)} "
        f"sh -ec {_shell(check)}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run make check against an exact artifact in a network-isolated gravebuster container."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--host", default="gravebuster")
    parser.add_argument("--image", default="python:3.12")
    args = parser.parse_args(argv)

    try:
        receipt = run(args.repo_root.resolve(), args.host, args.image)
    except RuntimeError as exc:
        print(f"graybox check failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt["execution_returncode"]


if __name__ == "__main__":
    raise SystemExit(main())
