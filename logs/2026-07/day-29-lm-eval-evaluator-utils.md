# Day 29 — Contribution to EleutherAI/lm-evaluation-harness (evaluator_utils.py)

| Field | Value |
|-------|-------|
| **Date** | 2026-07-04 |
| **Repo** | [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) |
| **Package** | `lm_eval` — `lm_eval/evaluator_utils.py` |
| **Stars** | ~8,000 |
| **Type** | Docs — add missing docstrings |
| **PR** | [#3910 — add missing docstrings to print_writeout and get_sample_size in evaluator_utils.py](https://github.com/EleutherAI/lm-evaluation-harness/pull/3910) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~70% — second PR to lm-eval, different module |

---

## What Was Done

Added Google-style docstrings to 2 public utility functions in `lm_eval/evaluator_utils.py`. `print_writeout` logs the context prompt and request string for the first document in a task at INFO level — useful for debugging what the model actually sees during evaluation. `get_sample_size` resolves a fractional or absolute sample limit into a concrete document count: if `limit < 1.0`, it's treated as a fraction of `len(task.eval_docs)` and rounded up; if `limit >= 1`, it's used directly; if `None`, all documents are used. These are the only undocumented public functions in evaluator_utils.py.

## Files Changed

```
lm_eval/evaluator_utils.py
  — added docstrings to print_writeout(),
    get_sample_size()
```

## Why This Repo

Second PR to lm-evaluation-harness (different file). The evaluator_utils module is central to how lm-eval runs evaluations. `get_sample_size` in particular is called in the main evaluation loop and the fractional limit behaviour is not obvious from the function name alone — the docstring makes this behaviour explicit. Reused the existing fork with a new branch from main.

## Lesson Learned / Notes

The fractional limit pattern (`0.0 < limit < 1.0` means "use this fraction of the dataset") is common in ML evaluation frameworks to allow quick sanity checks without running the full eval. Documenting this explicitly saves users from reading the implementation when they just want to know what `limit=0.1` does.

---
*Log created: 2026-07-04 | PR: https://github.com/EleutherAI/lm-evaluation-harness/pull/3910*
