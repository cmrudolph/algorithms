import cffi
import importlib
import os
import sys


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
    w = FFIWrapper.create(sys.argv[1])
