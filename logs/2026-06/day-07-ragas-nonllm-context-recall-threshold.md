# Day 7 — Contribution to vibrantlabsai/ragas (metrics)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-30 |
| **Repo** | [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) (formerly explodinggradients/ragas) |
| **Package** | `ragas` — `src/ragas/metrics/` |
| **Stars** | ~10,000 |
| **Type** | Real bug fix + unit tests — threshold operator inconsistency |
| **Issue Fixed** | [#2777 — NonLLMContextRecall and NonLLMContextPrecisionWithReference threshold applied inconsistently](https://github.com/vibrantlabsai/ragas/issues/2777) |
| **PR** | [#2798 — fix(metrics): align NonLLMContextRecall threshold to >= for boundary consistency](https://github.com/vibrantlabsai/ragas/pull/2798) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~90% — one-character fix, clearly documented bug, tests included, issue was unassigned for weeks |

---

## Background — Why LangChain PRs Were Closed

Before this contribution, 5 LangChain PRs (Day 2–6) were **auto-closed by a GitHub bot** because:

1. LangChain uses `require_issue_link.yml` — an automated workflow that closes any PR from an external contributor who is NOT assigned to the linked issue.
2. We did not comment on issues first to request assignment.

**Lesson learned:** For LangChain and LangGraph, the correct flow is:
1. Comment on the issue → explain your approach
2. Wait for maintainer to assign you
3. THEN open the PR

We have already commented on LangGraph issue #8130 requesting assignment. Once assigned, we can reopen a PR and it will be accepted.

RAGAS (vibrantlabsai) has **no such bot** — PRs from external contributors are welcome directly.

---

## What Was Done

### The Bug — Two Sibling Metrics with Different Threshold Operators

**File 1:** `src/ragas/metrics/_context_recall.py` — `NonLLMContextRecall._compute_score()`

**File 2:** `src/ragas/metrics/_context_precision.py` — `NonLLMContextPrecisionWithReference`

Both metrics:
- Compare a string-similarity score against a shared `threshold` (default `0.5`)
- Use `NonLLMStringSimilarity` as the distance measure
- Convert float scores to binary (0 or 1) relevance judgements

But they used **different operators**:

```python
# NonLLMContextRecall (WRONG — line 219):
response = [1 if score > self.threshold else 0 for score in verdict_list]
#                    ↑ strict greater-than

# NonLLMContextPrecisionWithReference (CORRECT — line 234):
scores = [1 if score >= self.threshold else 0 for score in scores]
#                    ↑ greater-than-or-equal
```

**The impact:**
```
Context similarity = 0.5 (exactly at threshold)

Precision: 0.5 >= 0.5 → True → RELEVANT ✅
Recall:    0.5 >  0.5 → False → NOT RELEVANT ❌

Same context, same metric, different answer — broken.
```

### The Fix — One Character Change

```diff
- response = [1 if score > self.threshold else 0 for score in verdict_list]
+ response = [1 if score >= self.threshold else 0 for score in verdict_list]
```

### Unit Tests Added

New file: `tests/unit/test_nonllm_context_threshold.py`

Tests cover:
| Test | Purpose |
|------|---------|
| `test_score_at_threshold_is_relevant` | Regression test — the exact bug: score=0.5 must now return 1.0 |
| `test_score_above_threshold_is_relevant` | Score=0.6 → 1.0 (should always have worked) |
| `test_score_below_threshold_is_not_relevant` | Score=0.4 → 0.0 (should always have worked) |
| `test_mixed_scores_with_boundary` | [0.5, 0.3] → 0.5 (1 of 2 relevant) |
| `test_empty_list_returns_nan` | Empty list → nan (existing behavior preserved) |
| `test_custom_threshold_boundary` | threshold=0.7: score=0.7 → 1.0, score=0.69 → 0.0 |
| `test_boundary_score_consistent_between_recall_and_precision` | Cross-metric: both agree at threshold |

---

## Q&A

**Q: Is this a real-world impacting bug?**
A: In practice, floating-point similarity scores landing exactly at `0.5` are rare. But the inconsistency breaks the semantic contract users expect: if precision counts it as relevant, recall must too. Any evaluation framework where `NonLLMContextRecall` and `NonLLMContextPrecisionWithReference` are run together will produce incoherent results at the boundary.

**Q: Why did two operators end up different if the same author wrote both?**
A: `git blame` shows the commits were ~50 seconds apart. Almost certainly a copy-paste where the author typed `>` instead of `>=` in one file. This is extremely common in sibling implementations.

**Q: How is RAGAS different from LangChain for contributions?**
A: RAGAS (vibrantlabsai) is a smaller team (5–10 people) with no assignment-before-PR bot. PRs are reviewed faster (24–48h typically) and welcomed directly. LangChain/LangGraph require you to be assigned to an issue before your PR is accepted.

**Q: What is `NonLLMContextRecall` used for?**
A: It measures how many of the reference contexts were retrieved, using string similarity (no LLM needed). It is one of the core RAGAS metrics for RAG pipeline evaluation. Used in production CI pipelines to detect retrieval regressions.

**Q: What is the `threshold` parameter?**
A: The threshold decides when a similarity score is "good enough" to count a retrieved context as a true positive. Default is 0.5 (using `NonLLMStringSimilarity`). A context with 50% similarity or above = relevant. Below 50% = not relevant.

---

## Files Changed

```
src/ragas/metrics/_context_recall.py
  — _compute_score(): changed `>` to `>=` (1 char change, line 219)

tests/unit/test_nonllm_context_threshold.py
  — NEW: 7 unit tests covering threshold boundary and cross-metric consistency
```

---

## Lesson Learned

**RAGAS is a better starting point for new open source contributors** than LangChain. Reasons:

1. No pre-assignment bot — you can open PRs directly
2. Smaller team = faster review cycles (24–48h vs weeks)
3. Codebase is focused on one domain (RAG evaluation) — easier to navigate
4. Issues are clearly described with reproduction scripts
5. ~10K stars = still impressive on your GitHub profile

The strategy: **use RAGAS to build momentum and get merges, use LangChain for long-term presence after getting assigned to issues.**

For LangChain: We already commented on LangGraph issue #8130 to request assignment. Once a maintainer assigns it, the PR can be reopened and will be accepted automatically by the bot.

---

*Log created: 2026-06-30 | PR: https://github.com/vibrantlabsai/ragas/pull/2798*
