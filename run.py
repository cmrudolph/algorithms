#!/usr/bin/env python3

import ffi
import importlib
import sys
import timeit

if __name__ == "__main__":
    wrapper = ffi.FFIWrapper.create("multiply")
    cstr1 = wrapper.to_cstr(sys.argv[1])
    cstr2 = wrapper.to_cstr(sys.argv[2])

    result_cstr_long = wrapper.lib.multiply_long(cstr1, cstr2)
    result_long = wrapper.to_pstr(result_cstr_long)
    wrapper.lib.free(result_cstr_long)

    result_cstr_rec = wrapper.lib.multiply_recursive(cstr1, cstr2)
    result_rec = wrapper.to_pstr(result_cstr_rec)
    wrapper.lib.free(result_cstr_rec)

    print(f"LONG: {sys.argv[1]} * {sys.argv[2]} = {result_long}")
    print(f"REC : {sys.argv[1]} * {sys.argv[2]} = {result_rec}")

