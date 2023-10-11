---
title: Python's power on big monoliths
---

Python's unhinged dynamic nature, while having it's own drawbacks, has a big
win in the context of big monoliths that evolve rapidly within an organization.

Did you find yourself trying to merge some important dependency upgrade on a
repository with hundreds of merges per day? That introduces breaking changes?
While having a rollback plan in case something goes wrong in production?

In Python, supporting multiple versions of libraries is trivial, just **check
the library's reported version** and act accordingly. That way, the only thing
to upgrade or rollback is the dependency itself, instead of having to deal with
constant conflicts.

Is the migration taking a while, and want to ensure that the codebase works
fine with both versions? Just **run all the tests with both dependency versions**
in your CI pipeline, in parallel. Require both versions to work on every merge,
but just deploy one.

Python's power on big monoliths is **easing up incremental improvements**, and
you might not think about it if your past experience comes mostly from strictier
languages.
