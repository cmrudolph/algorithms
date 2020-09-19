[![Build Status](https://cmrudolph.semaphoreci.com/badges/algorithms/branches/master.svg)](https://cmrudolph.semaphoreci.com/projects/algorithms)

# algorithms
An attempt to revisit the "glory days" of my CS education by tinkering with various data structures and algorithms. The intent is to write the performance-critical code in C (side benefit being that I get to see if I remember how to do anything in C...), but to use Python + CFFI to simplify invoking/testing/benchmarking or when the implementation in Python is reasonable enough.

## Setup

We need just a few dependencies. They are installable via pip and should be installed into a virtual environment.

```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

## Tests

Tests are written in pytest and should run with no external dependencies.

```
pytest
```

## Ad-hoc running

A simple way to invoke one of our implementation's functions.

```
./run.py [ name ] [ func ] {func args}
```

## Benchmarking

A special type of invoke that leverages timeit to run many iterations of the specified function and output metrics.

```
./time.py [ name ] [ func ] [ runs ] {setup args}
```
