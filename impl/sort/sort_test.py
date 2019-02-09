import pytest
from util.timing import time


@pytest.fixture(params=[
    "c_mergesort",
    "c_qsort_builtin",
    "py_builtin",
    "py_mergesort"])
def impl(facade, request):
    # Given the module-specific facade, extract each of the test
    # implementation functions that we want to invoke each case for
    return getattr(facade, request.param)


def do_test(impl, actual, expected):
    orig = actual[:]
    result = impl(actual)

    # Ensure original is not modified
    assert actual == orig

    # Ensure returned copy is sorted
    assert result == expected


@pytest.mark.parametrize("mode", [
    "sorted",
    "reversed",
    "zero",
    "random"])
def test_timing(facade, mode):
    r = time(facade, "sort", 1, mode, 5)
    assert len(r) == 4


def test_zero_items(impl):
    do_test(impl, [], [])


def test_one_item(impl):
    do_test(impl, [1], [1])


def test_two_items(impl):
    do_test(impl, [2, 1], [1, 2])


def test_odd_length(impl):
    do_test(impl, [7, 3, 5], [3, 5, 7])


def test_even_length(impl):
    do_test(impl, [4, 8, 6, 2], [2, 4, 6, 8])


def test_already_sorted(impl):
    do_test(impl, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])


def test_reversed(impl):
    do_test(impl, [5, 4, 3, 2, 1], [1, 2, 3, 4, 5])


def test_duplicates(impl):
    do_test(impl, [2, 1, 1, 2, 1], [1, 1, 1, 2, 2])


def test_all_same(impl):
    do_test(impl, [0, 0, 0, 0], [0, 0, 0, 0])
