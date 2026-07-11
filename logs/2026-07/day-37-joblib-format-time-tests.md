# Day 37 — Phase 2: joblib format_time tests

**Date:** 2026-07-11
**Repo:** [joblib/joblib](https://github.com/joblib/joblib)
**PR:** [#1814](https://github.com/joblib/joblib/pull/1814)
**Type:** Test coverage — regression tests for two untested utilities
**Phase:** 2

---

## What was done

`format_time` and `short_format_time` in `joblib/logger.py` had no direct
tests — only the `PrintTime` smoke test in `test_logger.py` exercises
`format_time` indirectly. These are the same two functions I documented in
#1811, so tests are a natural follow-up.

Added three tests to `test_logger.py`:

- `test_format_time` — the seconds+minutes output
- `test_short_format_time_seconds` — the sub-minute branch (` %5.1fs`)
- `test_short_format_time_minutes` — the over-a-minute branch (`%4.1fmin`)

Expected values are computed through `_squeeze_time` so the Windows `-0.1s`
adjustment path stays correct — the tests pass on every platform, not just
non-Windows CI.

### Files changed

`joblib/test/test_logger.py` — +21/−1 (import line + three test functions).

---

## Why this should merge

- Pure test addition, no behaviour change, zero risk
- Fills a real gap: both functions were untested directly
- Cross-platform safe (goes through `_squeeze_time`, not hardcoded output)
- All 4 tests in the file pass; ruff + ruff-format clean (joblib CI)
- Natural continuation of #1811 — maintainers already engaged there
- Checked: no competing PR for these functions

## Note on target selection

numba is now off-limits for this kind of work — a maintainer confirmed numba
adopted the LLVM AI policy ("AI tools must not be used to fix good-first-issues").
Recorded in the skip list. Stuck with the uncontested pattern: coverage for a
genuinely untested pure function in a repo where they already know the name.
