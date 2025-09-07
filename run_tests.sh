#!/usr/bin/env bash
set -euo pipefail

PY="venv/Scripts/activate"   # venv Python on Windows
if [[ ! -f "$PY" ]]; then
  echo "❌ Can't find $PY"
  exit 1
fi

set +e
"$PY" -m pytest -q --headless --webdriver=Chrome
rc=$?
set -e

[[ $rc -eq 0 ]] && echo "✅ All tests passed." || echo "❌ Tests failed (exit $rc)."
exit $([[ $rc -eq 0 ]] && echo 0 || echo 1)
