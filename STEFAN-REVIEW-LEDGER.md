# Stefan's Review Ledger — every correction he has made, across 43 pypdf PRs

> **Purpose.** Built 2026-09-01 from all 34 review comments `stefan6419846` left on
> RavSinghChandan's PRs. Before opening any new pypdf PR, grep the diff against this list.
> A comment he has already made once must never be earned twice.
>
> Regenerate:
> ```bash
> for n in $(gh api "search/issues?q=author:RavSinghChandan+type:pr+repo:py-pdf/pypdf&per_page=100" --jq '.items[].number'); do
>   gh api "repos/py-pdf/pypdf/pulls/$n/comments" --jq ".[]|select(.user.login==\"stefan6419846\")|\"#$n :: \(.body)\""
> done
> ```

## The ranked list — how often each ask has cost a review round

| # | Ask | Times | PRs |
|---|---|---|---|
| 1 | **Meaningful `pytest.param` IDs**, never auto-generated | **6** | #4018 #4019 #4020 #4021 #4022 #4023 |
| 2 | **Don't add a test that already exists** | 3 | #3971 #4029 #4031 |
| 3 | **Unnecessary comments in the source** | 3 | #3960 #3971 #4030 |
| 4 | **No abbreviated imports / aliases** | 2 | #4003 #4014 |
| 5 | **Prefer `Literal` / `StrEnum` over broad `str`** | 3 | #3970 #3989 #4017 |
| 6 | **Drop a redundant type in a union** | 1 | #3988 |
| 7 | **Hoist a length out of a hot loop** | 1 | #4016 |
| 8 | **Factor a repeated literal into an internal constant** | 1 | #4014 |
| 9 | **Use standard characters, not fancy dashes** | 1 | #3943 |
| 10 | **Don't assert non-deterministic values** (Pillow pixels) | 1 | #3943 |
| 11 | **Prefer regular mocking over a custom class** | 1 | #3971 |
| 12 | **Behavioural change? Say so and prove the old paths hold** | 1 | #4023 |

## The checks to run before pushing

```bash
# 1. every parametrize case needs an explicit id=
git diff upstream/main..HEAD -- tests/ | grep -A8 parametrize

# 2. does a test for this already exist?
grep -rc "<function_under_test>" tests/*.py | grep -v ":0"

# 3. did I add a comment that explains the fix? delete it - it belongs in the PR body
git diff upstream/main..HEAD -- pypdf/ | grep "^+.*#"

# 4. any new abbreviated import or alias?
git diff upstream/main..HEAD | grep -E "^\+.*import .* as [a-z]{1,4}$"

# 5. broad str where the value set is closed? -> Literal or StrEnum
# 6. any non-ASCII character I introduced?
git diff upstream/main..HEAD | grep -P "^\+.*[^\x00-\x7F]"
```

## 2026-09-02 — the two failures that cost the most

**13. A network-gated test still has to be READ.** #4042 changed `xmp_metadata` to
return `None` for a non-stream entry. `test_xmp_metadata__content_stream_is_dictionary_object`
asserts the opposite — that a `DictionaryObject` RAISES `PdfReadError`. It is marked
`enable_socket` so it could not run locally; the PR body disclosed that gap and shipped
anyway. **Disclosing a risk is not clearing it.** Before changing behaviour on any path:

```bash
grep -rn "<function_under_test>" tests/*.py   # READ them, including enable_socket ones
```

If a test asserts the current behaviour, the "bug" is a deliberate design choice.

**14. The 1-2 parallel PR promise is Chandan's own, in writing.** #4018 comment
5433803551. It is not relaxed by anything short of the maintainer saying so in a link.

## Rules of engagement learned the hard way

- **#4030 — "Isn't this wrong?" is a QUESTION, not a verdict.** Read the anchored `line`
  and `diff_hunk` before answering. Answering the wrong line cost two extra rounds.
  Revert the code and run it before conceding; the guard was defensible.
- **#4023 — never claim tests are "unaffected".** That holds for your change, not for the
  general suite. Say precisely what you ran.
- **#4031 — a style failure over one blank line is a wasted round.** Run ruff before pushing.
- **#4054 — partial coverage on a new helper cost a round.** The helper had three
  exits; the tests covered one. Codecov said 80% patch, project coverage down
  0.02%, and his whole review was one line: "The coverage is incomplete
  (`is_null_or_none` not covered)." He reads the coverage bot before the diff.
  Measure your own patch coverage before pushing — Rule #14.2.
