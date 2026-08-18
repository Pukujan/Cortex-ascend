# G0 Architecture Boundary Traceability

## Contract

Requirement IDs: `ASC-G0-R4`, `ASC-G0-R5`  
Invariant: `ASC-INV-FND-001`

The executable dependency direction is inward:

```text
cli -> adapters -> application -> kernel
        |             |
        v             v
       ports --------> kernel
```

The checker encodes these allowed internal dependencies:

- `kernel` -> `kernel` only;
- `ports` -> `ports`, `kernel`;
- `application` -> `application`, `ports`, `kernel`;
- `adapters` -> `adapters`, `application`, `ports`, `kernel`;
- `cli` -> any Ascend layer.

During G0, the kernel has an empty third-party allowlist. It may import Python standard-library modules and `cortex_ascend` internals only. This is stricter than enumerating AWS, AgentCore, LiteLLM, OpenCode, FOSSIL, GitHub, graph, orchestration, and model SDKs individually.

## Evidence

Real-tree command:

```text
python tools/check_architecture.py --root src
```

Expected-failure command:

```text
python tools/check_architecture_negative.py
```

Seeded negative cases cover a prohibited kernel third-party import, an outward kernel dependency, and a cross-layer cycle. The negative harness is successful only when each fixture fails for its declared diagnostic class.

This is a stdlib-only `Import Linter or equivalent` implementation for G0. It introduces no runtime or development dependency and no semantic kernel behavior.
