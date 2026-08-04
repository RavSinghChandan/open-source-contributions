# PR Pipeline — vetted candidates

Bugs that passed all 4 gates in `CONTRIBUTION-RULES.md` Rule #8. One at a time,
engage-first, never a batch.

**Vetted:** 2026-08-04 · **Re-check claim status before starting any of these** —
unclaimed today is not unclaimed next month.

---

## 1. aiokafka #1173 — Fetcher skips a record it never returned

**[aio-libs/aiokafka#1173](https://github.com/aio-libs/aiokafka/issues/1173)** ·
1396★ · you use this in `meeting-assistant` / `ai-content-factory`

Fetcher advances the consumed position past a record it never delivered
(`RecordTooLargeError`). Under `async for`, `Consumer.__anext__` catches the
error and only logs it — so the record is dropped with one log line, and
auto-commit makes the skip permanent.

- `aiokafka/consumer/fetcher.py:877` — `tp_state.consumed_to(tp_state.position + 1)`
- `aiokafka/consumer/consumer.py:1262` — `except RecordTooLargeError: log.exception(...)`

**Verified:** both lines confirmed on master `0ff6e71`. Zero PRs reference #1173
or `RecordTooLargeError`. All 5 open PRs touching `fetcher.py` (#1170, #1167,
#1111, #1107, #1000) touch **0 lines** of this path. The skip line has never
been debated — it entered via an unrelated typing fix (`e43a738`).

**Risks:** repo last pushed 2026-05-30 (~2 months); 34 open PRs; `ods` is the
sole merger. Not reproducible on a laptop — needs a multi-partition broker with
raised `message.max.bytes`. There is a real design question (leave position
unchanged, matching Java, vs. opt-in skip) that only the maintainer can settle.

**→ ENGAGE FIRST.** Comment drafted; ask which direction before writing code.

---

## 2. pypdf #3367 — RGB image mode always overwritten

**[py-pdf/pypdf#3367](https://github.com/py-pdf/pypdf/issues/3367)** · 10.1k★ ·
you use pypdf; you already have PR #3929 in this repo

**Filed by `stefan6419846`, the lead maintainer** — so the bug is
maintainer-confirmed by construction. He also wrote, on this exact issue:
*"No need to ask for permission to work on issues as long as there is no reason
like somebody already having indicated working on it beforehand and actually
having made progress."*

The computed `mode` is unconditionally overwritten at the end of the Indexed
branch: `pypdf/generic/_image_xobject.py:318`
```python
img = img.convert("L" if base == ColorSpaces.DEVICE_GRAY else "RGB")
```
Everything the `elif mode == "L"` / `elif mode == "CMYK"` branches computed above
is discarded. Originating change: commit `68e2cf0` from #1834.

**Verified:** `nevin-lim` asked to work on it 2025-10-03 and **never delivered a
single PR** to this repo (10 months). Only open PR touching the file is #3595,
which is type-hints only. Claim still valid on current `main` (`ea00497`).

**Caveat before starting:** the file moved
(`_xobj_image_helpers.py` → `generic/_image_xobject.py`) and was refactored, so
the issue's original line numbers are stale. Re-confirm the exact failure
against a real PDF and write the reproducing test first.

**Best odds of the four** — maintainer-authored, explicitly open, active repo
(pushed daily), and you already have standing there.

---

## 3. python-jose #408 — RSA1_5 padding-oracle (RFC 7516 §11.5)

**[mpdavis/python-jose#408](https://github.com/mpdavis/python-jose/issues/408)** ·
1757★ · you use `python-jose[cryptography]` in `cv-tailor`, `bench-resource-optimizer`

JWE decryption with `alg=RSA1_5` substitutes a random CEK on the *exception*
path but never length-checks a successfully-returned unwrap. A wrong-length CEK
reaches the AES key constructor and raises a length-specific `JWKError`,
distinguishable from the MAC-failure path — a Bleichenbacher oracle.

Same class as Authlib's **CVE-2026-28490 / GHSA-7432-952r-cw78** (High), fixed
in Authlib 1.6.9.

**Verified:** unclaimed — no linked PRs, no comments at all since 2026-05-26.

**Risks:** repo may be semi-dormant (last push 2026-04-14; last merges
2025-05-28 by `asherf`). Security fixes attract scrutiny — only take this if you
can explain constant-time behaviour to a reviewer. Verify the code path against
current source before writing anything.

---

## 4. pdfplumber #1370 — table's last row dropped when unclosed

**[jsvine/pdfplumber#1370](https://github.com/jsvine/pdfplumber/issues/1370)** ·
10.6k★ · you use pdfplumber in `meeting-assistant`, `cv-tailor`

Labelled `bug`. Last row of a table on a page is parsed improperly when the
table is left unclosed at the page boundary.

**Status: NOT yet fully vetted — Gate 3 pending.** Gates 1 and 2 pass (repo
safe, active, no linked PR). Before starting: download the reporter's PDF,
reproduce locally, and confirm no tolerance parameter fixes it — that is exactly
what killed #1380, #1360 and #1336 here.

**Note:** pdfplumber issues in particular are often tuning, not defects. Three
of four candidates from this repo died at Gate 3. Verify hard.

---

## Rejected — do not revisit

| Issue | Why |
|---|---|
| pdfplumber #1380 | `y_tolerance=3.5` fixes it. Documented knob, not a bug. |
| pdfplumber #1360 | Reporter's own `snap_x_tolerance=8` fixes it. |
| pdfplumber #1336 | 3 competing PRs. |
| pyjwt #1193 | **Bug does not exist** — `encode_token` absent from 2.13.0 and master; decode works. Maintainer said "pr welcome" without checking. |
| pyjwt #1189 | PR #1195 open. |
| soundfile #473 | Reporter's own array-shape error. |
| soundfile #459 | Unconfirmed; reporter never answered maintainer; needs 4GB file. |
| soundfile #479 | PRs #480 closed. |
| alembic #1758 / #1834 | PRs #1792 / #1840 open. |
| pypdf #3467 / #3302 | PRs #3577, #3785 / #3916 open. |
| python-multipart #31 | PR #306 open. |
| uvicorn #2722 | PR #3037 open. |

**Blocked repos** (CLAUDE.md/AGENTS.md → never touch): redis-py, aiohttp —
add to the skip list alongside the existing entries.
