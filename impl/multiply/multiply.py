import os
import random
import util

h_file = os.path.join(os.path.dirname(__file__), "multiply.h")
c_file = os.path.join(os.path.dirname(__file__), "multiply.c")
(ffi, lib) = util.compile("multiply", h_file, c_file)


def c_long(x, y):
    x_cstr = ffi.new("char[]", str(x).encode('ascii'))
    y_cstr = ffi.new("char[]", str(y).encode('ascii'))
    res_cstr = lib.multiply_long(x_cstr, y_cstr)
    res = int(ffi.string(res_cstr).decode('ascii'))
    lib.free(res_cstr)
    return res


def c_recursive(x, y):
    x_cstr = ffi.new("char[]", str(x).encode('ascii'))
    y_cstr = ffi.new("char[]", str(y).encode('ascii'))
    res_cstr = lib.multiply_recursive(x_cstr, y_cstr)
    res = int(ffi.string(res_cstr).decode('ascii'))
    lib.free(res_cstr)
    return res


def py_builtin(x, y):
    return builtin(x, y)


def adapt_run_args(raw_args):
    # RUN: Echo back the two values to multply as-is
    return {
        "x": int(raw_args[0]),
        "y": int(raw_args[1])
    }


def adapt_benchmark_args(raw_args):
    # BENCHMARK: Generate and return integers of length N
    length = int(raw_args[0])
    return {
        "x": int("9" * length),
        "y": int("9" * length)
    }


def builtin(x, y):
    return int(x) * int(y)
