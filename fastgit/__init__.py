"""Use git from python, fast

`fastgit` is a Python wrapper for the `git` command line, for use in scripts and interactive sessions. You call git subcommands as Python methods and pass options as keyword arguments.

Commands run through the installed `git` executable and return its text output. There is no separate object model for repositories and commits. Both synchronous and asynchronous clients are available."""

__version__ = "0.1.4"

from .core import *
