import pytest
import src.impl.multiply as multiply


@pytest.fixture(params=[
    "c_long",
    "c_recursive",
    "py_builtin"])
def sut(request):
    return getattr(multiply, request.param)


def do_test(sut, x, y, expected):
    product = sut(x, y)
    assert product == expected


def test_zero_both(sut):
    do_test(sut, 0, 0, 0)


def test_zero_top(sut):
    do_test(sut, 0, 987654321, 0)


def test_zero_bottom(sut):
    do_test(sut, 987654321, 0, 0)


def test_identity_top(sut):
    do_test(sut, 1, 987654321, 987654321)


def test_identity_bottom(sut):
    do_test(sut, 987654321, 1, 987654321)


def test_odd_even_length(sut):
    do_test(sut, 9, 99, 891)


def test_even_odd_length(sut):
    do_test(sut, 99, 9, 891)


def test_maxed_digits(sut):
    do_test(sut, 99, 99, 9801)


def test_trailing_zeroes(sut):
    do_test(sut, 10000, 10000, 100000000)


def test_middle_zeroes(sut):
    do_test(sut, 10001, 10001, 100020001)


def test_big(sut):
    do_test(sut, 9999999999, 9999999999, 99999999980000000001)
