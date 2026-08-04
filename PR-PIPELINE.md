# PR Pipeline — vetted candidates

Bugs that passed all 4 gates in `CONTRIBUTION-RULES.md` Rule #8. One at a time,
engage-first, never a batch.

**Vetted:** 2026-08-04 · **Re-check claim status before starting any of these** —
unclaimed today is not unclaimed next month.

## STATUS — all 4 claimed 2026-08-04, awaiting maintainer replies

| Issue | Claimed at (UTC) | Waiting on | Next step |
|---|---|---|---|
| [aiokafka #1173](https://github.com/aio-libs/aiokafka/issues/1173) | 01:55 | `ods` | Direction: match Java (leave position) vs opt-in skip |
| [python-jose #408](https://github.com/mpdavis/python-jose/issues/408) | 02:18 | `asherf` / `mpdavis` | Fix + test fully verified — PR ready on their word |
| [authlib #740](https://github.com/lepture/authlib/issues/740) | 02:23 | `azmeuk` (he filed it) | Where the consent check belongs |
| [authlib #627](https://github.com/lepture/authlib/issues/627) | 02:24 | `azmeuk` / `lepture` | Split description fix from deprecating the check? |

**Do NOT post again on these until a maintainer replies** — chasing reads as
pressure and is the pattern that got the stanza ban. Check for replies once a
day; when one lands, build the fix and hand over the branch.

**Cadence rule:** 4 claims in one day is already the ceiling. No new claims until
at least one of these resolves.

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

**GATE 3 FAILED — NO REPRODUCIBLE FAILURE (tested 2026-08-04).** Built Flate PDFs
for all three Indexed bases and instrumented `putpalette`/`convert`:

| Base | Output | Correct? |
|---|---|---|
| /DeviceGray | `L` — `[0, 85, 170, 255]` | yes |
| /DeviceRGB | `RGB` — red, green, blue, yellow | yes |
| /DeviceCMYK | `RGB` — red, green, blue, yellow | yes |

`mode` IS overwritten at line 318, exactly as the maintainer says — but it is
consumed by `putpalette(rawmode=mode)` *before* that line, so nothing breaks.
That is why he wrote *"We should check whether this causes any harm"* — he
flagged suspicious code, not a confirmed defect.

**Do not PR without a real-world PDF that renders wrong.** Otherwise it is a
no-op refactor of working code. Park until such a file turns up.

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

**ALL 4 GATES PASSED + FIX VERIFIED (2026-08-04). This is the live one.**

Claim: 0 assignees, 0 comments, zero linked PRs. Two open PRs touch `jwe.py` —
#411 (auth-tag `compare_digest`) and #323 (headers feature) — neither near this
path.

Reproduced on released 3.5.0: `cryptography`'s PKCS1v15 fallback returns
wrong-length bytes rather than raising for **68% of malformed ciphertexts**
(204/300 measured), and those skip the random-CEK substitution entirely.
400 malformed tokens produce two attacker-visible outcomes:

```
297x  Key must be 256 bit for alg A256GCM   <- unwrap returned wrong length
103x  Invalid JWE Auth Tag                  <- substitution worked
```

Fix (length-check the unwrap, let it fall into the existing `except`) collapses
this to **400x `Invalid JWE Auth Tag`**, and all six RSA1_5 + enc combinations
still round-trip.

Maintainers are active: `asherf` 2026-07-30, `mpdavis` 2026-07-07.

**→ PRIVATE DISCLOSURE FIRST.** Full report ready to send:
`SECURITY-REPORT-python-jose-408.md`.

---

## ~~4. pdfplumber #1370~~ — CLAIMED, do not take

**[jsvine/pdfplumber#1370](https://github.com/jsvine/pdfplumber/issues/1370)** ·
10.6k★ · you use pdfplumber in `meeting-assistant`, `cv-tailor`

Labelled `bug`. Last row of a table on a page is parsed improperly when the
table is left unclosed at the page boundary.

**DIED AT GATE 2 (2026-08-04).** `Soumik8114` commented 2026-06-15:
*"I would like to address this issue and have been working upon this, would like
to make a PR after testing my solution locally."* No PR yet, but that is an
active claim — respect it. Missed on the first pass because I checked linked PRs
but not comment text; **claim checking must read the comments, not just the
timeline.**

---

## 4. authlib #740 — `consent_required` never raised (OIDC core §3.1.2.6)

**[lepture/authlib#740](https://github.com/lepture/authlib/issues/740)** · 5389★ ·
authlib is the library whose CVE mirrors your python-jose #408 finding

**Filed by `azmeuk`, an active maintainer** (merged #916 on 2026-07-30, #912 on
2026-07-17) — maintainer-confirmed by construction, same standing as pypdf #3367.

OIDC core §3.1.2.6 requires `consent_required` when `prompt=none` but the user
has not consented. `validate_request_prompt()` in
`authlib/oidc/core/grants/util.py:31` only raises `LoginRequiredError`, and only
when there is **no** end user:

```python
    if prompt == "none" and not end_user:
        raise LoginRequiredError(...)
```

A logged-in user who has not consented falls straight through.

**Verified 2026-08-04:** `consent_required` returns **zero code hits** across the
whole repo — it is never raised anywhere, exactly as reported. 0 assignees,
0 comments, no linked PRs. One open PR (#907) touches the same file but adds
`prompt=create` for issue #735 — adjacent, not overlapping.

**Repo is healthy:** 5 merges in the last 6 weeks by two maintainers
(`azmeuk`, `lepture`). No CLAUDE.md/AGENTS.md, no CONTRIBUTING AI policy.

**→ ENGAGE FIRST** — azmeuk filed it, so ask which error shape he wants before
coding (raise in `validate_request_prompt`, or a new hook).

---

## 5. authlib #627 — OAuth1 wrongly enforces TLS (copy-paste from OAuth2)

**[lepture/authlib#627](https://github.com/lepture/authlib/issues/627)** · 5389★

`OAuth1Request.__init__` calls `InsecureTransportError.check(uri)`, but OAuth 1.0
is transport-independent — it signs requests rather than relying on TLS. The
error text gives the copy-paste away: `description = "OAuth 2 MUST utilize https."`
on an **OAuth1** error class.

- `authlib/oauth1/rfc5849/wrapper.py:18` — `InsecureTransportError.check(uri)`
- `authlib/oauth1/rfc5849/errors.py:29` — `"OAuth 2 MUST utilize https."`

**Verified 2026-08-04:** both still present in current source. Open since
2024-02-17 with **0 comments, 0 assignees, no linked PRs**, and no open PR
touches either file.

**Caveat:** removing the check is a behaviour change — apps relying on it would
stop getting the error. Likely needs a deprecation path, so **ask first**. The
description-string fix is uncontroversial on its own and could ship separately.

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
| asyncpg #1335 / #1317 / #1340 / #1310 | PRs #1339 / #19 / #113 / #1312 open. |
| marshmallow #2999 | PR #3000 open. |
| marshmallow #2893 | 13 linked PRs; maintainer `lafrech` engaged. |

**Blocked repos** (CLAUDE.md/AGENTS.md → never touch): redis-py, aiohttp,
pyca/cryptography, agronholm/anyio — add to the skip list.
**Also skip:** pallets/* (click #3659 retitled "AI junk" by davidism).
