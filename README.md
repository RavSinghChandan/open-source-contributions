# Open Source Contributions — Chandan Kumar (RavSinghChandan)

> **Goal:** Build a publicly visible track record as a serious AI Engineer through real open source contributions — merged PRs, issue discussions, and community presence in the AI/ML ecosystem.
> **Target companies:** Google DeepMind · Anthropic · OpenAI · Microsoft · HuggingFace · Cohere · Mistral

---

## The 5-Phase Roadmap — From Contributor to Core Maintainer

This is not just a PR challenge. This is a career strategy.
Each phase builds on the last. By Phase 5, your GitHub profile tells a story that gets you interviews at top AI companies.

```
Phase 1 → Learn the workflow, build presence        [DONE ✅]
Phase 2 → Get real merges, build reputation         [IN PROGRESS 🔄]
Phase 3 → Fix real bugs, become trusted             [NEXT]
Phase 4 → Own features, get credited in changelogs  [GOAL]
Phase 5 → Core contributor, public recognition      [VISION]
```

---

## Phase 1 — Foundation: Learn the Workflow (Days 1–30) ✅ COMPLETE

**Goal:** Understand how open source works. Learn repo rules, CI systems, PR etiquette, and docstring styles across 15+ repos. Build the habit of daily contribution.

**Strategy used:** Add missing docstrings to public utility functions in ruff-only repos.

**What we learned:**
- Large HuggingFace repos (smolagents, evaluate, accelerate, datasets, optimum) have slow review cycles for doc-only PRs
- Repos with strict rules (wandb, LangChain) require different approach — file issues first, wait for assignment
- click maintainers close tiny PRs silently — need more substance
- Joblib, lighteval, nanotron, stanza, optax have active maintainers who review quickly

**Phase 1 result:** 35 PRs opened · 0 merged (yet) · 28 active open · 30 log files · 15 repos touched

**Phase 1 PRs:**

