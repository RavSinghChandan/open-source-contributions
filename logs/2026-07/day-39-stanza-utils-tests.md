# Day 39 — Phase 2: stanza utils tests

**Date:** 2026-07-11
**Repo:** [stanfordnlp/stanza](https://github.com/stanfordnlp/stanza)
**PR:** [#1641](https://github.com/stanfordnlp/stanza/pull/1641)
**Type:** Test coverage — regression tests for two untested utilities
**Phase:** 2

---

## What was done

Two helpers in `stanza/models/common/utils.py` had no tests:

- `harmonic_mean` — unweighted + weighted harmonic mean, with a zero
  short-circuit and a weight-length assertion
- `get_adaptive_eval_interval` — scales an eval interval by
  `round(cur / thres)` once the dev set exceeds a threshold

Added two tests to `tests/common/test_utils.py`, next to the existing ones,
matching the direct-assert style. Verified every value against the real
source first.

### Cases covered

- **harmonic_mean:** unweighted (`[1,2,4]`), weighted (`[1,3]` w=`[1,1]`),
  zero present → `0`, mismatched weights → `AssertionError`
- **get_adaptive_eval_interval:** at/below threshold → base unchanged,
  above → scaled, and the banker's-rounding edge (`round(2.5)==2`, so
  `250` vs a `100` threshold gives `20`, not `30`) — the easy-to-trip case

### Files changed

`stanza/tests/common/test_utils.py` — +25 (two test functions).

---

## Why this should merge

- Pure test addition, no behaviour change, zero risk
- Fills a real gap: two untested utilities
- Matches the file's existing conventions exactly
- All assertions verified against the real source
- stanza has no ruff/flake8 gate; the only pyflakes noise is the
  pre-existing `import *` at the top of the file, untouched
- Not competing with any open PR
