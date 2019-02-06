#!/usr/bin/env python3

import ffi
import importlib
import sys
import timeit

if __name__ == "__main__":
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    wrapper = ffi.FFIWrapper.create("multiply")
    mod = importlib.import_module("multiply.multiply")
    mul = getattr(mod, "Multiply")
    mul_inst = mul(wrapper)

    func_long = getattr(mul_inst, "multiply_long_c")
    result_long = func_long(x, y)

    func_rec = getattr(mul_inst, "multiply_recursive_c")
    result_rec = func_rec(x, y)

    func_builtin = getattr(mul_inst, "multiply_builtin_py")
    result_builtin = func_builtin(x, y)

    print(f"LONG: {x} * {y} = {result_long}")
    print(f"REC : {x} * {y} = {result_rec}")
    print(f"PY  : {x} * {y} = {result_builtin}")
