import timeit


def setup(ffi):
    cstr1 = ffi.to_cstr("9" * 100)
    cstr2 = ffi.to_cstr("9" * 100)

    return cstr1, cstr2


def benchmark(ffi, setup_obj):
    result_cstr = ffi.lib.multiply_long(setup_obj[0], setup_obj[1])
    ffi.lib.free(result_cstr)
