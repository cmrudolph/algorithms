#!/usr/bin/env python3

import argparse
import ffi
import importlib
import logging
import sys
import timeit
import wrapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("func")
    parser.add_argument("--verbose", action="store_true")
    known, unknown = parser.parse_known_args()

    level = logging.DEBUG if known.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("run")
    log.debug(f"Known args:{known}; unknown args:{unknown}")

    wrapper = wrapper.WrapperFactory.create(known.name, True)

    func = getattr(wrapper, known.func)
    result = func(*unknown)

    print(f"{known.name}.{known.func}({unknown}) --> {result}")
