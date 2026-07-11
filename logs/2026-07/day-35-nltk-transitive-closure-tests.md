# Day 35 — Phase 2: nltk/nltk test coverage

**Date:** 2026-07-11
**Repo:** [nltk/nltk](https://github.com/nltk/nltk)
**PR:** [#3703](https://github.com/nltk/nltk/pull/3703)
**Type:** Test coverage — regression tests for an untested utility
**Phase:** 2

---

## What was done

`transitive_closure` in `nltk/util.py` is a real graph algorithm (a variant of
the Ioannidis & Ramakrishnan marking algorithm) but had **zero unit tests** —
it wasn't in `test_util.py`, the util doctest, or anywhere else in the suite.

Read the implementation, verified its actual behaviour by hand on several
inputs, then added tests to `nltk/test/unit/test_util.py` (right next to the
existing everygrams tests, same plain-pytest style, no test class).

### Cases covered

- **chain** `a→b→c` — plain closure
- **reflexive=True** — each node includes itself
- **cycle** `a↔b` — terminates, both nodes reachable from both
- **empty graph** — returns `{}`
- **no input mutation** — the function copies its sets internally; pinned this
  so a future refactor can't silently start mutating the caller's dict

### Files changed

`nltk/test/unit/test_util.py` — +29/−1 (one import line + five test functions).

---

## Why this should merge

- Pure test addition — no behaviour change, zero risk to existing code
- Fills a genuine gap: a real algorithm that was completely untested
- All 10 tests in the file pass (5 existing + 5 new)
- Full pre-commit passes locally: black, isort, ruff, pyupgrade
- Followed the file's existing conventions exactly (function-style pytest)
- Not competing with any open PR — checked before starting

## Note on today's target selection

Every well-scoped *bug* in the popular safe repos (nltk #3554/#3699,
datasets #8246/#8296) already had a same-week PR from another contributor.
Rather than duplicate or step on those, went with an unclaimed coverage gap —
still genuine, useful, and mergeable, without treading on anyone's work.
