# Day 6 — Contribution to langchain-ai/langchain (core + text-splitters)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-29 |
| **Repo** | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| **Packages** | `langchain-core` + `langchain-text-splitters` |
| **Stars** | 140,482 |
| **Type** | Two real bug fixes — logic error + missing feature |
| **Issue Fixed** | [#36750 — Feature/Bug: Implement missing Language.PERL separators and fix InMemoryCache maxsize update bug](https://github.com/langchain-ai/langchain/issues/36750) |
| **PR** | [#38543 — fix(core,text-splitters): fix `InMemoryCache` eviction on update and add `Language.PERL` separators](https://github.com/langchain-ai/langchain/pull/38543) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~80% — two real bugs, both reproducible, clear fixes |

---

## What Was Done

### Bug 1 — `InMemoryCache` Evicts on Update (Logic Error)

**File:** `libs/core/langchain_core/caches.py`

**The Bug:**
`InMemoryCache.update()` always evicts the oldest entry when the cache is full — even if the caller is just updating a key that ALREADY EXISTS in the cache.

```python
# BUGGY CODE:
def update(self, prompt, llm_string, return_val):
    if self._maxsize is not None and len(self._cache) == self._maxsize:
        del self._cache[next(iter(self._cache))]   # ← evicts even on re-update!
    self._cache[prompt, llm_string] = return_val
```

**What happens:**
```python
cache = InMemoryCache(maxsize=2)
cache.update("p1", "llm1", "val1")   # cache: {p1: val1}
cache.update("p2", "llm2", "val2")   # cache: {p1: val1, p2: val2}  ← full

# Now update an EXISTING key (p2):
cache.update("p2", "llm2", "val2_new")
# EXPECTED: {p1: val1, p2: val2_new}  ← p1 should survive
# ACTUAL:   {p2: val2_new}            ← p1 was wrongly evicted!
```

**The Fix:**
```python
# FIXED CODE:
def update(self, prompt, llm_string, return_val):
    key = (prompt, llm_string)
    if self._maxsize is not None and key not in self._cache and len(self._cache) == self._maxsize:
        del self._cache[next(iter(self._cache))]   # only evict for NEW keys
    self._cache[key] = return_val
```

**Why this matters:** Caches are used to avoid expensive LLM API calls. If an existing cache entry causes another entry to be evicted, the cache becomes smaller than intended. A maxsize=100 cache could effectively behave as maxsize=50 or less under heavy re-update traffic.

---

### Bug 2 — `Language.PERL` Not Implemented (Missing Feature)

**File:** `libs/text-splitters/langchain_text_splitters/character.py`

**The Bug:**
`Language.PERL` exists in the `Language` enum (line 406) but `get_separators_for_language()` has no `if language == Language.PERL:` branch. Every call raises:

```
ValueError: Language Language.PERL is not implemented yet!
```

This is an incomplete implementation — the enum value was added but the corresponding separator logic was never written.

**The Fix — Added PERL separators:**
```python
if language == Language.PERL:
    return [
        # Split along subroutine definitions
        "\nsub ",
        # Split along package declarations
        "\npackage ",
        # Split along use/require statements
        "\nuse ",
        "\nrequire ",
        # Split along eval blocks
        "\neval {",
        "\neval \"",
        # Split along control flow
        "\nif (",
        "\nelsif (",
        "\nelse {",
        "\nunless (",
        "\nwhile (",
        "\nfor (",
        "\nforeach (",
        "\nuntil (",
        "\ndo {",
        # Split along regular expression operations
        "\n=~ s/",
        "\n=~ m/",
        # Normal line splitting
        "\n\n",
        "\n",
        " ",
        "",
    ]
```

**Why these separators?**
| Separator | Perl construct |
|-----------|---------------|
| `\nsub ` | Subroutine definition — most important split boundary |
| `\npackage ` | Package/namespace declaration |
| `\nuse ` / `\nrequire ` | Module imports |
| `\neval {` / `\neval "` | Runtime code evaluation blocks |
| `\nif/elsif/else/unless` | Conditional blocks |
| `\nwhile/for/foreach/until/do` | Loop constructs |
| `\n=~ s/` / `\n=~ m/` | Regex substitution / match operations |
| `\n\n` / `\n` / ` ` / `` | Fallback progressively smaller splits |

---

## Q&A

**Q: Why are two unrelated bugs in one PR?**
A: The issue reporter grouped them in one issue (#36750). The convention in LangChain is to close issues with PRs. Since both fixes are in separate files with no overlap, they can be reviewed independently within one PR and both close one issue cleanly.

**Q: What is `InMemoryCache` used for?**
A: It is LangChain's default in-memory LLM response cache. When you call an LLM with the same prompt + configuration twice, the second call hits the cache instead of making a real API call. This saves money (no tokens charged) and time (instant response). A buggy eviction policy means cache entries are lost unnecessarily → more API calls, more cost.

**Q: How did you design the PERL separators?**
A: Followed the same pattern as other languages in the file (PHP, Ruby, etc.): start with the most structural boundaries (function/subroutine definitions, package declarations), then imports, then blocks, then control flow, then fallback to lines and characters. Perl's most distinctive constructs are `sub` (functions), `package` (namespaces), and `=~` (regex operations).

**Q: Is PERL still widely used?**
A: Yes — in bioinformatics, systems administration, legacy banking and telecom code, and CPAN-based tooling. It is still a top-20 language by usage. LangChain RAG pipelines applied to Perl codebases need this to work correctly.

**Q: What is the hardest part of this fix?**
A: The PERL separators required genuine knowledge of Perl syntax. Getting them right means the `RecursiveCharacterTextSplitter` will cut Perl code at meaningful boundaries (between subroutines, packages) rather than in the middle of a line — which is important for RAG pipelines indexing code.

---

## Files Changed

```
libs/core/langchain_core/caches.py
  — update() method: added key-existence check before eviction (3 lines changed)

libs/text-splitters/langchain_text_splitters/character.py
  — get_separators_for_language(): added Language.PERL branch (+27 lines)
```

---

## Lesson Learned

**Real bugs are better than docstring fixes** from a contribution quality standpoint. A docstring fix shows you can read code. A logic bug fix shows you can REASON about code.

The `InMemoryCache` bug is a classic off-by-one-condition error: the guard should have been `key not in self._cache AND len == maxsize` but it was only `len == maxsize`. These are the bugs that feel satisfying to fix because they are provably wrong, the fix is clean, and you can describe the exact scenario that breaks.

For finding these: always look at issues with reproduction scripts. If someone provides a script that shows wrong behaviour, the fix is usually nearby. Issue #36750 had a perfect reproduction script — that is your roadmap to the fix.

---

*Log created: 2026-06-29*
