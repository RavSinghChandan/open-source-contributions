#!/usr/bin/env bash
# Finish an fpdf2 branch: changelog line (after the newest "### Fixed" entry), gate, commit, push.
#   tools/finish_fpdf2.sh "<commit subject>" "<changelog line>"   (run in the fpdf2 checkout, files already edited)
set -eu
subject=$1; line=$2
python3 - "$line" <<'PY'
import sys
lines=open('CHANGELOG.md').read().split('\n')
i=next(k for k,l in enumerate(lines) if l.startswith('### Fixed'))
lines.insert(i+1,"* "+sys.argv[1])
open('CHANGELOG.md','w').write('\n'.join(lines))
PY
"$(dirname "$0")/prepush.sh" fpdf2 2>&1 | grep -E "^(FAILED|ALL CHECKS|SOME CHECKS|---)" || true
echo "--- review: git diff --stat"; git diff --stat | tail -6
