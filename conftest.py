import importlib
import pytest
from ffi import FFIWrapper


@pytest.fixture(scope="module")
def wrapper(request):
    """
    Module-level test fixture that utilizes a convention-based approach to
    create an instance of the relevant wrapper correponding to the given
    test file. This creates a situation where test file naming must follow
    the convention for everyting to be properly wired up:
      - C module called 'foo' consisting of 'foo.h' and 'foo.c'
      - PY test file called 'foo_test.py'
      - PY wrapper module called 'foo.py'
      - PY wrapper class in wrapper called 'Foo'
    """

    # Test module (foo_test.py)
    mod_name = request.module.__name__.replace("_test", "")

    # C library sources (foo.c, foo.h)
    ffi = FFIWrapper.create(mod_name)

    # PY wrapper module (foo.py)
    mod = importlib.import_module(mod_name)

    # PY wrapper class (foo.Foo)
    wrapper_type = getattr(mod, mod_name.title())

    # Construct and return PY wrapper instance (consumer facing artifact)
    return wrapper_type(ffi)
