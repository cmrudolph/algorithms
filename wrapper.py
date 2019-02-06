import ffi
import importlib
import logging


class WrapperFactory:
    @staticmethod
    def create(name, qualify_module):
        log = logging.getLogger("wrapper_factory")

        log.debug(f"Creating FFI wrapper for {name}")
        ffi_wrapper = ffi.FFIWrapper.create(name)

        mod_short = f"{name}_wrapper"
        mod_name = f"{name}.{mod_short}" if qualify_module else mod_short
        log.debug(f"Importing module {mod_name}")
        mod = importlib.import_module(mod_name)

        inst_type_name = f"{name.title()}Wrapper"
        log.debug(f"Getting wrapper type {inst_type_name}")
        inst_type = getattr(mod, inst_type_name)

        log.debug(f"Creating wrapper instance of {inst_type_name}")
        inst = inst_type(ffi_wrapper)

        return inst
