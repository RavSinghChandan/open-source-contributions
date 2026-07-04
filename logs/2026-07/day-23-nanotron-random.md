# Day 23 — Contribution to huggingface/nanotron (random.py)

| Field | Value |
|-------|-------|
| **Date** | 2026-07-04 |
| **Repo** | [huggingface/nanotron](https://github.com/huggingface/nanotron) |
| **Package** | `nanotron` — `src/nanotron/random.py` |
| **Stars** | ~2,600 |
| **Type** | Docs — add missing docstrings |
| **PR** | [#408 — add missing docstrings to set_random_seed, set_random_state and get_synced_random_state](https://github.com/huggingface/nanotron/pull/408) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~65% — nanotron team is active and receptive to doc improvements |

---

## What Was Done

Added Google-style docstrings to 3 public functions in `src/nanotron/random.py`. `set_random_seed` sets all random number generators (Python, NumPy, PyTorch CPU and CUDA) to a given seed for reproducible training. `set_random_state` restores all RNG states from a previously captured `RandomState` snapshot. `get_synced_random_state` broadcasts a random state from rank 0 to all ranks in a process group so that all ranks start with the same RNG state. These are critical functions for reproducible distributed training but had no documentation.

## Files Changed

```
src/nanotron/random.py
  — added docstrings to set_random_seed(), set_random_state(),
    get_synced_random_state()
```

## Why This Repo

Second contribution to nanotron in this challenge (different file, different branch). The random state management module is particularly important to document because reproducibility in distributed training depends on understanding how seeds propagate across ranks. Reused the existing fork with a new branch.

## Lesson Learned / Notes

Distributed training reproducibility requires synchronizing RNG state across all ranks at initialization. `get_synced_random_state` uses `broadcast_object_list` (pickle-based broadcast) rather than `broadcast` because `RandomState` is a dataclass containing a numpy array — not a flat tensor. This is a subtle design decision worth capturing in documentation.

---
*Log created: 2026-07-04 | PR: https://github.com/huggingface/nanotron/pull/408*
