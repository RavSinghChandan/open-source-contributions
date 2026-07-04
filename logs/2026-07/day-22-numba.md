# Day 22 — Contribution to numba/numba

| Field | Value |
|-------|-------|
| **Date** | 2026-07-04 |
| **Repo** | [numba/numba](https://github.com/numba/numba) |
| **Package** | `numba` — `numba/core/utils.py` |
| **Stars** | ~10,000 |
| **Type** | Docs — add missing docstrings |
| **PR** | [#10686 — add missing docstrings to runonce, format_time and benchmark in numba/core/utils.py](https://github.com/numba/numba/pull/10686) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~60% — numba is large and slow-moving, docs PRs occasionally merge |

---

## What Was Done

Added NumPy-style docstrings to 3 public utility functions in `numba/core/utils.py`. `runonce` is a decorator that ensures the wrapped function only executes once regardless of how many times it is called. `format_time` converts a raw elapsed time in seconds into a human-readable string with appropriate units (ns, µs, ms, s). `benchmark` runs a callable repeatedly and returns statistics including the minimum elapsed time. The existing documented functions in the file use NumPy style (Parameters/Returns sections), so the new docstrings follow the same convention.

## Files Changed

```
numba/core/utils.py
  — added docstrings to runonce(), format_time(), benchmark()
```

## Why This Repo

numba is one of the most widely used JIT compilers for Python with ~10,000 GitHub stars and hundreds of millions of downloads. The core/utils module contains fundamental building blocks used throughout the compiler pipeline. No CLAUDE.md, no AGENTS.md, no mypy enforcement in CI.

## Lesson Learned / Notes

NumPy-style docstrings use section headers underlined with dashes (e.g., `Parameters\n----------`). This style is more verbose than Google style but is standard in scientific Python (NumPy, SciPy, pandas). The `runonce` decorator pattern is common in compiler code to avoid re-running expensive initialization.

---
*Log created: 2026-07-04 | PR: https://github.com/numba/numba/pull/10686*
