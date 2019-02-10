#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
from importlib import import_module


if __name__ == "__main__":
    """
    Ad-hoc runner that is able to consume certain known arguments to spin up
    instances of whatever implementation/function we want to call and then
    pass along the remaining args to said function.
    """
    parser = ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("func")
    parser.add_argument("--verbose", action="store_true")
    known, unknown = parser.parse_known_args()

    level = logging.DEBUG if known.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("run")
    log.debug(f"Known args are {known} and unknown args are {unknown}")

    mod = import_module(f"src.impl.{known.name}")

    func = getattr(mod, known.func)
    run_args = mod.adapt_run_args(unknown)
    log.debug(f"Run args {run_args}")

    result = func(**run_args)

    print(f"{known.name}.{known.func} --> {result}")
