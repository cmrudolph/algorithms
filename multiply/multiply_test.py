import pytest

@pytest.fixture(params=["multiply_long", "multiply_recursive"])
def impl(ffi, request):
    return getattr(ffi.lib, request.param)


def invoke(ffi, impl, x_pstr, y_pstr):
    x_cstr = ffi.to_cstr(x_pstr)
    y_cstr = ffi.to_cstr(y_pstr)
    result_cstr = impl(x_cstr, y_cstr)
    result = ffi.to_pstr(result_cstr)
    ffi.lib.free(result_cstr)
    return result


def test_zero_both(ffi, impl):
    assert invoke(ffi, impl, "0", "0") == "0"


def test_zero_top(ffi, impl):
    assert invoke(ffi, impl, "0", "987654321") == "0"


def test_zero_bottom(ffi, impl):
    assert invoke(ffi, impl, "987654321", "0") == "0"


def test_zero_padding(ffi, impl):
    assert invoke(ffi, impl, "00", "00") == "0"


def test_identity_top(ffi, impl):
    assert invoke(ffi, impl, "1", "987654321") == "987654321"


def test_identity_bottom(ffi, impl):
    assert invoke(ffi, impl, "987654321", "1") == "987654321"


def test_odd_even_length(ffi, impl):
    assert invoke(ffi, impl, "9", "99") == "891"


def test_even_odd_length(ffi, impl):
    assert invoke(ffi, impl, "99", "9") == "891"


def test_maxed_digits(ffi, impl):
    assert invoke(ffi, impl, "99", "99") == "9801"


def test_trailing_zeroes(ffi, impl):
    assert invoke(ffi, impl, "10000", "10000") == "100000000"
