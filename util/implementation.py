import importlib
import logging
from util.interop import CLibraryFacade


class ImplementationFactory:
    """
    Factory that understands our project convention and knows how to create
    instances of the facade types that correspond to each of our
    unique implementations.
    """
    @staticmethod
    def create(name, qualify_module):
        log = logging.getLogger("ImplementationFactory")

        log.debug(f"Creating C library facade for {name}")
        ffi_wrapper = CLibraryFacade.compile_and_load(name)

        # The module name to use when loading from the same context as the
        # module resides in (e.g. pytest)
        mod_short = f"{name}_facade"

        # The module name to use when loading via a top-level entry point
        # (e.g. main function in the project root)
        mod_qualified = f"impl.{name}.{mod_short}"

        mod_name = mod_qualified if qualify_module else mod_short
        log.debug(f"Importing module {mod_name}")
        mod = importlib.import_module(mod_name)

        facade_type = f"{name.title()}Facade"
        log.debug(f"Locating facade type {facade_type}")
        inst_type = getattr(mod, facade_type)

        if ffi_wrapper is not None:
            log.debug(f"Instantiating facade type {facade_type} with C")
            facade_inst = inst_type(ffi_wrapper)
        else:
            log.debug(f"Instantiating facade type {facade_type} without C")
            facade_inst = inst_type()

        funcs = [f for f in dir(facade_inst) if not f.startswith("_")]
        log.debug(f"Facade functions {funcs}")

        return facade_inst
