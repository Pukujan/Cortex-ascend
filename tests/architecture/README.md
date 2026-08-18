# G0 architecture qualification fixtures

These fixtures are deliberately invalid. `tools/check_architecture_negative.py` is green only when each bad structure is rejected for its declared reason.

- `prohibited_kernel_import`: proves the kernel cannot import third-party infrastructure (`boto3` is the seeded example).
- `reverse_layer_import`: proves the kernel cannot depend outward on `application`.
- `architecture_cycle`: proves a cross-layer cycle is reported explicitly.

The real repository tree is checked separately with `tools/check_architecture.py --root src`.
