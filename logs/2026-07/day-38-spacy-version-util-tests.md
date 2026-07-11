# Day 38 — Phase 2: spaCy version util tests

**Date:** 2026-07-11
**Repo:** [explosion/spaCy](https://github.com/explosion/spaCy)
**PR:** [#13991](https://github.com/explosion/spaCy/pull/13991)
**Type:** Test coverage — regression tests for three untested utilities
**Phase:** 2

---

## What was done

Three version helpers in `spacy/util.py` had no tests:

- `get_minor_version_range` — builds a range like `>=1.2.3,<1.3.0`
- `get_base_version` — strips prerelease bits (`3.0.0.dev1` → `3.0.0`)
- `split_requirement` — splits `spacy>=1.2.3` into `("spacy", ">=1.2.3")`

Added parametrized tests to `spacy/tests/test_misc.py`, right after the
existing `test_minor_version`, matching the file's `@pytest.mark.parametrize`
+ `util.func_name` style. Verified every expected value against the real
installed spaCy (3.8.14) before committing.

### Files changed

- `spacy/tests/test_misc.py` — +33 (three parametrized test functions)
- `.github/contributors/RavSinghChandan.md` — signed contributor agreement
  (required for a first PR to this repo)

---

## First PR to spaCy — contributor agreement

spaCy requires a signed Contributor Agreement (SCA, based on the Oracle CA)
under `.github/contributors/<username>.md` on your first PR. Signed as an
individual and included in the same PR — without it, nothing merges here.

## Why this should merge

- Pure test addition, no behaviour change, zero risk
- Fills a real gap: three untested version utilities
- Matches the existing test conventions exactly
- Values verified against installed spaCy 3.8.14
- Only ruff finding in the file is a pre-existing `F841` at line 522
  (unrelated `httpd` var in someone else's test — left untouched)
- Contributor agreement signed, so the PR isn't blocked on that
