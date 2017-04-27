# Python Meta-Programming _once and for all_

Meta-programming can get overwhelming really fast. 

This repo is my humble attempt to explain the most common magic methods that appear in Python3 meta-programming. I keep these demo scripts as references for future projects, so that I don't have to go down the rabbit hole over and over again.

In `boilerplate.py`, I list the standard method signatures for:

- Metaclass:
    - `__new__`
    - `__init__`
    - `__call__`

- Concrete class:
    - `__new__`
    - `__init__`

In `examples.py`, I show a few codee snippets of how to use or abuse metaclasses, aggregated from StackOverflow and other excellent tutorials. 
