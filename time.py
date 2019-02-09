#!/usr/bin/env python3

import argparse
import logging
from util.implementation import ImplementationFactory
from util.timing import time


if __name__ == "__main__":
    """
    Executes a particular function many times, collecting timings and showing
    metrics when finished.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("runs", type=int)
    parser.add_argument("--func")
    parser.add_argument("--verbose", action="store_true")
    known, unknown = parser.parse_known_args()

    level = logging.DEBUG if known.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("time")
    log.debug(f"Known args are {known} and unknown args are {unknown}")

    facade = ImplementationFactory.create(known.name, True)

    results = time(facade, known.name, known.runs, func=known.func, *unknown)
    for r in results:
        print(r)
