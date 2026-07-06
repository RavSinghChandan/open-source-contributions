# Day 33 — Phase 2: joblib/joblib bug fix

**Date:** 2026-07-06
**Repo:** [joblib/joblib](https://github.com/joblib/joblib)
**PR:** [#1812](https://github.com/joblib/joblib/pull/1812)
**Issue fixed:** [#1784](https://github.com/joblib/joblib/issues/1784)
**Type:** Bug fix — inconsistency between dump() and load() for os.PathLike
**Phase:** 2

---

## What was done

`dump()` only accepted `pathlib.Path` via an `isinstance(filename, Path)` check.
Any other path-like object (e.g. `BIDSPath` from mne-bids, custom `__fspath__`
classes) fell through to the `is_filename` string check, failed, and raised a
misleading `ValueError`. Meanwhile `load()` already worked for these objects
because `open()` accepts any `os.PathLike` natively.

### Files changed

**`joblib/numpy_pickle.py`**:
- Replaced `isinstance(filename, Path)` → `isinstance(filename, os.PathLike)`
  in both `dump()` and `load()`, converting via `os.fspath()`
- Removed now-unused `from pathlib import Path` import (caught by ruff)

**`joblib/test/test_numpy_pickle.py`**:
- Added `test_dump_and_load_accept_os_pathlike` — uses a minimal inline
  `CustomPath(os.PathLike)` class, no external dependency needed

Net: 21 insertions, 5 deletions across 2 files.

---

## Why this will merge

- Issue had 0 comments, 0 assignees — no competing PRs
- The inconsistency is real and reproducible (load works, dump doesn't)
- Fix is the correct Python idiom: `os.PathLike` is the standard protocol
- Ruff lint passes (including removing the dead import), both tests pass
- We already have a merged-pending docstring PR in this repo (#1811) —
  maintainers have already seen the name RavSinghChandan
