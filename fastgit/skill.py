"""Object-oriented local git via `Repo`: commits, refs, status, diffs, merges, rebases, stashes, and remotes as live Python objects with terminal-style reprs. Use this for any local repo work: reading history, comparing revisions, cloning, syncing with remotes, and driving merge/rebase/stash workflows including conflict resolution, with no shelling out to `git`.

# The model

git stores snapshots. A `Commit` is immutable, so a handle never goes stale; a `Ref` (branch or tag) is a mutable named pointer to one; log, diff, and status are queries computed on demand. `Repo` is the entry point:

    from fastgit.skill import *
    r = Repo('.')                # any dir inside the repo works; r.exists checks it's a repo
    r.init(b='main')             # create a repo in an empty dir (set user.name/email before committing)
    r = Repo.clone(url, 'dest')  # or clone one; returns a Repo on the fresh checkout

Every result is designed to be displayed bare: reprs mirror the terminal (`--oneline` log, `branch -vv`, `status -sb`, `--stat`). End the cell with the object and read it. Don't loop over fields to rebuild what the repr already shows.

# Reading

    r.log()                    # Commits, newest first; repr is a --oneline log
    r.log('main..feat', n=10)  # git's own range syntax and flags pass through
    r.at('HEAD~2')             # one Commit (sha/ref/rev syntax; None if unknown)
    r.head                     # Commit at HEAD; .sha .msg .author .date .parents
    c.parent                   # first-parent Commit (None for a root commit)
    r.branches, r.tags         # Refs; each has .name .sha .upstream .ahead .behind .commit
    r.branch                   # the current branch as a Ref (None if detached); r('branch', ...) for the raw verb
    r.remotes                  # Remotes (name and url), like `git remote -v`
    r.stashes                  # Stashes; each is a real Commit addressed stash@{n}
    r.cat('rev:path')          # exact file content at a revision (raw verbs strip trailing whitespace; cat doesn't)
    r.blame('core.py', func='load_cfg')  # Blame rows: line -> the last Commit to touch it (via .commit)
    r.trace('core.py', func='load_cfg')  # git log -L: the range's history as Commits, each with .patch

`blame` and `trace` share three range keywords: `func='name'` (git's `:funcname` form; the default funcname pattern only sees column-0 definitions, so indented methods need `*.py diff=python` in the repo's `.gitattributes`), `lines=(start,end)`, and `regex=` (a bare content pattern ranges over just the matched line; a `(start, end)` pair widens it, each element a pattern, an int line number, or a `+N`/`-N` offset str, e.g. `regex=('def f2c', '+3')`). Note that `blame` reports only the last commit to touch each line, so recent reformatting hides a line's true origin; for \"how long has this been so\", use `trace`.

# Status

`r.status` is a `Status`: branch info (`.branch .upstream .ahead .behind`), one entry per changed path, `.clean`, `.conflicts` (the unmerged entries), and `.op` naming any in-progress operation ('merge', 'rebase of feat', 'cherry-pick', ...). Entry `xy` codes are porcelain v2's (`.M` modified-unstaged, `M.` staged, `??` untracked, `UU` conflicted).

# Diffs

Since `b = a + patch`, subtraction spells the patch: `b - a` is `git diff a b`. It works on `Commit` and `Ref`, and `r.diff('v1...HEAD')` passes git's range syntax through. The result is file rows (`.path .adds .dels`) shown `--stat`-style, with the full text in `.patch`.

    r.head - r.at('v0.1')    # what changed since the tag
    print((b - a).patch)     # full patch text
    print(c.patch)           # a Commit's own patch vs its first parent (git show)

# Write ops: conflict is a status, not an error

Every op that changes the working tree returns the resulting `Status`, clean or conflicted; nothing raises on conflict. Read the returned status to see which you got.

    c = r.commit('msg')      # commit staged changes -> new head Commit
    st = r.merge('feat')     # Status; st.clean means merged, st.op=='merge' means paused
    st = r.rebase('main')    # Status, same contract
    st = r.pull()            # Status
    st = r.stash('wip')      # Status; r.stashes[0].pop()/.apply()/.drop() -> Status

Conflict resolution works on the same objects. A conflicted entry has `xy=='UU'` and `.stages`, the [base, ours, theirs] blob shas, and the three versions are readable as `:1:path`/`:2:path`/`:3:path`:

    st = r.merge('feat')
    for e in st.conflicts:                # the unmerged entries (xy=='UU')
        theirs = r.cat(f':3:{e.path}')    # exact content; :2: ours, :1: base. NOT r.show, which strips the final newline
        # write the resolved file, then:
        r.add(e.path)
    r.commit('merge feat')                # concludes the merge; .parents shows 2

To back out of a paused op: `r.merge('--abort')`, `r.rebase('--abort')`.

# Remotes

`fetch` moves the remote-tracking refs and nothing else, so it returns the refreshed `branches`; read `.ahead`/`.behind` there. `push` returns the current branch's refreshed `Ref`, whose tracking bracket confirms the push took.

    r.fetch()                       # -> Refs; look for [origin/main: behind 1]
    r.push('-u', 'origin', 'main')  # -> Ref; publishes the branch and records its upstream
    st = r.pull()                   # fetch plus merge -> Status (can conflict like any merge)
    r.remote('add', 'origin', url)  # remote management stays raw verbs

Everything above `push` is reversible local state; `push` is the one operation that changes what other people and machines see, and a `--force`/`--force-with-lease` push rewrites shared history, discarding remote commits others may have pulled or based work on. When working on someone's behalf, never push on inference: a request to prepare, fix, or update a branch or PR is not a request to publish it. Push only when the specific push has been explicitly asked for, and force-push only when the history rewrite itself has been agreed to - then prefer `--force-with-lease`, which at least refuses to overwrite remote commits you have not seen. When a push is off the table, stop after the commit and report the branch ready to push.

# Everything else: raw verbs

`Repo` subclasses `Git`, so any other git command dispatches dynamically and returns git's own output as a str: `r.switch('main')`, `r.restore('.')`, `r.tag('v1')`. Kwargs become flags (`n=1` -> `-n 1`, `no_ff=True` -> `--no-ff`), `__=['path']` puts paths after `--`, and errors print one terse line and return None (pass `raise_exc=True` to raise instead). `r.log`/`r.diff`/`r.status` impose their own machine formats; for custom `--format` output call the verb explicitly: `r('log', format='%H %s')`.
"""

from fastgit.core import Git, callgit, get_top
from fastgit.repo import (Repo, Commit, Commits, Ref, Refs, Diff, DiffFile, Status, StatusEntry,
    Stash, Stashes, Remote, Remotes, Blame, BlameLine)

__all__ = ['Repo', 'Git', 'callgit', 'get_top', 'Commit', 'Commits', 'Ref', 'Refs', 'Diff', 'DiffFile',
    'Status', 'StatusEntry', 'Stash', 'Stashes', 'Remote', 'Remotes', 'Blame', 'BlameLine']
