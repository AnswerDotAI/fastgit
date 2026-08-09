"""Use git from python, fast

Modules:

- `fastgit.skill`: Object-oriented local git via `Repo`: commits, refs, status, diffs, merges, rebases, stashes, and remotes as live Python objects with terminal-style reprs. Use this for any local repo work: reading history, comparing revisions, cloning, syncing with remotes, and driving merge/rebase/stash workflows including conflict resolution, with no shelling out to `git`."""

__version__ = "0.1.1"

from .core import *
from .repo import *
