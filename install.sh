#!/usr/bin/env bash
# Install CVPR-skills as a Claude Code skill.
#
#   ./install.sh              -> ~/.claude/skills/cvpr-skills
#   ./install.sh /some/where  -> /some/where/cvpr-skills
#
# The skill id is lowercase-kebab because Claude Code requires it; the project
# is CVPR-skills.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_ROOT="${1:-$HOME/.claude/skills}"
DEST="$DEST_ROOT/cvpr-skills"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found; CVPR-skills needs Python 3.8+" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"
if [ -e "$DEST" ]; then
  echo "replacing existing install at $DEST"
  rm -rf "$DEST"
fi

mkdir -p "$DEST"
for item in SKILL.md AGENTS.md manifest.yaml README.md README.zh-CN.md \
            LICENSE CHANGELOG.md references scripts tests; do
  [ -e "$SRC/$item" ] && cp -R "$SRC/$item" "$DEST/"
done
find "$DEST" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true

echo "installed to $DEST"
echo
python3 "$DEST/tests/test_audit.py" >/dev/null 2>&1 \
  && echo "self-test: passed" \
  || echo "self-test: FAILED -- run python3 $DEST/tests/test_audit.py to see why"
echo
echo "try it:"
echo "  python3 $DEST/scripts/audit_paper.py /path/to/your/paper/"
echo
echo "optional, for citation verification:"
echo "  pip install academic-refchecker[llm]"
