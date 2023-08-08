from wedne.utils import Backoffer, distinct_on


def test_distinct_on():
    unique_roots = distinct_on([4, 5, 9], key=lambda x: int(x**0.5))
    assert sorted(unique_roots) == [5, 9]
    unique_roots = distinct_on([5, 4, 9], key=lambda x: int(x**0.5))
    assert sorted(unique_roots) == [4, 9]


def test_backoffer_smoke():
    backoffer = Backoffer(base=2, max_value=100500)
    assert backoffer.failed() == 1
    assert backoffer.failed() == 2
    assert backoffer.failed() == 4
    backoffer.succeeded()
    assert backoffer.failed() == 1


def test_backoffer_with_max_value():
    backoffer = Backoffer(base=10, max_value=69)
    backoffer.failed()
    backoffer.failed()
    assert backoffer.failed() == 69
