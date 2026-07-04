# Day 15 — Contribution to nltk/nltk

| Field | Value |
|-------|-------|
| **Date** | 2026-06-30 |
| **Repo** | [nltk/nltk](https://github.com/nltk/nltk) |
| **Package** | `nltk` — `nltk/compat.py`, `nltk/decorators.py` |
| **Stars** | ~14,000 |
| **Type** | Docs — add missing docstrings |
| **PR** | [#3688 — add missing docstrings to 5 utility functions in compat.py and decorators.py](https://github.com/nltk/nltk/pull/3688) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~65% — NLTK is a mature project with slower review cycles but docstring PRs are accepted |

---

## What Was Done

Added Epytext/NumPy-style docstrings to 5 public utility functions spread across two foundational utility modules. In `compat.py`, documented compatibility shims that handle Python 2/3 differences still present in the codebase (the module exists for historical reasons). In `decorators.py`, documented decorator utilities including `overridden` (checks if a method is overridden in a subclass) and `py_meth_to_classmethod`. These gaps existed because both files are legacy utility modules written before the project adopted consistent documentation standards.

## Files Changed

```
nltk/compat.py
  — added docstrings to 3 compatibility utility functions

nltk/decorators.py
  — added docstrings to 2 decorator utility functions:
    overridden(), py_meth_to_classmethod()
```

## Why This Repo

NLTK is the foundational NLP library that taught a generation of NLP practitioners (~14K stars). Despite its maturity, several utility modules still lack docstrings. The `decorators.py` module in particular has functions used throughout the class hierarchy that have no documentation. Adding docstrings to these makes the codebase more accessible to new contributors learning NLP. CI uses flake8 and basic checks, not mypy.

## Lesson Learned / Notes

NLTK's review cycle is slower than HF repos — may take 2–4 weeks for a maintainer to look at the PR. The codebase has a mix of Epytext (the Epydoc format from NLTK's early days) and more modern NumPy style. Always check the file being edited for the existing convention rather than assuming project-wide consistency.

---
*Log created: 2026-06-30 | PR: https://github.com/nltk/nltk/pull/3688*
