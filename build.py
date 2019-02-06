#!/usr/bin/env python3

import ffi
import sys

if __name__ == "__main__":
    """
    In its current, rough form, default to just building the specified test
    case (verify compilation succeeds).
    """
    short_name = sys.argv[1]

    print(f"Compiling {short_name}")

    try:
        wrapper = ffi.FFIWrapper.create(short_name)
    except:
        pass
