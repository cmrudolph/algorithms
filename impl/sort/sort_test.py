import pytest


@pytest.fixture(params=[
    "c_mergesort",
    "c_qsort_builtin",
    "py_mergesort",
    "py_builtin"])
def impl(wrapper, request):
    # Given the module-specific wrapper, extract each of the test
    # implementation functions that we want to invoke each case for
    return getattr(wrapper, request.param)


def test_empty(impl):
    assert impl([]) == []


def test_single(impl):
    assert impl([888]) == [888]


def test_sorted(impl):
    assert impl([1, 2, 3]) == [1, 2, 3]


def test_reversed(impl):
    assert impl([3, 2, 1]) == [1, 2, 3]


def test_duplicates(impl):
    assert impl([2, 1, 1, 2, 1]) == [1, 1, 1, 2, 2]


def test_odd_length(impl):
    assert impl([7, 3, 5]) == [3, 5, 7]


def test_even_length(impl):
    assert impl([4, 8, 6, 2]) == [2, 4, 6, 8]
