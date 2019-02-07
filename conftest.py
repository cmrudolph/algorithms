import pytest
from util.implementation import ImplementationFactory


@pytest.fixture(scope="module")
def wrapper(request):
    """
    Module-level test fixture that utilizes a convention-based approach to
    create an instance of the relevant wrapper correponding to the given
    test file. This creates a situation where test file naming must follow
    the convention for everyting to be properly wired up:
      - C module called 'foo' consisting of 'foo.h' and 'foo.c'
      - PY test file called 'foo_test.py'
      - PY facade module called 'foo_facade.py'
      - PY facade class in called 'FooFacade'
    """

    # Test module (foo_test.py)
    mod_name = request.module.__name__.replace("_test", "")
    return ImplementationFactory.create(mod_name, False)
