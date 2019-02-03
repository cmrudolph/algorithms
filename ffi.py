import cffi
import importlib
import os
import sys
import timeit


class FFIWrapper:
    """
    My own wrapper around the FFI functionality needed by my tests. This
    provides not only access to the C library, but also surfaces certain
    common FFI-related functions (e.g. string conversions) to make
    life easier.
    """
    def __init__(self, ffi, lib):
        self._ffi = ffi
        self._lib = lib

    @staticmethod
    def create(name):
        """
        Factory method that creates an instance by compiling the corresponding
        C code and returning a wrapper around that library.
        """
        h_file = os.path.join(name, name + ".h")
        c_file = os.path.join(name, name + ".c")
        mod_name = "gen._" + name

        # Read the .h and .c files from disk. Our convention is to require that
        # the names of the files match the name of the module we are building.
        with open(h_file, "r") as f:
            header = f.read()
        with open(c_file, "r") as f:
            source = f.read()

        # Use CFFI to compile our header and source files into a library that
        # we can call into using the CFFI plumbing later.
        ffi = cffi.FFI()
        ffi.cdef(header)
        ffi.set_source(mod_name, source)
        ffi.compile()

        # Load the module and return the 'lib' instance to the caller. This
        # means the caller cab invoke the C functions (from the header) on the
        # instance with no other effort required.
        mod = importlib.import_module(mod_name)
        lib = mod.lib

        return FFIWrapper(ffi, lib)

    def to_cstr(self, pstr):
        """
        Converts a Python string int a C-style string (char array). ASCII
        encoding is assumed.
        """
        return self._ffi.new("char[]", pstr.encode('ascii'))

    def to_pstr(self, cstr):
        """
        Converts a C-style string (char array) into a Python string. ASCII
        encoding is assumed.
        """
        return self._ffi.string(cstr).decode('ascii')

    @property
    def lib(self):
        """
        Gets the wrapped C library. Declared functions can be invoked directly
        through this instance.
        """
        return self._lib


if __name__ == "__main__":
    """
    In its current, rough form, default to running a custom benchmark
    function for the specified module. This has a lot of room for improvement,
    but it lets us run code in a timed fashion for now.
    """
    short_name = sys.argv[1]
    iterations = int(sys.argv[2])

    print(f"Benchmarking {short_name} with {iterations} iterations")

    ffi = FFIWrapper.create(short_name)

    # Convention 1: Assume there is a file called [NAME]/[NAME]_bench.py.
    mod_name = f"{short_name}.{short_name}_bench"
    mod = importlib.import_module(mod_name)

    # Convention 2: Assume there is a setup function to invoke.
    setup_obj = mod.setup(ffi)

    # Convention 3: Assume there is a benchmark function to invoke.
    code = "mod.benchmark(ffi, setup_obj)"
    setup = "from __main__ import setup_obj, mod, ffi"
    print(timeit.timeit(code, setup=setup, number=int(iterations)))
