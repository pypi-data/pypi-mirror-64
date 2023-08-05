# Pythomata


[![](https://img.shields.io/pypi/v/pythomata.svg)](https://pypi.python.org/pypi/pythomata)
[![](https://img.shields.io/travis/whitemech/pythomata.svg)](https://travis-ci.org/whitemech/pythomata)
[![](https://img.shields.io/pypi/pyversions/pythomata.svg)](https://pypi.python.org/pypi/pythomata)
[![](https://img.shields.io/badge/docs-mkdocs-9cf)](https://www.mkdocs.org/)
[![](https://img.shields.io/badge/status-development-orange.svg)](https://img.shields.io/badge/status-development-orange.svg)
[![codecov](https://codecov.io/gh/whitemech/pythomata/branch/master/graph/badge.svg)](https://codecov.io/gh/whitemech/pythomata)
[![](https://img.shields.io/badge/flake8-checked-blueviolet)](https://img.shields.io/badge/flake8-checked-blueviolet)
[![](https://img.shields.io/badge/mypy-checked-blue)](https://img.shields.io/badge/mypy-checked-blue)
[![](https://img.shields.io/badge/license-LGPLv3%2B-blue)](./LICENSE)

Python implementation of automata theory.

## Links

- GitHub: [https://github.com/whitemech/pythomata](https://github.com/whitemech/pythomata)
- PyPI: [https://pypi.org/project/pythomata/](https://pypi.org/project/pythomata/)
- Documentation: [https://whitemech.github.io/pythomata](https://whitemech.github.io/pythomata)
- Changelog: [https://whitemech.github.io/pythomata/release-history/](https://whitemech.github.io/pythomata/release-history/)
- Issue Tracker:[https://github.com/whitemech/pythomata/issues](https://github.com/whitemech/pythomata/issues)
- Download: [https://pypi.org/project/pythomata/#files](https://pypi.org/project/pythomata/#files)


## Install

- from [PyPI](https://pypi.org/project/pythomata/):
```
pip install pythomata
```
- or, from source (e.g. `develop` branch):
```
pip install git+https://github.com/whitemech/pythomata.git@develop
```

- or, clone the repository and install:
```
git clone htts://github.com/whitemech/pythomata.git
cd pythomata
pip install .
```

## How to use

* Define an automaton:

```python
from pythomata import SimpleDFA
alphabet = {"a", "b", "c"}
states = {"s1", "s2", "s3"}
initial_state = "s1"
accepting_states = {"s3"}
transition_function = {
    "s1": {
        "b" : "s1",
        "a" : "s2"
    },
    "s2": {
        "a" : "s3",
        "b" : "s1"
    },
    "s3":{
        "c" : "s3"
    }
}
dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
```

* Test word acceptance:

```python
# a word is a list of symbols
word = "bbbac"
dfa.accepts(word)        # True

# without the last symbol c, the final state is not reached
dfa.accepts(word[:-1])   # False
```

* Operations such as minimization and trimming:

```python
dfa_minimized = dfa.minimize()
dfa_trimmed = dfa.trim()
```

* Translate into a [`graphviz.Digraph`](https://graphviz.readthedocs.io/en/stable/api.html#graphviz.Digraph)
  instance:

```python
graph = dfa.minimize().trim().to_graphviz()
```

To print the automaton:
```
graph.render("path_to_file")
```

For that you will need to install Graphviz.
Please look at their [download page](https://graphviz.gitlab.io/download/)
for detailed instructions depending on your system.

The output looks like the following:

<p align="center">
  <img width="150" height="300" src="./images/my_awesome_automaton.svg" />
</p>


## Features


* Basic DFA and NFA support;
* Algorithms for DFA minimization and trimming;
* Algorithm for NFA determinization;
* Translate automata into Graphviz objects.
* Support for Symbolic Automata.


## Tests

To run the tests:
```
tox
```
To run only the code style checks:
```
tox -e flake8 -e mypy
```
## Docs

To build the docs:

```
mkdocs build
```

To view documentation in a browser

```
mkdocs serve
```

and then go to [http://localhost:8000](http://localhost:8000)


## License

Pythomata is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).

Copyright 2018-2020 [WhiteMech](https://whitemech.github.io)

