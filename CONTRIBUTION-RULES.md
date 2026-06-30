# Contribution Rules — Read This Before Every PR

> **Why this file exists:** On Day 1, we opened 5 PRs in LangChain without following their rules.
> All 5 were auto-closed by a bot within minutes. The fixes were correct — but we skipped the process.
> This file exists so that mistake never happens again.

---

## Rule #1 — Before Touching Any Repo, Read Their Rules First

Every big open source repo has its own contribution process. Before writing a single line of code:

1. Read `CONTRIBUTING.md` in the repo root
2. Read `CLAUDE.md` or `AGENTS.md` if it exists
3. Check `.github/workflows/` for any bots (look for files named `require_issue_link`, `auto-close`, `check-assignee`)
4. Read the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)

**Do this in 5 minutes before starting. It saves hours of wasted work.**

---

## Rule #2 — Know If the Repo Requires Issue Assignment Before PR

Some repos (LangChain, LangGraph) have a bot that **auto-closes your PR** if you are not assigned to the linked issue first.

### How to check:
```bash
# Check if the repo has a require-assignment bot
gh api repos/OWNER/REPO/contents/.github/workflows \
  --jq '.[].name' | grep -i "require\|assign\|issue"
```

### What you will find:

| Result | Meaning | What to do |
|--------|---------|------------|
| File named `require_issue_link.yml` exists | Bot will auto-close your PR if not assigned | Follow the 3-step process below |
| No such file | You can open PR directly | Open PR, link the issue, done |

---

## Rule #3 — The 3-Step Process for Repos With Assignment Bot

**LangChain, LangGraph, and similar large repos require this exact flow:**

```
Step 1 → Find an open, unassigned issue
         gh issue list --repo OWNER/REPO --state open --json number,title,assignees

Step 2 → Comment on the issue explaining your fix
         "Hi! I'd like to fix this. My approach: [explain in 2-3 lines].
          Could a maintainer assign me? I'll open the PR immediately once assigned."

Step 3 → Wait for assignment. ONLY THEN open the PR.
         The bot checks: assigned? YES → PR stays open. NO → PR auto-closed.
```

**Never skip Step 2. Never open a PR before Step 3 is complete.**

---

## Rule #4 — Repos Where You Can Open PR Directly (No Bot)

These repos have been verified — no assignment bot, PRs from external contributors are welcome directly:

| Repo | Verified | Notes |
|------|---------|-------|
| vibrantlabsai/ragas | ✅ Day 2 | Small team, fast reviews (24–48h) |
| BerriAI/litellm | ✅ Check before PR | Usually open, verify each time |
| explodinggradients/* | ✅ | Same org as ragas |
| vonzosten/awesome-LangGraph | ✅ Day 1 | Curated list, always open |

**Even for these repos — always link an issue in your PR body using `Closes #123`.**

---

## Rule #5 — How to Write a Good Assignment Request Comment

A bad comment gets ignored. A good comment gets assigned within hours.

### Bad comment (ignored):
> "Please assign me."

### Good comment (gets assigned):
> "Hi! I'd like to fix this. The issue is in `libs/core/langchain_core/caches.py` line 135 —
> the `update()` method evicts an entry even when updating a key that already exists.
> Fix: add `key not in self._cache` guard before evicting. I've already tested this locally.
> Could a maintainer assign me? I'll open the PR immediately once assigned. Thank you!"

**Formula:** What file + what line + what the fix is + you've already tested it + polite ask.

---

## Rule #6 — Branch Naming Conventions

Different repos have different branch naming rules. Always check `CONTRIBUTING.md` first.

| Repo | Branch format | Example |
|------|-------------|---------|
| langchain-ai/langchain | `username/scope/description` | `RavSinghChandan/core/fix-cache-eviction` |
| langchain-ai/langgraph | `username/scope/description` | `RavSinghChandan/prebuilt/fix-typo-graphrecursionerror` |
| vibrantlabsai/ragas | `username/fix/description` | `RavSinghChandan/fix/nonllm-context-recall-threshold` |

---

## Rule #7 — Commit Message Format

Most AI repos follow **Conventional Commits**:

```
type(scope): short description

Longer explanation if needed.

Closes #issue_number
```

Common types: `fix`, `feat`, `docs`, `test`, `chore`

Example:
```
fix(core): align NonLLMContextRecall threshold to >= for boundary consistency

Closes #2777
```

---

## Summary Checklist — Do This Every Time Before Opening a PR

```
[ ] Read CONTRIBUTING.md of the target repo
[ ] Check .github/workflows/ for require_issue_link bot
[ ] If bot exists → comment on issue first, wait for assignment
[ ] If no bot → open PR directly, link the issue
[ ] Branch name follows repo convention
[ ] Commit message follows Conventional Commits
[ ] PR description starts with "Closes #issue_number"
[ ] Fix is small, focused, and unambiguous
[ ] No code logic changes unless 100% sure (stick to docs/typos first)
```

---

*Created: 2026-06-30 | Lesson learned on Day 1 — never skip the rules of a repo*
