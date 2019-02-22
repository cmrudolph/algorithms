import pytest
import impl.sort as sort


@pytest.fixture(params=[
    "c_mergesort",
    "c_qsort_builtin",
    "c_quicksort",
    "py_builtin",
    "py_mergesort"])
def sut(request):
    return getattr(sort, request.param)


def do_test(sut, actual, expected):
    orig = actual[:]
    result = sut(actual)

    # Ensure original is not modified
    assert actual == orig

    # Ensure returned copy is sorted
    assert result == expected


def test_zero_items(sut):
    do_test(sut, [], [])


def test_one_item(sut):
    do_test(sut, [1], [1])


def test_two_items(sut):
    do_test(sut, [2, 1], [1, 2])


def test_odd_length(sut):
    do_test(sut, [7, 3, 5], [3, 5, 7])


def test_even_length(sut):
    do_test(sut, [4, 8, 6, 2], [2, 4, 6, 8])


def test_already_sorted(sut):
    do_test(sut, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])


def test_reversed(sut):
    do_test(sut, [5, 4, 3, 2, 1], [1, 2, 3, 4, 5])


def test_random(sut):
    orig = [13, 17, 6, 18, 20, 10, 15, 3, 8, 2,\
            11, 4, 16, 19, 12, 7, 14, 9, 1, 5]
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    do_test(sut, orig, expected)