- **#4080 — a test docstring that narrates the old bug is obsolete on merge.** Mine
  said the code "raised UnboundLocalError"; once the fix lands that is no longer
  true. His whole review: "This comment seems to be obsolete." Write docstrings in
  the present tense describing what the code MUST do, matching the file's own
  style ("is_open=False must produce a collapsed outline item").
- **#4058 — a new test helper ignored the repo's own naming convention.** It went
  in as `_font_with_differences`; the repo already had `_generate_flate_pdf` and
  `_generate_dag_with_forms`. His whole review was a one-line `suggestion` block
  with the corrected name. Grep the two nearest existing examples before naming
  anything new — Rule #15. And when he sends a suggestion, apply it verbatim.

## The shape that merged clean, first try, zero comments

**#4038** (STY: Type read_object as the PdfObject it always returns) — one PR removing six
suppressions across three functions. No new tests (pure typing, no runtime change), no new
comments, mypy baseline stated explicitly, corpus-test gap disclosed upfront.
**That is the target shape: one PR, several call sites, nothing decorative.**

## 2026-09-21 — two PRs written against this ledger before pushing

Both in `pypdf/_font.py`, both crashes on `extract_text()` reproduced against a
real reader before any code was written.

- **`widths-not-an-array`** — a string `/Widths` raised `ValueError: invalid
  literal for int()`.
- **`type0-without-descendant-fonts`** — a `/Type0` font with no
  `/DescendantFonts` raised a bare `KeyError`. The source comment claimed the
  entry "need not be tested for"; that holds for the subtype, not the entry.
  The false half of the comment was deleted, the useful half kept.

Checks run before each push, not after:

| Ledger item | Result |
|---|---|
| #1 explicit `pytest.param` ids | 3 and 5 ids, zero auto-generated |
| #2 duplicate test | grepped `tests/` first; neither path had one |
| #3 comments explaining the fix | none added; two false ones removed |
| #4 abbreviated imports | none |
| #9 fancy dashes / non-ASCII | none |
| #15 naming convention | matched `test_font__<method>__<case>` from the file |
| Rule #14 diff coverage | every line of both diffs measured `ok`, none missing |
| Warning style | matched the file's `%(name)s` + keyword form, not an f-string |

The warning style was the near-miss: the first draft used an f-string, which
`_font.py` does not use. Caught by reading the two nearest `logger_warning`
calls before committing — the same grep that Rule #15 exists for.

Offline suite: 1390 passed on both branches.

## 2026-09-23 — the rules are measurably working; stop adding, start applying

Review comments Stefan left on the last ten merged PRs:

| PR | Comments | Rule that would have caused one |
|---|---|---|
| #4119 | **0** | — |
| #4118 | **0** | — |
| #4102 | **0** | — |
| #4099 | **0** | — |
| #4098 | 1 | #15 naming (`_strict` vs `__strict`) |
| #4080 | 1 | obsolete test docstring |
| #4074 | 0 | — |
| #4069 | 1 | redundant compound condition |
| #4064 | 0 | — |
| #4058 | 1 | #15 naming |

**Four consecutive zero-comment merges.** Every remaining comment was a
one-liner, and every one of those is already a numbered rule.

### What actually produces a first-time merge

Not the number of rules. Four things, done before pushing:

1. **Reproduce the crash through the public API first.** Never patch a `cast()`
   because it looks unsafe — build the file, call the method, capture the
   traceback. Half the candidates die here, which is the point: they were not
   bugs (tqdm's negative interval, tenacity's `stop_after_attempt(0)`).
2. **Grep the two nearest existing examples** before naming anything or writing
   a warning. #4118's first draft used an f-string where `_font.py` uses
   `%(name)s` + keywords. Caught before commit; it would have been a comment.
3. **Measure the diff's own branch coverage**, not the file's.
4. **Run the values that already worked.** Rule #16 came from a fix that
   correctly rejected strings and broke `effective_n_jobs(None)`.

### The failure mode to watch now

The remaining mistakes are no longer *rule* failures, they are *process* slips:
- a `Title:` prefix pasted into a PR title field (#4119)
- opening PRs while 37 sat unreviewed across 21 repos (Rule #17)

Both were caught by checking the result after acting. Neither needed a new rule.
