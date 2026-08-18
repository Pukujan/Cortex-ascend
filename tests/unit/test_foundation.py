import cortex_ascend


def test_package_metadata_is_importable() -> None:
    assert cortex_ascend.__version__ == "0.0.0"
