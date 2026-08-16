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

## Rule #8 — VET FIRST, DEEP-DIVE SECOND. Never the other way round.

> **Added 2026-08-04.** The order is the rule. Picking an issue that looks good and
> *then* discovering it is taken, or was never a bug, is how days get burned.

The expensive mistake is not "picking the wrong bug" — it's picking one
**blindly**, sinking hours into understanding it, and only then finding out
someone already did it. Cheap checks come first. Expensive understanding comes
last, and only for what survives.

### The 4 gates, in this exact order

**Gate 1 — Is the repo safe?** (30 seconds, kills whole repos at once)
```bash
gh api repos/OWNER/REPO/contents --jq '.[].name' | grep -iE 'CLAUDE|AGENTS'
gh api repos/OWNER/REPO/contents/.github/workflows --jq '.[].name' | grep -iE 'require|assign'
gh api repos/OWNER/REPO --jq '"\(.stargazers_count)★ push=\(.pushed_at[0:10])"'
```
CLAUDE.md / AGENTS.md → abort. Assignment bot → issue-comment flow first.
Last push older than ~3 months → the PR will rot; deprioritise.

**Gate 2 — Is it UNCLAIMED?** (the gate that matters most — run before reading the issue body)
```bash
# linked PRs — the single best claim signal
gh api repos/OWNER/REPO/issues/N/timeline \
  --jq '[.[]|select(.event=="cross-referenced" and .source.issue.pull_request!=null)
        |"\(.source.issue.number)/\(.source.issue.state)"]|join(",")'

# who is already talking in the thread
gh api repos/OWNER/REPO/issues/N/comments --jq '[.[].user.login]|unique|join(",")'

# does any OPEN PR touch the same file/lines?
for n in $(gh pr list -R OWNER/REPO --state open --limit 60 --json number --jq '.[].number'); do
  gh api repos/OWNER/REPO/pulls/$n/files --jq '[.[].filename]|join(" ")' | grep -q "TARGET_FILE" && echo "PR #$n overlaps"
done
```
Any open linked PR → skip. Somebody said "I'm working on this" **and** delivered
→ skip. Somebody asked months ago and **never delivered** → fair game (check
their PR history: `gh api "search/issues?q=repo:OWNER/REPO+type:pr+author:THEM"`).

**Gate 3 — Is it actually a bug?** (verify the claim against CURRENT source, never trust the issue text)
- Read the cited lines on `master` **today** — files move, code gets refactored,
  line numbers in old issues go stale.
- If a documented user-tunable parameter fixes it → **it is not a bug.**
- Reproduce locally if the environment allows it. If it needs infrastructure
  you don't have (a Kafka broker, a 4GB file, Windows), you cannot defend the
  fix to a reviewer — downgrade it.
- If the reporter never answered the maintainer's follow-up question → unconfirmed.

**Gate 4 — Only now, deep-dive.** Understand the fix well enough to explain it
in your own words to a reviewer. If you can't, don't open the PR.

### What each gate has actually caught (real examples, 2026-08-04)

| Candidate | Died at | Why |
|---|---|---|
| pdfplumber #1380 | Gate 3 | Reproduced it — but `y_tolerance=3.5` fixes it. Documented knob, not a defect. Changing the default breaks other PDFs. |
| pdfplumber #1336 | Gate 2 | Three competing PRs (#1362/#1363/#1364) already open. |
| pdfplumber #1360 | Gate 3 | Reporter's own `snap_x_tolerance=8` fixes it. |
| soundfile #473 | Gate 3 | Student's own array-shape error, not a library bug. |
| pyjwt #1193 | Gate 3 | **A maintainer said "pr welcome" — and the bug did not exist.** `encode_token` is absent from released 2.13.0 *and* master; decode works. Reporter had a corrupted install. |
| soundfile #459 | Gate 3 | Reporter never answered `bastibe`'s question. Unconfirmed + needs a 4GB file. |
| alembic #1758/#1834, pypdf #3467/#3302, multipart #31, uvicorn #2722 | Gate 2 | All had open linked PRs. |

**The pyjwt one is the lesson in one line: a maintainer's "pr welcome" is NOT
verification.** Maintainers reply from a phone without opening the code. Gate 3
is never optional, no matter who blessed the issue.

### Bug quality bar (what "like aiokafka #1173" means)

The shape worth chasing — all five, not three of five:
1. **Real defect**, not a tuning/config/user-error issue
2. **Cites specific code** with a permalink, and that code still exists today
3. **Consequence is concrete** — data loss, silent corruption, security, crash
4. **Unclaimed** — no linked PR, nobody delivered
5. **Verifiable by you** — reproducible on macOS, or the logic is provable by reading

Prefer bugs in libraries **your own projects actually import** (the
`requirements.txt` list). joblib #1812 — the best merge to date — came from
exactly there.

---


## Rule #9 — Write the Code the Reviewer Would Have Written

> **Added 2026-08-16.** Every point below is something `stefan6419846` actually
> raised on a pypdf PR. Five PRs, five merges — but two of them needed a
> CHANGES_REQUESTED round that was avoidable. Check this list *before* pushing.

