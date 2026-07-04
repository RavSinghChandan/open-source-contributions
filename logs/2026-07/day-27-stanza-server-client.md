# Day 27 — Contribution to stanfordnlp/stanza (server/client.py)

| Field | Value |
|-------|-------|
| **Date** | 2026-07-04 |
| **Repo** | [stanfordnlp/stanza](https://github.com/stanfordnlp/stanza) |
| **Package** | `stanza` — `stanza/server/client.py` |
| **Stars** | ~7,400 |
| **Type** | Docs — add missing docstrings |
| **PR** | [#1635 — add missing docstrings to clean_props_file, is_alive and atexit_kill in server/client.py](https://github.com/stanfordnlp/stanza/pull/1635) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~60% — second PR to stanza on the same day, different module |

---

## What Was Done

Added informal-style docstrings to 3 public functions in `stanza/server/client.py`. `clean_props_file` removes a temporary properties file from disk and clears the cached path attribute on the client instance. `RobustService.is_alive` checks whether the background Java CoreNLP server process is still running by polling the process exit code. `RobustService.atexit_kill` is registered as an `atexit` handler to ensure the server process is terminated when the Python interpreter shuts down. Matched the informal docstring style used elsewhere in the file.

## Files Changed

```
stanza/server/client.py
  — added docstrings to clean_props_file(),
    RobustService.is_alive(), RobustService.atexit_kill()
```

## Why This Repo

Second contribution to stanza (different file, different branch). The server/client module wraps Stanford CoreNLP's Java server and is commonly used by users who need CoreNLP features not natively available in stanza's Python pipeline. Understanding the lifecycle management functions is important for users integrating CoreNLP into long-running services.

## Lesson Learned / Notes

The `atexit` module registers cleanup functions to run when the interpreter exits. Documenting that `atexit_kill` is an atexit handler (not just a method) helps users understand why it exists and that it should not be called directly in normal usage. The `RobustService` class is designed to keep the Java server alive across connection failures.

---
*Log created: 2026-07-04 | PR: https://github.com/stanfordnlp/stanza/pull/1635*
