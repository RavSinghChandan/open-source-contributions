# 30-Day Open Source Plan — AI Engineer Track

> Strategy: Go DEEP in 6 repos over 30 days. Multiple PRs per repo = you become a KNOWN contributor.
> Target: 1 PR/day. If even 5–8 get merged, your GitHub profile transforms.

---

## The Strategy (Why 6 Repos, Not 30)

```
WRONG approach (scatter):       RIGHT approach (depth):
Day 1  → Repo A (1 fix)         Week 1–2 → LangChain + LangGraph
Day 2  → Repo B (1 fix)                    5–7 PRs, multiple merged
Day 3  → Repo C (1 fix)         Week 3   → RAGAS + Chroma
...                                         4–5 PRs
Day 30 → Repo Z (1 fix)         Week 4   → LiteLLM + HuggingFace
                                            4–5 PRs
Result: nobody knows you         Result: you are a known contributor
```

Recruiters google your name. They see: "This person has 3 merged PRs in LangChain."
That is 100x more impressive than "This person opened 30 one-line PRs across 30 unknown repos."

---

## Week 1–2: LangChain + LangGraph (Days 1–14)

**Why:** You use these daily. You know the codebase. Fastest path to real fixes.

| Day | Target | Type | Issue/Area |
|-----|--------|------|-----------|
| ✅ 1 | awesome-LangGraph | Add projects | PR #76 opened |
| ✅ 2 | langchain/core | Bug fix + tests | PR #38538: operator error message |
| ✅ 3 | langchain/qdrant | Docstring fix | PR #38539: missing await |
| 4 | langchain/core | Docstring improvement | Find a method missing `Returns:` section |
| 5 | langchain | Bug fix | Issue #38203: VectorStore.add_texts silent truncation |
| 6 | langchain | Bug fix | Issue #38138: @tool(infer_schema=False) docstring ignored |
| 7 | REST DAY | Review PR feedback | Check if any PRs got comments → respond within 24h |
| 8 | langgraph | Docstring/example fix | Search langgraph issues for "documentation" |
| 9 | langgraph | Bug fix | Find an open unassigned issue |
| 10 | langgraph | Test addition | Find a function with 0% test coverage |
| 11 | langchain-docs | Doc improvement | Fix a broken link or missing example |
| 12 | langchain-docs | Doc improvement | Add async example where only sync shown |
| 13 | langchain | Bug fix | Find one more open issue |
| 14 | REST DAY | Update tracker | Log all PRs, check merge status |

---

## Week 3: RAGAS + Chroma (Days 15–21)

**Why:** RAGAS is small team (5–10 people) → PRs get reviewed in 24–48h. Chroma is the most popular local vector DB.

| Day | Target | Type | Area |
|-----|--------|------|------|
| 15 | explodinggradients/ragas | Docstring fix | Find missing `Args:` or `Returns:` sections |
| 16 | explodinggradients/ragas | Example addition | Add a complete usage example to a metric class |
| 17 | explodinggradients/ragas | Bug fix | Search open issues for "bug" label |
| 18 | chroma-core/chroma | README fix | Find a broken link or outdated code snippet |
| 19 | chroma-core/chroma | Docstring fix | Find missing docstrings in client methods |
| 20 | chroma-core/chroma | Bug fix | Search open issues for easy fixes |
| 21 | REST DAY | Review PR feedback | Respond to any review comments |

---

## Week 4: LiteLLM + Hugging Face (Days 22–30)

**Why:** LiteLLM is very active and welcoming. HuggingFace on your profile = instant credibility.

| Day | Target | Type | Area |
|-----|--------|------|------|
| 22 | BerriAI/litellm | Provider doc | Add missing provider example |
| 23 | BerriAI/litellm | Bug fix | Search open issues |
| 24 | BerriAI/litellm | Test addition | Find uncovered edge case |
| 25 | huggingface/transformers | Docstring | Small targeted docstring fix |
| 26 | huggingface/huggingface_hub | Bug fix | Find open issue |
| 27 | pydantic/pydantic-ai | Doc fix | New library, many doc gaps |
| 28 | explodinggradients/ragas | New feature test | Add test for edge case |
| 29 | FREE CHOICE | Pick your best | Whichever repo you enjoyed most |
| 30 | REST + CELEBRATE | Write retrospective | Update tracker, count merges, share on LinkedIn |

---

## Daily Ritual (15–30 min max)

```
Morning (10 min):
  1. Open TARGET-REPOS.md or 30-DAY-PLAN.md → find today's repo
  2. Run: gh search issues "bug" --repo <owner/repo> --state open --limit 10
  3. Pick one issue: clear description + small scope + unassigned

Work (varies):
  4. Fork + clone (sparse checkout if large repo)
  5. Fix + test + commit (follow repo conventions from CLAUDE.md or CONTRIBUTING.md)
  6. Push + open PR

Evening (5 min):
  7. Create log file in logs/YYYY-MM/day-XX-reponame.md
  8. Update scoreboard in README.md
  9. Check if any existing PRs got comments → respond
```

---

## What to Do When a PR Gets Comments

This is GOOD news, not bad. Maintainer engagement = they're interested.

```
Response time: within 24 hours (shows you're serious)
Response tone: "Thanks for the feedback. Fixed in [commit hash]."
Never argue about the fix — ask why if confused, but always be open to their way.
```

If a PR gets rejected:
- Say thank you
- Ask what they WOULD accept
- Learn for next time
- Log it in the day's log file

---

## Expected Results After 30 Days

| Scenario | PRs Opened | PRs Merged | Profile Impact |
|----------|------------|------------|----------------|
| Conservative | 25 | 5–8 | "Active contributor to LangChain" |
| Realistic | 28 | 10–15 | "Known contributor in LangChain + LangGraph" |
| Best case | 30 | 18–22 | "Regular contributor, probably gets maintainer invite" |

Even the conservative case — 5 merged PRs in LangChain (140K stars) — is interview gold.

---

## LinkedIn Post Template (Do This After First Merge)

```
🚀 My first open source contribution to @LangChain was merged today!

Fixed a copy-paste bug in Visitor._validate_func where an operator error
message incorrectly said "comparators" instead of "operators".

Small fix. Big learning.

I'm doing 30 days of open source contributions to AI/ML repos.
Day 1 of 30. Let's go.

#OpenSource #LangChain #AIEngineering #Python
```

Post this. Tag LangChain. You'll get reactions. Recruiters notice.

---

*Created: 2026-06-29 | Strategy: Depth over breadth | Target: 30 PRs, 5+ merged*
