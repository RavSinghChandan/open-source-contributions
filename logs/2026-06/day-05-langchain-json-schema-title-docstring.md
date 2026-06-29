# Day 5 — Contribution to langchain-ai/langchain (core — function_calling.py)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-29 |
| **Repo** | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| **Package** | `langchain-core` |
| **Stars** | 140,482 |
| **Type** | Docstring improvement — clarify required `title` key for JSON schema dicts |
| **Issue Fixed** | [#34662 — Docs: JSON schema 'title' requirement not clearly documented](https://github.com/langchain-ai/langchain/issues/34662) |
| **PR** | [#38542 — fix(core): clarify that JSON schema dicts require a top-level `title` key](https://github.com/langchain-ai/langchain/pull/38542) |
| **Status** | ⏳ Open — awaiting review |
| **Merge probability** | ~85% — closes a reported issue, no behaviour change, pure documentation |

---

## What Was Done

### The Problem

Users passing a raw JSON schema dict to `convert_to_openai_function` or `convert_to_openai_tool` hit this confusing error:

```
ValueError: Unsupported function {...}
Functions must be passed in as Dict, pydantic.BaseModel, or Callable.
If they're a dict they must either be in OpenAI function format or valid JSON
schema with top-level 'title' key.
```

The error message mentions `title` — but the docstrings for both functions did NOT make this requirement obvious. The existing text only said:

> "a JSON schema with top-level `title` key specified"

…buried in a list of accepted formats, with no example and no explanation of WHY `title` is needed.

### What Was Fixed

Expanded the `Args` section of BOTH functions — `convert_to_openai_function` and `convert_to_openai_tool` — to:

1. Explicitly say `title` is **required** (not just mentioned in passing)
2. Explain what `title` is used for — it becomes the function/tool name
3. Show a minimal, copy-pasteable example of the correct shape
4. Add `ValueError` to the `Raises` section of `convert_to_openai_function` (it was missing)

### The Fix (docstring change only, no code changed)

```python
# BEFORE (confusing):
"""
Args:
    function: A dictionary, Pydantic BaseModel class, TypedDict class, a
        LangChain Tool object, or a Python function.

        If a dictionary is passed in, it is assumed to already be a valid OpenAI
        function, a JSON schema with top-level `title` key specified, an Anthropic
        format tool, or an Amazon Bedrock Converse format tool.
"""

# AFTER (clear):
"""
Args:
    function: A dictionary, Pydantic BaseModel class, TypedDict class, a
        LangChain Tool object, or a Python function.

        If a dictionary is passed in, it is assumed to already be a valid OpenAI
        function, a JSON schema with top-level `title` key specified, an Anthropic
        format tool, or an Amazon Bedrock Converse format tool.

        When passing a raw JSON schema dict, a top-level `title` key is **required**
        and will be used as the function name. Schemas without `title` raise a
        `ValueError`. Example of a valid JSON schema dict:

        .. code-block:: python

            {
                "title": "ContactInfo",          # required — becomes function name
                "description": "Contact details",  # optional
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
                "required": ["name", "email"],
            }
"""
```

---

## Q&A

**Q: Why is `title` required for JSON schema dicts?**
A: LangChain converts JSON schema dicts into OpenAI function-calling format. OpenAI requires a `name` for every function. LangChain uses the `title` field of the schema as that `name`. Without `title`, there is no name → ValueError. It is a design decision, not a bug.

**Q: Why were both `convert_to_openai_function` and `convert_to_openai_tool` fixed?**
A: Both functions have the same dict-processing logic and the same gap in their docstrings. They are often used interchangeably by users. Fixing only one would leave the other confusing.

**Q: Does this change any behaviour?**
A: Zero. Only docstrings were modified. No logic, no tests needed.

**Q: What does a user now need to do differently?**
A: Nothing changes in code. But when they read the docs before writing code, they will immediately see the example and know to add `"title": "MyFunctionName"` to their dict.

**Q: How did you find this issue?**
A: Searched `gh search issues "documentation" --repo langchain-ai/langchain --state open` and filtered for issues with the `bug` or `doc` label. Issue #34662 was 6 months old, unassigned, clearly described — perfect for a targeted docstring fix.

---

## Files Changed

```
libs/core/langchain_core/utils/function_calling.py
  — convert_to_openai_function docstring: expanded Args + added Raises entry
  — convert_to_openai_tool docstring: expanded Args with same clarification
  — Total: +38 lines, 0 logic changes
```

---

## Lesson Learned

Documentation issues filed months ago and never picked up are **gold** for contributors. They are:
- Already validated by a real user who was confused
- Never assigned to anyone
- No code change needed — just reading + writing clearly
- Fast to fix (30 minutes total)
- High merge probability (no risk of breaking anything)

The key is reading the issue carefully, understanding the root confusion, and fixing it where a user would FIRST look — the docstring, not a separate docs page.

---

*Log created: 2026-06-29*
