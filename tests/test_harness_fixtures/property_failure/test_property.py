from hypothesis import given
from hypothesis import strategies as st


@given(st.integers())
def test_seeded_property_failure(value: int) -> None:
    assert value != 0
