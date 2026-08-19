.DEFAULT_GOAL := check

UV ?= uv
UV_RUN := $(UV) run --frozen

.PHONY: check

# Keep this ordered list as the single local/CI G0 qualification graph.  Every
# recipe is a separate command so GNU make stops immediately on the first
# failed gate; no failure is masked with a leading '-' or shell fallback.
check:
	$(UV) lock --check
	$(UV_RUN) ruff format --check .
	$(UV_RUN) ruff check .
	$(UV_RUN) mypy --strict src/cortex_ascend tools
	$(UV_RUN) python tools/check_architecture.py --root src
	$(UV_RUN) pytest -q tests/unit
	$(UV_RUN) pytest -q tests/property
	$(UV_RUN) python tools/check_docs.py
	$(UV_RUN) python tools/check_github_workflows.py
	$(UV_RUN) python tools/check_secrets.py
	$(UV) pip check
	$(UV_RUN) python tools/check_architecture_negative.py
	$(UV_RUN) python tools/check_static_negative.py
	$(UV_RUN) python tools/check_test_negative.py
	$(UV_RUN) python tools/check_docs_negative.py
	$(UV_RUN) python tools/check_github_workflows_negative.py
	$(UV_RUN) python tools/check_secrets_negative.py
