def test_echo_int(ffi):
    assert ffi.lib.echo_int(888) == 888
