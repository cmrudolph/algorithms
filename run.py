#!/usr/bin/env python3

import argparse
import importlib
import logging
from util.implementation import ImplementationFactory


if __name__ == "__main__":
    """
    Ad-hoc runner that is able to consume certain known arguments to spin up
    instances of whatever implementation/function we want to call and then
    pass along the remaining args to said function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("func")
    parser.add_argument("--verbose", action="store_true")
    known, unknown = parser.parse_known_args()

    level = logging.DEBUG if known.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("run")
    log.debug(f"Known args are {known} and unknown args are {unknown}")

    wrapper = ImplementationFactory.create(known.name, True)

    func = getattr(wrapper, known.func)
    result = func(*unknown)

    print(f"{known.name}.{known.func}({unknown}) --> {result}")
