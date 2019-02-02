def multiply_long(ffi, x_pstr, y_pstr):
    x_cstr = ffi.to_cstr(x_pstr)
    y_cstr = ffi.to_cstr(y_pstr)
    result_cstr = ffi.lib.multiply_long(x_cstr, y_cstr)
    return ffi.to_pstr(result_cstr)


def test_zero_top(ffi):
    assert multiply_long(ffi, "0", "987654321") == "0"


def test_zero_bottom(ffi):
    assert multiply_long(ffi, "987654321", "0") == "0"


def test_identity_top(ffi):
    assert multiply_long(ffi, "1", "987654321") == "987654321"


def test_identity_bottom(ffi):
    assert multiply_long(ffi, "987654321", "1") == "987654321"
