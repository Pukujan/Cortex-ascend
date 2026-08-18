from hypothesis import given, strategies as st


@given(st.lists(st.integers()))
def test_reverse_twice_round_trips(values: list[int]) -> None:
    assert list(reversed(list(reversed(values)))) == values
