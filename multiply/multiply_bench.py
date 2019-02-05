import timeit


def setup(ffi):
    cstr1 = ffi.to_cstr("9" * 1000)
    cstr2 = ffi.to_cstr("9" * 1000)

    return cstr1, cstr2


def benchmark_multiply_long(ffi, setup_obj):
    result_cstr = ffi.lib.multiply_long(setup_obj[0], setup_obj[1])
    ffi.lib.free(result_cstr)


def benchmark_multiply_recursive(ffi, setup_obj):
    result_cstr = ffi.lib.multiply_recursive(setup_obj[0], setup_obj[1])
    ffi.lib.free(result_cstr)
