# Day 31 — Phase 2 begins: huggingface/evaluate bug fix

**Date:** 2026-07-04  
**Repo:** [huggingface/evaluate](https://github.com/huggingface/evaluate)  
**PR:** [#774](https://github.com/huggingface/evaluate/pull/774)  
**Issue fixed:** [#758](https://github.com/huggingface/evaluate/issues/758)  
**Type:** Bug fix — public API improvement  
**Phase:** 2 (first contribution)

---

## What was done

Fixed a silent API gap: `EvaluationModuleError` was defined internally in `module.py` but never exported from `evaluate/__init__.py`. This meant that when a metric's `compute()` method failed, raw exceptions from sklearn or numpy propagated directly to the caller with no evaluate context — and users couldn't catch evaluate-specific errors without catching broad `Exception`.

### Files changed

**`src/evaluate/module.py`**
- Added `EvaluationModuleError(Exception)` class with docstring example
- Wrapped `_compute` call at compute time to catch unexpected exceptions and re-raise as `EvaluationModuleError`, preserving the original cause via `from e`
- Already-raised `EvaluationModuleError` pass through unchanged (re-raise guard)

**`src/evaluate/__init__.py`**
- Added `EvaluationModuleError` to the `from .module import ...` line

### Net change
26 insertions, 2 deletions. No logic changes to how metrics are computed.

---

## Why this repo

- We already have an open Phase 1 PR here ([#771](https://github.com/huggingface/evaluate/pull/771))
- Issue #758 had 0 comments, 0 assignees — clean entry
- Fix is small, surgical, and objectively correct — no style opinions, no ambiguity
- Consistent with how PyTorch, sklearn, and other ML libraries handle error wrapping
- The issue author even wrote out the exact fix — just needed someone to implement it

---

## What makes this a Phase 2 contribution (not Phase 1)

Phase 1 was docstring additions — nice to have, easy to deprioritize.  
This is a bug fix: before this PR, `evaluate.EvaluationModuleError` raised `AttributeError`. That's objectively broken. Maintainers merge broken things when they are fixed.

---

## Lessons learned

- Issues with 0 comments + clear fix description = fastest path to merge
- Always check if the class actually existed before (it didn't — the issue described creating it, not just exporting it)
- Comment on the issue immediately after opening the PR to connect them
- Keep PRs surgical: 2 files, 26 lines, one clear purpose
