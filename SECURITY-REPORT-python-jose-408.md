# python-jose #408 — private security report (ready to send)

**Status:** vetted, reproduced, fix verified. NOT yet sent.
**Prepared:** 2026-08-04

---

## Step 1 — Where to send it

**CORRECTED 2026-08-04: private reporting is NOT available on this repo.**
`GET /repos/mpdavis/python-jose/private-vulnerability-reporting` returns
`{"enabled": false}`, so `/security/advisories/new` 404s for non-owners. A 302 on
that URL is only a login redirect — never read it as "the form exists". There is
also no `SECURITY.md` and no security contact anywhere in the repo.

Issue #408 has been public since 2026-05-26, so the vulnerability is already
disclosed. What we control is not adding a working exploit to it. **Channel used:
a public comment on #408 with no reproducer** (the short version at the bottom of
this file). Sent 2026-08-04.

Maintainer emails exist on their profiles (`michael@mpdavis.com`,
`hello@asherfoa.com`) but cold security email is a poor first contact — spam risk,
and reaches only one person.

Maintainers are alive: `asherf` (merges everything, active 2026-07-30),
`mpdavis` (owner, active 2026-07-07).

---

## Step 2 — Advisory form fields

**Title**
```
RSA1_5 JWE decryption: wrong-length unwrapped CEK bypasses random-CEK substitution (Bleichenbacher oracle)
```

**Affected product:** `python-jose` · **Ecosystem:** PyPI
**Affected versions:** `<= 3.5.0` · **Patched versions:** none yet
**Severity:** High · **CWE:** CWE-208 (Observable Timing Discrepancy) / CWE-203 (Observable Discrepancy)

**Description** — paste this:

````
## Summary

JWE decryption with `alg=RSA1_5` gives a remote attacker a padding oracle. RFC 7516
Section 11.5 requires that a recipient "MUST NOT distinguish between format, padding,
and length errors of encrypted keys" and substitute a random CEK on failure.
`jose/jwe.py` does the substitution only in the `except` branch — a successful
`unwrap_key()` return is never length-checked.

## Why the exception path is not enough

`cryptography`'s PKCS1v15 decryption does not raise for every malformed ciphertext.
Its constant-time fallback returns bytes of an arbitrary length instead. I measured
this directly on 300 random 256-byte ciphertexts against a fresh RSA-2048 key:

- 96 raised an exception  (32%)
- 204 returned wrong-length bytes without raising  (68%)

Those 204 skip the substitution entirely. `cek_bytes` then reaches the AES key
constructor, which raises a *length-specific* `JWKError`.

## Observable oracle

400 malformed tokens (`alg=RSA1_5`, `enc=A256GCM`), random encrypted-key blobs,
against python-jose 3.5.0:

```
297x  JWEError: Key must be 256 bit for alg A256GCM     <- unwrap returned wrong length
103x  JWEError: Invalid JWE Auth Tag                    <- substitution worked
```

Two distinct, attacker-visible responses for the same class of malformed input.
That is the distinguisher Section 11.5 exists to remove, and it is the same
vulnerability class as Authlib's CVE-2026-28490 / GHSA-7432-952r-cw78 ("JWE RSA1_5
Bleichenbacher Padding Oracle", High), fixed in Authlib 1.6.9.

## Reproducer

```python
import os, json
from jose import jwe
from jose.utils import base64url_encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pem = priv.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode()

hdr = base64url_encode(json.dumps({"alg": "RSA1_5", "enc": "A256GCM"}).encode())

def token():
    return b".".join([
        hdr,
        base64url_encode(os.urandom(256)),   # bogus encrypted key
        base64url_encode(os.urandom(12)),
        base64url_encode(os.urandom(32)),
        base64url_encode(os.urandom(16)),
    ]).decode()

seen = {}
for _ in range(400):
    try:
        jwe.decrypt(token(), pem)
    except Exception as e:
        seen[str(e)] = seen.get(str(e), 0) + 1

for msg, count in seen.items():
    print(count, msg)
```

## Suggested fix

Treat a wrong-length unwrap result exactly like a raised padding error, so both
paths converge on the same random-CEK substitution:

```python
        try:
            cek_bytes = key.unwrap_key(encrypted_key)

            # An unwrap that returns the wrong number of bytes is a padding
            # failure that did not raise; treat it exactly like one, so that
            # length errors stay indistinguishable (RFC 7516 Section 11.5).
            if len(cek_bytes) != len(_get_random_cek_bytes_for_enc(enc)):
                raise JWEError("Invalid CEK length")

            # Record whether the CEK could be successfully determined for this
            # recipient or not.
            cek_valid = True
        except NotImplementedError:
            raise JWEError(f"alg {alg} is not implemented")
        except Exception:
            ...
```

The `raise` lands in the existing `except Exception` block, which already performs
the substitution — so no new code path is introduced.

With this applied, the 400-token run above collapses to a single uniform response:

```
400x  JWEError: Invalid JWE Auth Tag
```

I also confirmed round-trip decryption still succeeds for every RSA1_5 + enc
combination (A128GCM, A192GCM, A256GCM, A128CBC-HS256, A192CBC-HS384, A256CBC-HS512).

Happy to open a PR with this plus a regression test whenever you prefer — I did not
want to publish the reproducer before you had a chance to look.
````

---

## Step 3 — If they reply "send a PR"

Everything is verified and ready:

- **File:** `jose/jwe.py`, inside `decrypt()`, immediately after `cek_bytes = key.unwrap_key(encrypted_key)`
- **Patch:** the 4 added lines above (comment + `if` + `raise`)
- **Test:** assert that malformed RSA1_5 tokens produce only `Invalid JWE Auth Tag`,
  never a length-specific message; plus a round-trip test per `enc`
- **Branch:** `fix/rsa1_5-cek-length-check`
- **Commit:** `fix: treat wrong-length unwrapped CEK as a padding failure`

---

## Fallback — public comment (no exploit code)

If private reporting is unavailable, post on
https://github.com/mpdavis/python-jose/issues/408 :

```
Had a look at this one. The part that makes it bite is that
cryptography's PKCS1v15 decrypt doesn't raise on every bad ciphertext —
its constant-time fallback returns wrong-length bytes instead. On a quick
run here that was about two thirds of malformed inputs, and all of those
skip the random-CEK substitution because it only sits in the except branch.

The result is two different errors coming back depending on which path you
hit, which is the distinguisher 11.5 is trying to remove.

Looks like length-checking the unwrap result and letting it fall into the
existing except branch would be enough. Happy to put a PR together with a
test if that's the direction you'd want.
```

---

## Claim check (2026-08-04, re-verify before acting)

- #408: OPEN, 0 assignees, **0 comments**, opened 2026-05-26
- **Zero linked PRs**; PR searches for `408` / `RSA1_5` / `cek` / `padding oracle` = 0
- Two open PRs touch `jwe.py`, neither near this path:
  - #411 (`Nexory`, 2026-06-18) — swaps `!=` for `hmac.compare_digest` on the auth tag
  - #323 (`debanshuk`, 2023-07-02) — additional JWE headers feature
