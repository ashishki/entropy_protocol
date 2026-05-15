#!/usr/bin/env bash
# PreToolUse hook: enforce_codex_exec.sh
# Optional guard for direct tool writes to application code paths.
# In the Codex tmux setup, the active product Codex agent remains the only normal writer of application code. Do not use nested `codex exec`.
#
# Configuration:
#   PLAYBOOK_CODE_PATH_PREFIXES  colon-separated relative path prefixes treated as
#                                application code. Default: app/:src/:lib/:tests/
#   PLAYBOOK_CODEX_ENFORCEMENT   set to "off" to disable this guard

set -euo pipefail

if [ "${PLAYBOOK_CODEX_ENFORCEMENT:-on}" = "off" ]; then
  exit 0
fi

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('file_path', ''))
" 2>/dev/null || echo "")

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

PREFIXES="${PLAYBOOK_CODE_PATH_PREFIXES:-app/:src/:lib/:tests/}"
IFS=':' read -ra PATHS <<< "$PREFIXES"

for PREFIX in "${PATHS[@]}"; do
  if [ -z "$PREFIX" ]; then
    continue
  fi

  if [[ "$FILE_PATH" == "$PREFIX"* ]] || [[ "$FILE_PATH" == *"/${PREFIX}"* ]]; then
    echo "BLOCKED: direct tool edits to application code are disabled for '${FILE_PATH}'." >&2
    echo "Continue in the active product Codex loop; do not spawn nested Codex or codex exec." >&2
    echo "This repository reserves application code writing for the active product Codex agent." >&2
    exit 2
  fi
done

exit 0
