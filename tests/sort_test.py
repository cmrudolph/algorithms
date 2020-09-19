import pytest
import random
import impl.sort as sort


@pytest.fixture(params=[
    "c_bubblesort",
    "c_insertionsort",
    "c_mergesort",
    "c_qsort_builtin",
    "c_quicksort",
    "py_builtin",
    "py_mergesort",
    "py_quicksort"])
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
    """
    Some of our algorithms (particularly the quicksorts) have an element
    of randomness in them. Since we have a trustworthy baseline for
    correctness (the builtin sort), we are generating a set of dynamic test
    inputs of a reasonable length and hoping the free variation uncovers any
    interesting mistakes in the implementations.
    """
    iterations = 100
    length = 100
    for i in range(iterations):
        orig = random.sample(range(1, length + 1), length)
        expected = orig[:]
        expected.sort()
        do_test(sut, orig, expected)
