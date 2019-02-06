class Multiply:
    def __init__(self, ffi_wrapper):
        self._wrapper = ffi_wrapper
        self._lib = ffi_wrapper.lib

    def multiply_long_c(self, x, y):
        x_cstr = self._wrapper.to_cstr(str(x))
        y_cstr = self._wrapper.to_cstr(str(y))
        res_cstr = self._lib.multiply_long(x_cstr, y_cstr)
        res = int(self._wrapper.to_pstr(res_cstr))
        self._lib.free(res_cstr)
        return res

    def multiply_recursive_c(self, x, y):
        x_cstr = self._wrapper.to_cstr(str(x))
        y_cstr = self._wrapper.to_cstr(str(y))
        res_cstr = self._lib.multiply_recursive(x_cstr, y_cstr)
        res = int(self._wrapper.to_pstr(res_cstr))
        self._lib.free(res_cstr)
        return res

    def multiply_builtin_py(self, x, y):
        return x * y

    def get_benchmark_args(self):
        x = int("9" * 500)
        y = int("9" * 500)
        return x, y
