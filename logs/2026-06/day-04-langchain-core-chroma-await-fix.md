# Day 4 — Contribution to langchain-ai/langchain (core + chroma)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-29 |
| **Repo** | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| **Packages** | `langchain-core` + `langchain-chroma` (both inside monorepo) |
| **Stars** | 140,482 |
| **Type** | Docstring bug fix — missing `await` in async examples (2 files) |
| **PR** | [#38541 — fix(core,chroma): add missing `await` in `asimilarity_search` docstring examples](https://github.com/langchain-ai/langchain/pull/38541) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~90% — clear, provable, closes same class of bug as PR #38539 |

---

## What Was Done

### The Bug — Same Pattern, Two More Files

After fixing the missing `await` in `langchain-qdrant` (PR #38539), I scanned the entire LangChain monorepo for the same pattern:

```bash
grep -rn "# results = vector_store\.a" libs/ --include="*.py" | grep -v "await"
```

Found two more files with the identical bug:

**File 1: `libs/core/langchain_core/vectorstores/in_memory.py`** — `InMemoryVectorStore` class docstring

**File 2: `libs/partners/chroma/langchain_chroma/vectorstores.py`** — `Chroma` class docstring

Both had this line in their "Async:" usage section:

```python
# WRONG — returns a coroutine, not a list[Document]:
# results = vector_store.asimilarity_search(query="thud", k=1)

# CORRECT:
# results = await vector_store.asimilarity_search(query="thud", k=1)
```

Every other async call in both docstrings correctly used `await`. This was the only inconsistent line in each.

### The Fix

```diff
# in_memory.py line 135:
- # results = vector_store.asimilarity_search(query="thud", k=1)
+ # results = await vector_store.asimilarity_search(query="thud", k=1)

# chroma/vectorstores.py line 274:
- # results = vector_store.asimilarity_search(query="thud",k=1)
+ # results = await vector_store.asimilarity_search(query="thud", k=1)
```

Also fixed spacing after comma in the Chroma file (`k=1` → `k=1`) for style consistency.

---

## Q&A

**Q: Why open a separate PR instead of including this in PR #38539?**
A: Each PR in a large monorepo should be focused and reviewable independently. PR #38539 fixed qdrant. This PR fixes core + chroma. Reviewers can approve each independently, and if one needs changes the other is not blocked.

**Q: How did you find these two additional files?**
A: After fixing the first instance, ran a grep scan across all partner and core vectorstore files for the exact pattern `# results = vector_store.a` without `await`. This is systematic bug-class elimination — fix one, scan for all siblings.

**Q: Why does `InMemoryVectorStore` have this bug if it's in `langchain-core`?**
A: Core packages have many docstring examples written at different times by different contributors. No automated check enforces `await` in commented examples. This is a known category of documentation debt.

**Q: What is the user impact?**
A: A developer copies the async example, runs it, gets: `TypeError: 'coroutine' object is not iterable` or the result is a coroutine object printed to console. They spend 10–30 minutes debugging. One `await` would have prevented all of it.

---

## Files Changed

```
libs/core/langchain_core/vectorstores/in_memory.py      — line 135: added await
libs/partners/chroma/langchain_chroma/vectorstores.py   — line 274: added await + fixed spacing
```

---

## Lesson Learned

When you fix a bug in one file, always ask: **"Is this the same bug in other files?"**
Run a grep for the exact pattern. In open source, documentation bugs tend to be copy-pasted across multiple similar files (all vector stores follow the same docstring template). One grep → multiple PRs.

---

*Log created: 2026-06-29*
