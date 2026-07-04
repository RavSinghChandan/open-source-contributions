# Day 30 — Contribution to google-deepmind/optax (linear_algebra.py)

| Field | Value |
|-------|-------|
| **Date** | 2026-07-04 |
| **Repo** | [google-deepmind/optax](https://github.com/google-deepmind/optax) |
| **Package** | `optax` — `optax/_src/linear_algebra.py` |
| **Stars** | ~4,100 |
| **Type** | Docs — add missing docstring |
| **PR** | [#1721 — add missing docstring to get_spectral_radius_upper_bound in linear_algebra.py](https://github.com/google-deepmind/optax/pull/1721) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~65% — second PR to optax, different file |

---

## What Was Done

Added a Google-style docstring to `get_spectral_radius_upper_bound` in `optax/_src/linear_algebra.py`. This function computes `min(‖matrix‖_F, ‖matrix‖_1)` as a tight upper bound on the spectral radius of a square matrix. It is used internally by `nnls` (non-negative least squares) to bound the Lipschitz constant of the quadratic objective. The function had only an inline comment (`# Get an upper bound on the spectral radius of a matrix`) but no docstring — replacing it with a proper docstring makes it show up in generated API documentation and IDE tooltips. Matched the Google-style docstrings used throughout `linear_algebra.py` and the rest of the `_src` package.

## Files Changed

```
optax/_src/linear_algebra.py
  — added docstring to get_spectral_radius_upper_bound()
```

## Why This Repo

Second PR to optax (different file). `get_spectral_radius_upper_bound` is a mathematically meaningful function used as the Lipschitz constant estimator in `nnls` — understanding why min(Frobenius, 1-norm) is a valid upper bound on the spectral radius requires a brief explanation that the docstring provides. Reused the existing fork with a new branch from main.

## Lesson Learned / Notes

The Frobenius norm and the 1-norm (max column sum) are both valid upper bounds on the largest singular value (and hence spectral radius) of a real matrix. Their minimum gives a tighter estimate. The `matrix.size != 0` guard for the 1-norm exists because `jnp.linalg.matrix_norm(matrix, ord=1)` has a known bug on empty matrices tracked at jax-ml/jax#26555 — worth capturing this context in documentation.

---
*Log created: 2026-07-04 | PR: https://github.com/google-deepmind/optax/pull/1721*