### 9.1 — Use plain ASCII in comments and docstrings

> *"Please use standard characters"* — #3943

An em dash `—`, a curly quote `’`, an arrow `→` in source code will get flagged.
Save them for the PR description. In code: `-`, `'`, `->`.

```bash
# before pushing, check every line you added:
git diff -U0 | grep '^+' | grep -P '[^\x00-\x7F]'
```

### 9.2 — Don't over-comment. Delete anything the code already says.

> *"Is this part of the comment really necessary?"* — #3960

A comment earns its place only if it says something the code cannot:
a threshold, a spec reference, a reason the obvious approach was rejected.
"Set x to None" above `x = None` is noise. **One comment per non-obvious
decision, zero otherwise.**

### 9.3 — No reST markup in plain comments

> *"Why do the docstrings need double backticks?"* — #3960

` ``value`` ` is for **rendered** docstrings. A `#` comment is never rendered,
so the backticks are just clutter. Match what the surrounding lines do.

### 9.4 — Don't hardcode an assumption the spec doesn't guarantee

> *"`[1 0]` indicates that the array always has two entries. This is wrong, as
> we allow all even array lengths."* — #3943

Before writing a fix, read what the format actually permits. If the spec says
"even length", handle even length — not the two-element case you happened to
test with.

### 9.5 — Expect "why not the other branch too?"

> *"Why can we always use the inverted order? Shouldn't we consider
> `invert_color` as well?"* — #3943

If your fix takes one path through a conditional, be ready to explain why the
other path doesn't need it. Trace every case **before** the PR, and put the
conclusion in the description. On #3943 the answer was "no path reaches this
branch with the flag false" — that answer should have been in the PR body.

### 9.6 — Don't assert values that can drift between library versions

> *"Is the exact pixel value at (0, 0) deterministic across Pillow versions?
> My preference would be to check the exact RGB value if possible, or at least
> document them inside the test."* — #3943

Decoder output can shift by a step between builds. Either pin the value **and
say in a comment why it is stable**, or assert with a tolerance far smaller
than the bug's effect. Never assert a number you cannot justify.

### 9.7 — Take the suggestion

> *"we could in theory do something like this: `bits = int(mode[0])`"* — #3929

When a maintainer offers a simpler version and it is correct, take it. Don't
defend your version because it is yours.

### 9.8 — Ask before widening scope; keep one concern per PR

> *"I guess we can make this two separate PRs if you are planning to work on
> preparing the second PR after this."* — #3929

When review reveals a second, larger problem: **reproduce it, say so, and ask**
whether to widen this PR or open another. Never silently grow a PR the
maintainer has already reviewed.

### 9.9 — Rebase onto their structure, not yours

> *"For this to get merged, please resolve the merge conflict."* — #3929

Their merged change wins by default. Move your fix into its shape, then say
in one comment: what you rebased onto, what conflicted, and any ordering
constraint you had to preserve.

### 9.10 — Match the file, not your preference

Before writing: does this module use `assert x, "mypy"` or `cast()`? NumPy or
Google docstrings? Tabs of context around a change? Copy what is already there.
`_writer.py` uses `assert ..., "mypy"` — so a narrowing assert there should
look identical.

### Pre-push checklist (30 seconds, saves a review round)

```
[ ] No non-ASCII characters in added code
[ ] Every added comment says something the code does not
[ ] No ``backticks`` in plain # comments
[ ] Handled the general case the spec allows, not just my test case
[ ] Can explain why untouched branches need no change, and it is in the PR body
[ ] Test values are either justified in a comment or asserted with tolerance
[ ] Style matches the surrounding file
[ ] Ran the repo's own checks (scripts/check, make lint, ruff, mypy) not just pytest
```

---

## Summary Checklist — Do This Every Time Before Opening a PR

```
[ ] Gate 1: repo safe (no CLAUDE.md/AGENTS.md, no assignment bot, active)
[ ] Gate 2: UNCLAIMED (no linked open PR, no overlapping open PR, nobody delivered)
[ ] Gate 3: verified a REAL bug against current master (not a tunable param, not user error)
[ ] Gate 4: understood well enough to defend to a reviewer in own words
[ ] Read CONTRIBUTING.md of the target repo
[ ] If bot exists → comment on issue first, wait for assignment
[ ] If no bot → open PR directly, link the issue
[ ] Branch name follows repo convention
[ ] Commit message follows Conventional Commits
[ ] PR description starts with "Closes #issue_number"
[ ] Fix is small, focused, and unambiguous
[ ] Zero AI signals in commit/PR/comments
```

---

*Created: 2026-06-30 | Lesson learned on Day 1 — never skip the rules of a repo*
*Updated: 2026-08-04 | Rule #8 — vet before deep-diving; 6 of 12 candidates died at Gate 2/3*
*Updated: 2026-08-16 | Rule #9 — review lessons from 5 merged pypdf PRs; write the code the reviewer would have written*
