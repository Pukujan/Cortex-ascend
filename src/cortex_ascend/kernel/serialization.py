from __future__ import annotations

import dataclasses
import hashlib
import json
from enum import Enum
from typing import Any


class CanonicalEncoder(json.JSONEncoder):
    """Encode dataclasses, enums, and tuples for canonical hashing."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, tuple):
            return list(obj)
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return _dataclass_dict(obj)
        return super().default(obj)


def _dataclass_dict(value: Any) -> dict[str, Any]:
    """Convert a dataclass to a dict excluding compare=False fields."""
    fields = dataclasses.fields(value)
    return {field.name: getattr(value, field.name) for field in fields if field.compare}


def canonical_json(value: Any) -> str:
    """Return a canonical JSON representation suitable for hashing.

    Keys are sorted, tuples are lists, whitespace is deterministic, and the
    output is ASCII-safe. Dataclass fields marked `compare=False` are omitted.
    """
    base = value
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        base = _dataclass_dict(value)
    return json.dumps(
        base,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        cls=CanonicalEncoder,
    )


def canonical_hash(value: Any, algorithm: str = "sha256") -> str:
    """Return the canonical hex digest of a value.

    The default algorithm is SHA-256. Changing the algorithm changes the
    digest identity, so callers that need stable identities must fix the
    algorithm themselves.
    """
    if algorithm != "sha256":
        raise ValueError(f"unsupported canonical hash algorithm: {algorithm}")
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
