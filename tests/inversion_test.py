import pytest
import impl.inversion as inversion


@pytest.fixture(params=[
    "py_brute_force",
    "py_recursive_merge"])
def sut(request):
    return getattr(inversion, request.param)


def do_test(sut, actual, expected):
    orig = actual[:]
    result = sut(actual)

    # Ensure original is not modified
    assert actual == orig

    # Ensure correct inversion count
    assert result == expected


def test_zero_items(sut):
    do_test(sut, [], 0)


def test_one_item(sut):
    do_test(sut, [1], 0)


def test_two_items(sut):
    do_test(sut, [2, 1], 1)


def test_odd_length(sut):
    do_test(sut, [7, 3, 5], 2)


def test_even_length(sut):
    do_test(sut, [4, 8, 6, 2], 4)


def test_already_sorted(sut):
    do_test(sut, [1, 2, 3, 4, 5], 0)


def test_reversed(sut):
    do_test(sut, [5, 4, 3, 2, 1], 10)


def test_duplicates(sut):
    do_test(sut, [2, 1, 1, 2, 1], 4)


def test_all_same(sut):
    do_test(sut, [0, 0, 0, 0], 0)
