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

**Also read the AI policy here, before writing any code** (see Rule #11):
```bash
gh api repos/OWNER/REPO/contents/CONTRIBUTING.md --jq '.content' | base64 -d \
  | grep -i -A20 "AI policy\|artificial intelligence\|\bLLM\b\|AI-generated"
```
A policy found after the PR is open is a policy already broken.

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

### 9.11 — Look for the existing test file before creating one

> *"This is wrong. Please move the tests to the existing file
> `tests/scripts/test_make_release.py`"* — #3969

I wrote in the PR body that `make_release.py` "had none", created
`tests/test_make_release.py` at the top level, and was wrong on both counts.
The real file sat in `tests/scripts/` with 10 tests, fixture data in
`tests/scripts/data/`, and its own import convention
(`pytest.importorskip("make_release")` inside each test, not a module-level
import).

A `ls tests/` is not enough — tests are often in a subdirectory that mirrors
the thing under test. Search by name before writing anything:

```bash
# is there already a test for this module?
find tests -name "*<module>*"
grep -rl "<function_you_are_testing>" tests/
```

Then read it: match its imports, its parametrize style, its naming. Adding a
second file for the same module is a guaranteed review round.

**And never claim "there were no tests" in a PR body without running that
search.** It is the kind of statement a maintainer checks in ten seconds.

### Pre-push checklist (30 seconds, saves a review round)

```
[ ] No non-ASCII characters in added code
[ ] Every added comment says something the code does not
[ ] No ``backticks`` in plain # comments
[ ] Handled the general case the spec allows, not just my test case
[ ] Can explain why untouched branches need no change, and it is in the PR body
[ ] Test values are either justified in a comment or asserted with tolerance
[ ] Searched tests/ for an existing test file before creating one
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

---

## Rule #10 — The Reviewer's Pattern: Say Less, Prove More

> **Added 2026-08-21.** Derived from every comment `stefan6419846` has left across
> 17 pypdf PRs. Nine of them were the *same three requests* in different clothes.
> Applying these before pushing is the difference between a clean merge and a
> CHANGES_REQUESTED round.

### 10.1 — Use the narrowest type that is actually true

His most repeated question, in three separate forms:

- *"Out of curiosity: Why the broad `str` and not a `Literal`?"* — #3970
- *"If I understand it correctly, the string could be a `Literal`?"* — #3989
- *"Isn't a `TreeObject` a `DictionaryObject`, thus we could drop the `TreeObject`?"* — #3988

Two failure modes, opposite directions:
- **Too broad**: `str` where only two values ever occur -> use `Literal["a", "b"]`.
- **Redundant union**: `Union[Sub, Base]` where `Sub` subclasses `Base` -> just `Base`.

Before annotating anything, ask: what is the *smallest* set this can hold, and
is any member already covered by another?

```bash
# is the union redundant?
python3 -c "from pypdf.generic import A, B; print(issubclass(A, B))"
# what values does this key actually take? instrument and run the suite.
```

### 10.2 — A test that only exercises the type checker does not belong

- *"Do we really need a test for this?"* — #3971
- *"Additionally, having typing tested in this manner might not be required at all."* — #3972

For a pure annotation change, the typeguard run **is** the evidence. An
`isinstance` assertion in the test suite tests mypy, not the library. Ship the
annotation alone and put the before/after failure counts in the PR body.

Add a test only when runtime behaviour changes.

### 10.3 — Never construct what the repo already has

- *"I am not sure whether we need to build the PDF file explicitly and do not have
  a basic file in the `resources` or `sample-files` directory."* — #3972
- *"Why cannot we patch the `decode` method and use the regular mocking, instead of
  using a custom class?"* — #3971
- *"Please move the tests to the existing file"* — #3969

Search first, in this order: existing test file -> `resources/` -> `sample-files/`
-> standard `unittest.mock`. Hand-built fixtures and bespoke helper classes are a
last resort, and he will ask why.

```bash
ls resources/ | grep -i <feature>
grep -rn "<function_under_test>" tests/ | head
```

### 10.4 — Comments are guilty until proven necessary

- *"Is this part of the comment really necessary?"* — #3960
- *"Are the new comments really necessary?"* — #3971
- *"Why do the docstrings need double backticks?"* — #3960

Default to zero comments. One earns its place only for a spec reference, a
threshold, or a rejected alternative. Never restate the code.

### 10.5 — Trace every branch before he asks about the one you skipped

- *"Why can we always use the inverted order? Shouldn't we consider `invert_color`?"* — #3943
- *"If `len(decode)` has not an even number of entries, is this an input issue...?"* — #3943
- *"`[1 0]` indicates that the array always has two entries. This is wrong."* — #3943

Handle what the **spec** permits, not what your test file happened to contain.
If the fix takes one path through a conditional, put the reason the other path
is fine in the PR body before he has to ask.

### 10.6 — Ask before widening; he will tell you which he prefers

- *"How would this affect the new parameters you introduced? Would a general fix revert these?"* — #3929

When a related problem surfaces mid-PR, name it in the body and offer to handle
it separately. Do not silently expand the diff.

### Pre-push checklist (Rule #10)

```
[ ] Every new annotation is the narrowest true type (Literal? redundant union?)
[ ] No test added for a pure annotation change
[ ] No hand-built fixture where resources/ or unittest.mock would do
[ ] Zero new comments, unless one states a spec reference or a threshold
[ ] Every untaken branch explained in the PR body
[ ] Scope is one thing; anything adjacent is offered, not included
```


---

## Rule #11 — Read the AI Policy Before the First PR, and Disclose

> **Added 2026-08-27.** After 31 merged pypdf PRs, `stefan6419846` asked directly
> whether the AI usage guidelines had been followed. They had not been read. This
> is the most expensive lesson in this file, because it puts a real reputation at
> risk rather than costing an afternoon.

### What happened

Eight PRs were open at once. The maintainer wrote:

> *"Given the relatively large number of previously unreported issues and multiple
> PRs appearing in close succession, please make sure to follow our contribution
> guidelines regarding AI usage."*

pypdf's `CONTRIBUTING.md` has an **AI Policy** section that says, in short:

1. AI assistance for coding **is allowed**.
2. **"Clearly indicate in your pull request when you used AI and include the
   corresponding tool and model."**
3. **"AI should not be used to generate comments when communicating with
   maintainers. We expect comments on our projects to be written by humans."**
4. **"Do not copy responses from the AI when replying to questions from
   maintainers."**
5. You must be able to **explain the change in your own words**.

Points 2, 3 and 4 had been broken on every PR: the bodies and the replies to
review comments were AI-written and pasted verbatim, and no disclosure was made.

### 11.1 — Grep for the policy during Gate 1, not later

Add this to the Gate 1 check in Rule #8. It costs ten seconds:

```bash
gh api repos/OWNER/REPO/contents/CONTRIBUTING.md --jq '.content' | base64 -d \
  | grep -i -A20 "AI policy\|artificial intelligence\|\bLLM\b\|AI-generated"
```

Also check `.github/CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and any
`AI_POLICY.md`. A repo without an explicit policy still deserves disclosure.

### 11.2 — The split that keeps you honest

| AI may do | You must do |
|---|---|
| Find the defect | Understand why it is a defect |
| Write the patch | Read the patch and be able to defend it |
| Run gates, tests, mutation tests | Decide whether it is worth opening |
| Draft a technical summary **for you to rewrite** | Write the PR body in your own words |
| — | **Write every reply to a maintainer yourself** |

The line is: **AI writes code, the human writes to humans.** A maintainer's
question is a conversation with a person. Answering it with pasted text is how
trust is lost, and it is what most policies specifically forbid.

### 11.3 — Disclose in the PR body

One line, at the bottom, naming the tool and model. For example:

```
Used Claude (Opus) to help locate and patch this; I reviewed and tested the change.
```

This is not an admission of weakness. Policies that ask for it are asking for
honesty, not abstinence — pypdf's own wording is *"You may ask AI for (coding)
assistance."*

### 11.4 — Volume is a signal, and reviewers read it

The same message said:

> *"we should avoid having a large number of such similar PRs being worked on in
> parallel... a significant amount of my time is currently going into reviewing
> them, which makes it harder for me to look into other reported issues and
> important blockers."*
>
> *"I would prefer not to introduce a strict limit on the number of parallel PRs
> per contributor, thus I appreciate your help in keeping this manageable."*

A maintainer is a volunteer with finite attention. Eight near-identical PRs from
one contributor is not eight times the contribution — it is a queue that crowds
out their own priorities, and it reads as automation rather than engagement.

**Cap: one or two open PRs per repo.** Open the next only after the previous
merges. If a seam yields ten bugs, that is ten weeks of contribution, not one
afternoon. A batch of similar fixes is better as **one PR touching several call
sites** than as several PRs each touching one.

### 11.5 — Speed is what made him ask

Nothing in the code was wrong. What triggered the question was the *shape* of the
activity: many previously unreported issues, found quickly, filed in close
succession, each with a polished body. That pattern is indistinguishable from an
unattended bot, whatever the truth is.

Slowing down is not just courtesy. It is what makes the contribution legible as
human work.

### 11.6 — The technical notes from that same round

Worth keeping even though those PRs were closed, because each is a habit:

**Give parametrised tests real IDs.** Raised on six PRs in one sitting:

> *"Please provide meaningful IDs as well."* / *"Please provide useful IDs."* /
> *"Please provide meaningful IDs over the auto-generated IDs."*

```python
# not this - pytest generates ids like [1-Destination tree is not a dictionary: 1]
@pytest.mark.parametrize(("value", "expected"), [(NumberObject(1), "..."), ...])

# this
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(NumberObject(1), "...", id="number"),
        pytest.param(ArrayObject(), "...", id="array"),
    ],
)
```

**Do not name a test after your own change.** On a test called
`..._valid_entries_are_unaffected`:

> *"Why 'unaffected'? This only holds true for your change, not for the general
> tests."*

The test name should describe the behaviour, not its relationship to your diff.
Six months later nobody knows what "unaffected" referred to.

**Hoist a repeated length out of a loop or condition.**

> *"For a large amount of kids, this can be costly. Please consider using a
> dedicated variable for the length."*

**Fix the type, not the call site.** On a `Literal` alias added to work around a
class used as a type:

> *"I think this is the wrong approach. Instead, we should probably make
> `PageLabelStyle` a proper `StrEnum`."*

When an annotation is wrong because the underlying construct is wrong, fix the
construct. Rule 10.1 says use the narrowest true type; this extends it — if no
true type exists yet, create it properly rather than papering over it.

**Say whether a guard changes behaviour.**

> *"Isn't this a behavioral change, or are all `null_or_none` cases still handled
> correctly?"*

Any `isinstance` guard added to a path that previously fell through needs the
untouched cases traced and stated in the PR body, before he has to ask.

### Pre-push checklist (Rule #11)

```
[ ] CONTRIBUTING.md read in full, AI policy section grepped for explicitly
[ ] Disclosure line in the PR body naming the tool and model
[ ] PR body written in my own words, not pasted
[ ] I can explain this change without re-reading the diff
[ ] At most 1-2 PRs open in this repo
[ ] Related fixes grouped into one PR rather than split across many
[ ] Every maintainer reply written by me, personally
```


*Created: 2026-06-30 | Lesson learned on Day 1 — never skip the rules of a repo*
*Updated: 2026-08-04 | Rule #8 — vet before deep-diving; 6 of 12 candidates died at Gate 2/3*
*Updated: 2026-08-16 | Rule #9 — review lessons from 5 merged pypdf PRs; write the code the reviewer would have written*
*Updated: 2026-08-16 | Rule #9.11 — search for the existing test file first; stefan caught a duplicate on #3969*
*Updated: 2026-08-21 | Rule #10 — the reviewer's pattern across 17 pypdf PRs; narrowest type, no typing tests, reuse fixtures*
*Updated: 2026-08-27 | Rule #11 — read the AI policy first, disclose the tool, cap open PRs, and write to maintainers yourself*
