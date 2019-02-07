class MultiplyFacade:
    """
    Facade exposing all the necessary functionality to use this
    implementation for testing/benchmarking purposes.
    """
    def __init__(self, ffi_wrapper):
        self._wrapper = ffi_wrapper
        self._lib = ffi_wrapper.lib

    def c_long(self, x, y):
        x_cstr = self._wrapper.to_cstr(str(x))
        y_cstr = self._wrapper.to_cstr(str(y))
        res_cstr = self._lib.multiply_long(x_cstr, y_cstr)
        res = int(self._wrapper.to_pstr(res_cstr))
        self._lib.free(res_cstr)
        return res

    def c_recursive(self, x, y):
        x_cstr = self._wrapper.to_cstr(str(x))
        y_cstr = self._wrapper.to_cstr(str(y))
        res_cstr = self._lib.multiply_recursive(x_cstr, y_cstr)
        res = int(self._wrapper.to_pstr(res_cstr))
        self._lib.free(res_cstr)
        return res

    def py_builtin(self, x, y):
        return int(x) * int(y)

    def create_benchmark_args(self, *args):
        length = int(args[0])
        x = int("9" * length)
        y = int("9" * length)
        return x, y
