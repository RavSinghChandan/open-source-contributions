#!/usr/bin/env bash
# One command before pushing an OSS branch. Runs what each repo's CI runs, plus the
# checks that review rounds kept finding. Exit code is non-zero if anything fails.
#   tools/prepush.sh fpdf2   (run in the fpdf2 checkout, using its .venv)
#   tools/prepush.sh pypdf
#   tools/prepush.sh svglib
set -u
repo=${1:?usage: prepush.sh fpdf2|pypdf|svglib}
py=.venv/bin/python
fail=0
run() { echo "--- $*"; "$@" || { echo "FAILED: $*"; fail=1; }; }
case $repo in
  fpdf2)
    run .venv/bin/black --check -q fpdf test
    run .venv/bin/pylint fpdf test tutorial/tuto*.py        # W1404: wrap adjacent strings in (parentheses)
    run .venv/bin/mypy
    run .venv/bin/pyright
    run .venv/bin/typos                                      # also reads CHANGELOG.md and test strings
    run $py -m pytest -q -p no:cacheprovider -n auto test    # known local-only: test_image_with_explicit_dimensions, test_line_break order
    ;;
  pypdf)
    run $py -m ruff check pypdf tests                        # do NOT run `ruff format`: pypdf does not use it
    run $py -m mypy pypdf
    run $py -m pytest -q -p no:cacheprovider tests           # INCLUDE the network (enable_socket) tests
    ;;
  svglib)
    run $py -m ruff format --check src tests
    run $py -m ruff check src tests
    run $py -m mypy src tests
    run $py -m pytest -q -p no:cacheprovider tests           # public_api.json: `python -m tests.test_public_api --update`
    ;;
esac
git log origin/HEAD..HEAD --format=%B 2>/dev/null | grep -qi "claude\|anthropic\|co-authored" && { echo "FAILED: AI trailer in a commit"; fail=1; }
git diff --name-only origin/HEAD...HEAD 2>/dev/null | grep -q "^sample-files$" && { echo "FAILED: submodule pointer staged"; fail=1; }
git merge-base --is-ancestor origin/HEAD HEAD || { echo "FAILED: branch is behind origin: merge it first"; fail=1; }
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit $fail
