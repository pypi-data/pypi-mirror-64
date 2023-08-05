# -*- coding: utf-8 -*-

"""Top-level package for Pythomata."""

from pythomata.__version__ import __title__, __description__, __url__, __version__
from pythomata.__version__ import (
    __author__,
    __author_email__,
    __license__,
    __copyright__,
)


from .impl.simple import SimpleDFA
from .impl.symbolic import SymbolicAutomaton, PropositionalInterpretation
