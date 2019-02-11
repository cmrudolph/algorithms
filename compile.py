#!/usr/bin/env python3

import argparse
import importlib
import logging
import sys


if __name__ == "__main__":
    """
    In its current, rough form, default to just building the specified test
    case (verify compilation succeeds).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("build")
    log.debug(f"Args:{args}")

    print(f"Compiling C for {args.name}")

    try:
        importlib.import_module(f"impl.{args.name}")
    except:
        log.error(sys.exc_info()[0])
