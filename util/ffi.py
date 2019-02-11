import cffi
import importlib


def compile(name, header, source):
    mod_name = "gen._" + name
    ffi = cffi.FFI()
    ffi.cdef(open(header).read())
    ffi.set_source(
        mod_name,
        open(source).read(),
        extra_compile_args=['-O3', '-march=native', '-ffast-math'])
    ffi.compile()

    mod = importlib.import_module(mod_name)
    lib = mod.lib

    return ffi, lib
