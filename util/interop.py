import cffi
import importlib
import logging
import os


class CLibraryFacade:
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
    def compile_and_load(name):
        """
        Factory method that creates an instance of the wrapper by locating
        and compiling the C code for the given  by compiling the corresponding
        C code and returning a wrapper around that library.
        """
        log = logging.getLogger("CLibraryWrapper")

        h_file = os.path.join("impl", name, name + ".h")
        c_file = os.path.join("impl", name, name + ".c")
        mod_name = "gen._" + name

        log.debug(f"C header is {h_file}")
        log.debug(f"C source is {c_file}")
        log.debug(f"C generated module is {mod_name}")

        with open(h_file, "r") as f:
            header = f.read()
        with open(c_file, "r") as f:
            source = f.read()

        debug = log.getEffectiveLevel() == logging.DEBUG
        log.debug("Compiling C code")
        ffi = cffi.FFI()
        ffi.cdef(header)
        ffi.set_source(mod_name, source)
        ffi.compile(verbose=debug)

        # Load the module and return the 'lib' instance to the caller. This
        # means the caller cab invoke the C functions (from the header) on the
        # instance with no other effort required. Everything from the header
        # will be callable via 'lib'.
        log.debug("Importing generated C module")
        mod = importlib.import_module(mod_name)
        lib = mod.lib

        log.debug(f"Facade lib functions {dir(lib)}")
        return CLibraryFacade(ffi, lib)

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

    def to_c_int_array(self, int_list):
        return self._ffi.new("int[]", int_list)

    def to_py_int_list(self, c_int_array, length):
        return self._ffi.unpack(c_int_array, length)


    @property
    def lib(self):
        """
        Gets the wrapped C library. Declared functions can be invoked directly
        through this instance.
        """
        return self._lib



