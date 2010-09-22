#! /usr/bin/python3.1

"""A framework for GIT.

To execute a named METHOD:
$ python3 -m porcelain [Options] METHOD [Method Options]

Options:
  --git-dir=DIR     Repository directory (default is $PWD/.git)
  --work-tree=DIR   Work tree directory (default is $PWD)

To show an attribute of class Porcelain:
$ python3 -m porcelain ATTRIBUTE [KEYWORD]

Examples:
$ python3 -m porcelain config user.name
$ python3 -m porcelain work_tree

To show this help:
$ python3 -m porcelain
$ python3 -m porcelain --help

To show the class Porcelain help:
$ python3 -m porcelain help

To show help for a given METHOD:
$ python3 -m porcelain help METHOD
$ python3 -m porcelain --help METHOD
$ python3 -m porcelain METHOD --help

From within a python3 interpreter,
>>> from porcelain import Porcelain
>>> porcelain = Porcelain()
>>> help(porcelain)
>>> porcelain.config['user.name']
"""

from .base import Porcelain, Dict

try:
    from .__version__ import __version__
except ImportError:
    __version__ = "v0.1"

__all__ = [ 'base' ]