| Day | Date | Repo | Type | PR | Status |
|-----|------|------|------|----|--------|
| 1 | 2026-06-29 | [vonzosten/awesome-LangGraph](https://github.com/vonzosten/awesome-LangGraph) | Add 2 community projects | [#76](https://github.com/vonzosten/awesome-LangGraph/pull/76) | ⏳ Open |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Bug fix — `Visitor._validate_func` error message | [#38538](https://github.com/langchain-ai/langchain/pull/38538) | 🔄 Closed → awaiting assignment on [#36701](https://github.com/langchain-ai/langchain/issues/36701) |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Docstring — missing `await` in qdrant + chroma | [#38539](https://github.com/langchain-ai/langchain/pull/38539) | 🔄 Closed → awaiting [#37058](https://github.com/langchain-ai/langchain/issues/37058) |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Docstring — clarify JSON schema `title` requirement | [#38542](https://github.com/langchain-ai/langchain/pull/38542) | 🔄 Closed → awaiting [#34662](https://github.com/langchain-ai/langchain/issues/34662) |
| 1 | 2026-06-29 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Bug fix — `InMemoryCache` eviction + `Language.PERL` | [#38543](https://github.com/langchain-ai/langchain/pull/38543) | 🔄 Closed → awaiting [#36750](https://github.com/langchain-ai/langchain/issues/36750) |
| 2 | 2026-06-30 | [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) | Bug fix — `NonLLMContextRecall` threshold `>` → `>=` + tests | [#2798](https://github.com/vibrantlabsai/ragas/pull/2798) | ⏳ Open |
| 3 | 2026-06-30 | [huggingface/smolagents](https://github.com/huggingface/smolagents) | Docs — 5 missing docstrings in `utils.py` | [#2438](https://github.com/huggingface/smolagents/pull/2438) | ⏳ Open |
| 4 | 2026-06-30 | [huggingface/evaluate](https://github.com/huggingface/evaluate) | Docs — 5 missing docstrings in `naming.py` | [#771](https://github.com/huggingface/evaluate/pull/771) | ⏳ Open |
| 5 | 2026-06-30 | [huggingface/accelerate](https://github.com/huggingface/accelerate) | Docs — 3 missing docstrings in `operations.py` | [#4095](https://github.com/huggingface/accelerate/pull/4095) | ⏳ Open |
| 6 | 2026-06-30 | [huggingface/datasets](https://github.com/huggingface/datasets) | Docs — 5 missing docstrings in `py_utils.py` | [#8294](https://github.com/huggingface/datasets/pull/8294) | ⏳ Open |
| 7 | 2026-06-30 | [huggingface/optimum](https://github.com/huggingface/optimum) | Docs — 5 missing docstrings in `testing_utils.py` + `save_utils.py` | [#2454](https://github.com/huggingface/optimum/pull/2454) | ⏳ Open |
| 8 | 2026-06-30 | [UKPLab/sentence-transformers](https://github.com/UKPLab/sentence-transformers) | Docs — `Dense` methods + `to_scipy_coo` | [#3843](https://github.com/UKPLab/sentence-transformers/pull/3843) | ⏳ Open |
| 9 | 2026-06-30 | [huggingface/safetensors](https://github.com/huggingface/safetensors) | Docs — `storage_ptr`, `storage_size`, `rename`, `check_file_size` | [#806](https://github.com/huggingface/safetensors/pull/806) | ⏳ Open |
| 10 | 2026-06-30 | [nltk/nltk](https://github.com/nltk/nltk) | Docs — 5 missing docstrings in `compat.py` + `decorators.py` | [#3688](https://github.com/nltk/nltk/pull/3688) | ⏳ Open |
| 11 | 2026-06-30 | [wandb/wandb](https://github.com/wandb/wandb) | Docs — 7 env helper functions in `env.py` | [#12133](https://github.com/wandb/wandb/pull/12133) | 🚫 Closed — anti-AI-PR policy |
| 12 | 2026-07-01 | [explosion/spaCy](https://github.com/explosion/spaCy) | Docs — 6 functions in `util.py` + `cli/_util.py` | [#13987](https://github.com/explosion/spaCy/pull/13987) | ⏳ Open |
| 13 | 2026-07-02 | [pallets/click](https://github.com/pallets/click) | Docs — `measure_table` + `iter_rows` in `formatting.py` | [#3659](https://github.com/pallets/click/pull/3659) | 🚫 Closed — too minor |
| 14 | 2026-07-03 | [joblib/joblib](https://github.com/joblib/joblib) | Docs — `format_time`, `short_format_time`, `pformat` | [#1811](https://github.com/joblib/joblib/pull/1811) | ⏳ Open |
| 15 | 2026-07-03 | [huggingface/lighteval](https://github.com/huggingface/lighteval) | Docs — 3 functions in `utils/imports.py` | [#1282](https://github.com/huggingface/lighteval/pull/1282) | ⏳ Open |
| 16–30 | 2026-07-04 | nanotron · paramiko · lm-eval-harness · numba · stanza · optax | Docs — missing docstrings across utility files | [#407](https://github.com/huggingface/nanotron/pull/407) [#408](https://github.com/huggingface/nanotron/pull/408) [#409](https://github.com/huggingface/nanotron/pull/409) [#2641](https://github.com/paramiko/paramiko/pull/2641) [#3909](https://github.com/EleutherAI/lm-evaluation-harness/pull/3909) [#3910](https://github.com/EleutherAI/lm-evaluation-harness/pull/3910) [#10686](https://github.com/numba/numba/pull/10686) [#1634](https://github.com/stanfordnlp/stanza/pull/1634) [#1635](https://github.com/stanfordnlp/stanza/pull/1635) [#1636](https://github.com/stanfordnlp/stanza/pull/1636) [#1720](https://github.com/google-deepmind/optax/pull/1720) [#1721](https://github.com/google-deepmind/optax/pull/1721) | ⏳ Open |

---

## Phase 2 — Credibility: Get Real Merges (Days 31–60) 🔄 IN PROGRESS

**Goal:** At least 10 merged PRs. Shift from docstrings to higher-value contributions: fixing broken examples in docs, adding missing type annotations, writing tests for untested public functions.

**Why this phase matters:** A GitHub profile with 0 merges looks like spam to recruiters. 10 merges across well-known AI repos (HuggingFace, EleutherAI, StanfordNLP) signals you are a real contributor, not just a PR opener.

**Strategy shift — 3 types of contributions that get merged fast:**

### Type A — Fix broken code examples in docstrings (merge rate ~90%)
Many repos have docstring examples that are outdated or actually fail if you run them. These get merged same-day because they are objectively wrong, not a style opinion.
- How to find: `grep -r ">>>" src/` then copy-paste examples into Python and run them
- Target repos: ragas, smolagents, sentence-transformers, lm-evaluation-harness

### Type B — Add tests for untested public functions (merge rate ~80%)
Find public functions with 0 test coverage. Write simple unit tests. Maintainers almost never reject tests.
- How to find: `pytest --cov=src --cov-report=term-missing` → look for 0% covered public functions
- Target repos: lighteval, nanotron, optax, stanza

### Type C — Fix open "good first issue" bugs (merge rate ~85%)
Every active repo has a `good first issue` label. These are bugs the maintainer has already accepted — they just need someone to fix them.
- How to find: `gh issue list --repo OWNER/REPO --label "good first issue" --state open`
- Target repos: ragas, smolagents, lm-evaluation-harness, sentence-transformers

**Phase 2 target repos (pre-verified safe):**

| Repo | Why | Focus |
|------|-----|-------|
| [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) | Small team, fast reviews, AI domain | Good first issues + broken examples |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | HF flagship agentic lib, active | Broken examples in docstrings |
| [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | THE benchmark suite, high visibility | Tests + good first issues |
| [stanfordnlp/stanza](https://github.com/stanfordnlp/stanza) | Active NLP team, responsive | Tests for untested functions |
| [google-deepmind/optax](https://github.com/google-deepmind/optax) | DeepMind repo, high profile | Broken examples |
| [huggingface/lighteval](https://github.com/huggingface/lighteval) | Eval framework, small team | Tests + good first issues |
| [joblib/joblib](https://github.com/joblib/joblib) | scikit-learn ecosystem, very active | Good first issues |

**Phase 2 daily workflow:**
1. Morning: check if any Phase 1 PRs got merged or commented → respond within 1 hour
2. Pick today's contribution type (A, B, or C) from the list above
3. Do the contribution — must be more substantial than Phase 1 (aim for 20+ lines changed)
4. Open PR, update log, commit

**Phase 2 scoreboard:**

| Day | Date | Repo | Type | PR | Status |
|-----|------|------|------|----|--------|
| 31 | 2026-07-04 | [huggingface/evaluate](https://github.com/huggingface/evaluate) | Bug fix — export `EvaluationModuleError`, wrap `_compute` failures (fixes #758) | [#774](https://github.com/huggingface/evaluate/pull/774) | ⏳ Open |
| 32 | 2026-07-05 | [huggingface/smolagents](https://github.com/huggingface/smolagents) | Bug fix — replace `assert` with explicit check in `_validate_final_answer` + test (fixes #2456) | [#2469](https://github.com/huggingface/smolagents/pull/2469) | ⏳ Open |
| 33 | 2026-07-06 | [joblib/joblib](https://github.com/joblib/joblib) | Bug fix — accept any `os.PathLike` in `dump()` + `load()`, not just `pathlib.Path` + test (fixes #1784) | [#1812](https://github.com/joblib/joblib/pull/1812) | ⏳ Open |
| 34 | 2026-07-11 | [joblib/joblib](https://github.com/joblib/joblib) | Review response — addressed maintainer comments on #1811 (docstring spacing) and #1812 (dropped logger.py overlap, `os.PathLike` docstrings) | [#1811](https://github.com/joblib/joblib/pull/1811) · [#1812](https://github.com/joblib/joblib/pull/1812) | ⏳ Open |
| 35 | 2026-07-11 | [nltk/nltk](https://github.com/nltk/nltk) | Test coverage — regression tests for untested `transitive_closure` in `util.py` (chain, reflexive, cycle, empty, no-mutation) | [#3703](https://github.com/nltk/nltk/pull/3703) | ⏳ Open |
| 36 | 2026-07-11 | [UKPLab/sentence-transformers](https://github.com/UKPLab/sentence-transformers) | Test coverage — regression tests for untested `append_to_last_row` in `util/misc.py` (append, multi-value, header-only + empty no-op) | [#3855](https://github.com/UKPLab/sentence-transformers/pull/3855) | ⏳ Open |
| 37 | 2026-07-11 | [joblib/joblib](https://github.com/joblib/joblib) | Test coverage — regression tests for untested `format_time` + `short_format_time` in `logger.py` (both branches, cross-platform via `_squeeze_time`) | [#1814](https://github.com/joblib/joblib/pull/1814) | ⏳ Open |

---

## Phase 3 — Trust: Fix Real Bugs (Days 61–90)

**Goal:** 5+ bug fix PRs merged in AI repos. Start appearing in changelogs. Get maintainers to know your name.

**Why this phase matters:** Recruiters at Anthropic, Google DeepMind, and HuggingFace look at what you fixed, not just what you documented. A merged bug fix in `lm-evaluation-harness` or `ragas` says "this person understands the codebase deeply."

**Strategy:**
- Spend 2–3 days per week reading issues carefully in 3–4 repos
- Reproduce bugs locally before claiming them
- Write a clear fix + regression test
- Comment on the issue explaining your approach before opening a PR
- Build a relationship with 2–3 maintainers through issue discussions

**Target contribution types:**
- Fix metric calculation bugs in RAG evaluation libraries (ragas, lighteval)
- Fix edge cases in tokenization and data loading (datasets, stanza)
- Fix incorrect behavior in distributed training utilities (nanotron, accelerate)
- Add missing error handling in agent frameworks (smolagents, lm-evaluation-harness)

**Phase 3 target repos:**

| Repo | Domain relevance | Difficulty |
|------|-----------------|------------|
| vibrantlabsai/ragas | RAG evaluation — core AI skill | Medium |
| huggingface/smolagents | AI agents — hot topic | Medium |
| EleutherAI/lm-evaluation-harness | LLM benchmarking | Medium-Hard |
| huggingface/lighteval | LLM evaluation | Medium |
| huggingface/datasets | Data loading | Medium |

**Phase 3 goal:** 5 merged bug fixes · First changelog entry · Known by name to at least 2 maintainers

---

## Phase 4 — Ownership: Build Features (Days 91–120)

**Goal:** Own a small but complete feature end-to-end in 1–2 repos. Get credited in release notes.

**Why this phase matters:** "Contributed feature X to repo Y" on a CV beats "fixed 50 docstrings." By Phase 4, you want 1–2 sentences in a release changelog that say your name.

**Strategy:**
- Pick 1–2 repos where you are already known from Phase 2–3 PRs
- Find a well-scoped feature request (not too large, clearly wanted)
- Discuss approach on the issue before writing code
- Implement, write tests, update docs — complete package
- Be responsive to review feedback — iterate fast

**Target feature ideas (AI-domain, manageable scope):**
- Add a new metric to `ragas` (e.g. answer completeness with configurable LLM)
- Add a new task/benchmark to `lm-evaluation-harness` (e.g. a Hindi reasoning dataset)
- Add async support to a sync-only function in `smolagents`
- Add a new callback type to `lighteval` for custom logging
- Improve streaming output handling in `nanotron`

**Phase 4 goal:** 1–2 features merged · Named in changelog · GitHub profile shows "contributed to X, Y"

---

## Phase 5 — Recognition: Core Contributor (Days 121–150)

**Goal:** Become a recognized contributor in 1 repo. Get invited to review others' PRs. Speak or write about your contributions.

**Why this phase matters:** Top AI companies (Anthropic, Google DeepMind, HuggingFace) hire people who are already part of the community. If a hiring manager recognizes your GitHub handle from a repo they use daily, the interview starts differently.

**Strategy:**
- Focus entirely on 1–2 repos where you have the most merged PRs
- Start reviewing other people's PRs — leave thoughtful, constructive comments
- Write a blog post or LinkedIn article: "What I learned from contributing to [repo]" — link your PRs
- File issues proactively — not just fixes, but ideas for improvement
- Apply for maintainer status if the repo has a formal process

**Phase 5 goal:**
- Invited to review PRs in at least 1 repo
- Written 1 public post about your open source journey
- GitHub profile: 20+ merged PRs across 5+ AI repos
- At least 1 maintainer who can vouch for you in a reference

---

## What This Does for Your Career

As an AI Engineer targeting top companies, here is what each phase adds to your story:

| Phase | What a recruiter sees | What it signals |
|-------|-----------------------|-----------------|
| 1 | 30+ PRs opened, daily contributions | Consistency, knows the workflow |
| 2 | 10+ merged PRs across HF, EleutherAI, StanfordNLP | Can actually ship, not just open PRs |
| 3 | Bug fixes with tests in AI eval frameworks | Understands codebases deeply, writes tests |
| 4 | Feature in changelog of known AI library | Can own a task end-to-end |
| 5 | Reviewer in a top AI repo, blog post | Part of the community, trusted |

The portfolio you are building here answers the one question every top company has:
**"Can this person contribute to our codebase on day one?"**

Your GitHub will say yes — with receipts.

---

## Current Stats

- **Phase:** Phase 2 — Days 31–60
- **Total PRs opened:** 38
- **Total PRs merged:** 0 (Phase 1 pending — Phase 2 will change this)
- **PRs closed by bot:** 5 (LangChain — requires issue assignment)
- **PRs closed by maintainer:** 2 (wandb anti-AI policy · click too minor)
- **Active open PRs:** 31
- **LangChain issues awaiting assignment:** 5
- **LangGraph issues awaiting assignment:** 4

---

## LangChain — Issues Awaiting Assignment

| Issue | Fix | Status |
|-------|-----|--------|
| [#36701](https://github.com/langchain-ai/langchain/issues/36701) | Bug: `comparators` → `operators` in `Visitor._validate_func` + 4 unit tests | ⏳ Awaiting assignment |
| [#37058](https://github.com/langchain-ai/langchain/issues/37058) | Docstring: missing `await` in qdrant `asimilarity_search` example | ⏳ Awaiting assignment |
| [#38560](https://github.com/langchain-ai/langchain/issues/38560) | Docstring: missing `await` in InMemoryVectorStore + Chroma examples | ⏳ Awaiting assignment |
| [#34662](https://github.com/langchain-ai/langchain/issues/34662) | Docstring: clarify `title` is required key in JSON schema dicts | ⏳ Awaiting assignment |
| [#36750](https://github.com/langchain-ai/langchain/issues/36750) | Bug: `InMemoryCache` eviction guard + add `Language.PERL` separators | ⏳ Awaiting assignment |

## LangGraph — Issues Awaiting Assignment

| Issue | Fix | Status |
|-------|-----|--------|
| [#8130](https://github.com/langchain-ai/langgraph/issues/8130) | Typo: `GraphRecusionError` → `GraphRecursionError` in docstring | ⏳ Awaiting assignment |
| [#8226](https://github.com/langchain-ai/langgraph/issues/8226) | Grammar: `tool_calls` → `tool_call` in mermaid diagram | ⏳ Awaiting assignment |
| [#8227](https://github.com/langchain-ai/langgraph/issues/8227) | Docs: `context_schema` param missing description | ⏳ Awaiting assignment |
| [#8228](https://github.com/langchain-ai/langgraph/issues/8228) | Wrong import: `from langchain.tools import ToolNode` in 2 places | ⏳ Awaiting assignment |

---

## Skip List (repos with AI-PR policies or CLAUDE.md/AGENTS.md)

wandb · peft · trl · litellm · diffusers · huggingface_hub · tokenizers · pytorch · keras · scikit-learn · openai-python · haystack · mlflow · scikit-image · chroma · transformers · rich · timm · instructor · gradio · networkx · pytest · click · attrs

## Safe Repos (verified ruff-only CI, no restrictions)

smolagents · evaluate · accelerate · datasets · optimum · sentence-transformers · safetensors · spaCy · joblib · lighteval · nanotron · paramiko · lm-evaluation-harness · numba · stanza · optax · ragas

---

## Logs

All daily logs at [`logs/`](logs/) — one file per day with full context, what was changed, why, and lessons learned.

---

*Started: 2026-06-29 | Maintained by Chandan Kumar (RavSinghChandan)*
*Target: Top AI Engineer role at Google DeepMind · Anthropic · HuggingFace · Cohere*
