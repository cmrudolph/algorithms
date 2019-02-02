import pytest
from ffi import FFIWrapper


@pytest.fixture(scope="module")
def ffi(request):
    """
    Module-level test fixture that utilizes a convention-based approach to
    create an instance of the relevant FFI wrapper relevant to the test file
    in question. This creates a situation where test file naming must follow
    the convention for everyting to be properly wired up:
      - C module called 'foo' consisting of 'foo.h' and 'foo.c'
      - PY test file called 'foo_test.py'
      - The fixture injected into these tests will be 'foo'
    """
    mod_name = request.module.__name__.replace("_test", "")
    ffi = FFIWrapper.create(mod_name)
    yield ffi
