# Day 34 — Phase 2: joblib review responses (both PRs)

**Date:** 2026-07-11
**Repo:** [joblib/joblib](https://github.com/joblib/joblib)
**PRs:** [#1811](https://github.com/joblib/joblib/pull/1811) · [#1812](https://github.com/joblib/joblib/pull/1812)
**Type:** Review response — addressed maintainer change requests
**Phase:** 2
**Reviewer:** Nanored4498

---

## What was done

Both joblib PRs got concrete review comments from maintainer Nanored4498.
Addressed both today — this is the step that actually moves a PR toward merge.

### PR #1811 (docstrings)

Reviewer flagged that the `short_format_time` docstring showed `' 42.0s'`
(one leading space) but the function returns `" %5.1fs"`, which renders as
`'  42.0s'` (two spaces) for a value of 42.0. Verified by running the format
string directly, then fixed the docstring to match the real output.

- `joblib/logger.py` — one-char docstring fix (single → double space)
- Replied confirming the format-string reasoning

### PR #1812 (os.PathLike fix)

Reviewer left two comments:
1. Revert the `logger.py` docstrings from this PR — they overlap with #1811
   and should land there, not here
2. On `numpy_pickle.py` line 489, change `pathlib.Path` → `os.PathLike` in
   the `dump()` docstring (the PR now accepts any os.PathLike)

Did both — reverted logger.py fully to upstream so #1812 is now *only* the
pathlike change + its test, and applied the `os.PathLike` wording to the
docstrings of both `dump()` and `load()` for consistency (not just line 489).

- `joblib/numpy_pickle.py` — 2 docstring lines, logger.py overlap removed
- Ran the pathlike tests: 2 passed
- Replied summarising both changes

---

## Status after today

| PR | State | Mergeable | Notes |
|----|-------|-----------|-------|
| #1811 | open | yes | maintainer's only comment addressed |
| #1812 | open | yes | both comments addressed, PR now clean |

Both are now waiting on the maintainer's re-review. Responding to review
comments the same day is exactly what turns a stale doc PR into a merge —
these two are the closest of the 24 open PRs.
