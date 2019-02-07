import pytest


@pytest.fixture(params=[
    "c_long",
    "c_recursive",
    "py_builtin"])
def impl(wrapper, request):
    # Given the module-specific wrapper, extract each of the test
    # implementation functions that we want to invoke each case for
    return getattr(wrapper, request.param)


def test_zero_both(impl):
    assert impl(0, 0) == 0


def test_zero_top(impl):
    assert impl(0, 987654321) == 0


def test_zero_bottom(impl):
    assert impl(987654321, 0) == 0


def test_identity_top(impl):
    assert impl(1, 987654321) == 987654321


def test_identity_bottom(impl):
    assert impl(987654321, 1) == 987654321


def test_odd_even_length(impl):
    assert impl(9, 99) == 891


def test_even_odd_length(impl):
    assert impl(99, 9) == 891


def test_maxed_digits(impl):
    assert impl(99, 99) == 9801


def test_trailing_zeroes(impl):
    assert impl(10000, 10000) == 100000000


def test_middle_zeroes(impl):
    assert impl(10001, 10001) == 100020001


def test_big(impl):
    assert impl(9999999999, 9999999999) == 99999999980000000001
