import pytest
from util.timing import time


@pytest.fixture(params=[
    "py_brute_force"])
def impl(facade, request):
    # Given the module-specific facade, extract each of the test
    # implementation functions that we want to invoke each case for
    return getattr(facade, request.param)


def do_test(impl, actual, expected):
    orig = actual[:]
    result = impl(actual)

    # Ensure original is not modified
    assert actual == orig

    # Ensure correct inversion count
    assert result == expected


@pytest.mark.parametrize("mode", [
    "sorted",
    "reversed",
    "zero",
    "random",
    "foo"])
def test_timing(facade, mode):
    r = time(facade, "inversion", 1, mode, 5)
    assert len(r) == 2


def test_zero_items(impl):
    do_test(impl, [], 0)


def test_one_item(impl):
    do_test(impl, [1], 0)


def test_two_items(impl):
    do_test(impl, [2, 1], 1)


def test_odd_length(impl):
    do_test(impl, [7, 3, 5], 2)


def test_even_length(impl):
    do_test(impl, [4, 8, 6, 2], 4)


def test_already_sorted(impl):
    do_test(impl, [1, 2, 3, 4, 5], 0)


def test_reversed(impl):
    do_test(impl, [5, 4, 3, 2, 1], 10)


def test_duplicates(impl):
    do_test(impl, [2, 1, 1, 2, 1], 4)


def test_all_same(impl):
    do_test(impl, [0, 0, 0, 0], 0)
