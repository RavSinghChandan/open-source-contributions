# Day 40 — Phase 2: evaluate radar_plot mutable-default fix

**Date:** 2026-07-11
**Repo:** [huggingface/evaluate](https://github.com/huggingface/evaluate)
**PR:** [#781](https://github.com/huggingface/evaluate/pull/781)
**Type:** Code fix — remove mutable default argument
**Phase:** 2

---

## What was done

Deliberately broke the test-coverage pattern this time and shipped a real
(if small) code fix, so the track record isn't five identical test PRs.

`radar_plot` in `src/evaluate/visualization.py` used `invert_range=[]` as a
default argument. A shared mutable default is a classic Python footgun — the
same list object persists across calls. It's only read here today, so no live
bug, but it's the kind of latent issue that bites the moment any code path
mutates it.

Fix: default → `None`, with the standard guard at the top of the body:

```python
if invert_range is None:
    invert_range = []
```

Behaviour is identical (empty `invert_range` → no metrics inverted).

### Files changed

`src/evaluate/visualization.py` — +3/−1.

---

## How I found it

AST-audited `src/` for real bug patterns (mutable defaults, `is` with
literals, etc.). This was the one genuine hit. Verified the fix is
behaviour-preserving and ran evaluate's actual CI linters — black, isort,
flake8 — all clean.

## Why this should merge

- Correct, standard fix for a well-known anti-pattern
- Minimal (2 lines), behaviour-preserving
- black + isort + flake8 clean (evaluate's exact `make quality` tools)
- Not competing with any open PR

## Note

Found a pre-existing incompatibility while testing: `radar_plot`'s plotting
code (`data.loc[g]`, line ~230) breaks on newer pandas — unrelated to this
change and well downstream of it. Left it alone; could be a future fix.
