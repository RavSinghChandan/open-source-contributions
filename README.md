# Open Source Contributions — Chandan Kumar (RavSinghChandan)

> **Goal:** 1 open source contribution per day. 30 days. At least 5 merged PRs.
> **Domain:** AI Engineering — LangChain, LangGraph, Hugging Face, and AI tooling ecosystem
> **Why:** Build a public track record as a serious AI open source contributor

---

## Contribution Scoreboard

| Day | Date | Repo | Type | PR Link | Status |
|-----|------|------|------|---------|--------|
| 1 | 2026-06-29 | [vonzosten/awesome-LangGraph](https://github.com/vonzosten/awesome-LangGraph) | Add 2 community projects | [PR #76](https://github.com/vonzosten/awesome-LangGraph/pull/76) | ⏳ Open |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Bug fix + unit tests — `Visitor._validate_func` error message | [PR #38538](https://github.com/langchain-ai/langchain/pull/38538) | 🔄 Closed → commented on [issue #36701](https://github.com/langchain-ai/langchain/issues/36701) for assignment |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Docstring fix — missing `await` in qdrant + core + chroma | [PR #38539](https://github.com/langchain-ai/langchain/pull/38539) | 🔄 Closed → commented on [issue #37058](https://github.com/langchain-ai/langchain/issues/37058) + [#38560](https://github.com/langchain-ai/langchain/issues/38560) for assignment |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Docstring — clarify JSON schema `title` requirement | [PR #38542](https://github.com/langchain-ai/langchain/pull/38542) | 🔄 Closed → commented on [issue #34662](https://github.com/langchain-ai/langchain/issues/34662) for assignment |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Bug fix — `InMemoryCache` eviction + `Language.PERL` separators | [PR #38543](https://github.com/langchain-ai/langchain/pull/38543) | 🔄 Closed → commented on [issue #36750](https://github.com/langchain-ai/langchain/issues/36750) for assignment |
| 2 | 2026-06-30 | [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) | Bug fix — `NonLLMContextRecall` threshold `>` → `>=` + unit tests | [PR #2798](https://github.com/vibrantlabsai/ragas/pull/2798) | ⏳ Open |

---

## LangChain — Issues Commented, Awaiting Assignment

> PRs were closed by bot on Day 1 because we didn't follow the rule. Fixed now — commented on every issue requesting assignment. PRs will be reopened the moment we are assigned.

| Issue | Fix | Merge chance | Status |
|-------|-----|-------------|--------|
| [#36701](https://github.com/langchain-ai/langchain/issues/36701) | Bug fix: `comparators` → `operators` in `Visitor._validate_func` error message + 4 unit tests | ~90% | ⏳ Awaiting assignment |
| [#37058](https://github.com/langchain-ai/langchain/issues/37058) | Docstring: missing `await` in qdrant `asimilarity_search` example | ~95% | ⏳ Awaiting assignment |
| [#38560](https://github.com/langchain-ai/langchain/issues/38560) | Docstring: missing `await` in InMemoryVectorStore + Chroma examples | ~95% | ⏳ Awaiting assignment |
| [#34662](https://github.com/langchain-ai/langchain/issues/34662) | Docstring: clarify `title` is required key in JSON schema dicts | ~85% | ⏳ Awaiting assignment |
| [#36750](https://github.com/langchain-ai/langchain/issues/36750) | Bug fix: `InMemoryCache` eviction guard + add `Language.PERL` separators | ~80% | ⏳ Awaiting assignment |

---

## LangGraph — Issues Filed & Awaiting Assignment

> These are ready to become PRs the moment a maintainer assigns us. All fixes are documentation/typo only — zero code logic changes.

| Issue | Repo | Fix | Merge chance | Status |
|-------|------|-----|-------------|--------|
| [#8130](https://github.com/langchain-ai/langgraph/issues/8130) | langchain-ai/langgraph | Typo: `GraphRecusionError` → `GraphRecursionError` in `create_react_agent` docstring | ~95% | ⏳ Awaiting assignment |
| [#8226](https://github.com/langchain-ai/langgraph/issues/8226) | langchain-ai/langgraph | Grammar: `ToolMessage for each tool_calls` → `tool_call` in mermaid diagram | ~95% | ⏳ Awaiting assignment |
| [#8227](https://github.com/langchain-ai/langgraph/issues/8227) | langchain-ai/langgraph | Docs: `context_schema` param has no description — add explanation + usage hint | ~85% | ⏳ Awaiting assignment |
| [#8228](https://github.com/langchain-ai/langgraph/issues/8228) | langchain-ai/langgraph | Wrong import: `from langchain.tools import ToolNode` → `from langgraph.prebuilt import ToolNode` (2 places) | ~90% | ⏳ Awaiting assignment |

---

## Stats

- **Total PRs opened:** 7 (6 on Day 1, 1 on Day 2)
- **Total PRs merged:** 0 (check back in 24–72h)
- **PRs closed by bot:** 5 (LangChain requires issue assignment before PR — lesson learned on Day 1)
- **Active open PRs:** 2 (awesome-LangGraph #76, RAGAS #2798)
- **LangChain issues awaiting assignment:** 5 (fixes ready, PRs will open the moment assigned)
- **LangGraph issues awaiting assignment:** 4 (fixes ready, PRs will open the moment assigned)
- **Current day:** Day 2
- **Target repos:** awesome-LangGraph ✅, LangChain (need assignment), RAGAS ✅, LangGraph (need assignment)

---

## Folder Structure

```
open-source-contributions/
├── README.md              ← This file — scoreboard + overview
├── logs/                  ← One file per contribution with full Q&A
│   └── 2026-06/
│       ├── day-01-awesome-langgraph.md           ← PR #76
│       ├── day-01-langchain-typo.md              ← PR #38538
│       ├── day-01-langchain-qdrant-await-fix.md  ← PR #38539
│       ├── day-01-langchain-core-chroma-await.md ← PR #38541
│       ├── day-01-langchain-json-schema-title.md ← PR #38542
│       ├── day-01-langchain-inmemorycache-perl.md ← PR #38543
│       └── day-02-ragas-nonllm-threshold.md      ← PR #2798
└── targets/
    ├── TARGET-REPOS.md    ← Pre-researched repos ready for contribution
    └── 30-DAY-PLAN.md     ← Full 30-day calendar with daily targets
```

---

## How to Use This Repo

**Before each contribution:**
1. Open `targets/TARGET-REPOS.md` → pick the day's repo
2. Follow the contribution steps in that file

**After each contribution:**
1. Add a row to the scoreboard table above
2. Create a log file in `logs/YYYY-MM/day-XX-reponame.md`
3. Update the Stats section

---

## The Strategy (Why These PRs Get Merged)

1. **awesome-* repos** — curated lists, always welcoming new entries. Near 100% merge rate.
2. **Typo/doc fixes in large repos** — clear value, no controversy, merged quickly.
3. **Missing docstrings** — maintainers love these. Easy to write, high value.
4. **Test coverage** — adding tests to existing features. Always welcome.
5. **Real bug fixes** — highest impact, takes more effort, but very rewarding.

---

*Started: 2026-06-29 | Maintained by Chandan Kumar (RavSinghChandan)*
