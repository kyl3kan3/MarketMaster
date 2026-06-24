#!/usr/bin/env bash
# Package the distribution-engine skill into an installable .skill bundle.
#
#   bash scripts/package_skill.sh
#
# Produces dist/distribution-engine.skill (a zip of the skill directory).
# Install via Settings → Capabilities → Skills, then trigger by intent
# ("help me distribute this post") — no need to name the skill.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$ROOT/skills/distribution-engine"
DIST="$ROOT/dist"
OUT="$DIST/distribution-engine.skill"

if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
  echo "error: $SKILL_DIR/SKILL.md not found" >&2
  exit 1
fi

mkdir -p "$DIST"
rm -f "$OUT"

# Quick sanity checks before packaging.
python3 - "$SKILL_DIR" <<'PY'
import sys, pathlib, json
d = pathlib.Path(sys.argv[1])
assert (d / "SKILL.md").read_text().startswith("---"), "SKILL.md missing frontmatter"
json.loads((d / "scripts" / "connectors.json").read_text())
for f in ["scripts/engine.py", "scripts/diagnose.py", "scripts/atomize.py",
          "scripts/validate_connectors.py", "scripts/schedule.py",
          "scripts/lib/common.py", "assets/signup-form.html"]:
    assert (d / f).exists(), f"missing {f}"
print("sanity: ok")
PY

# Zip the skill folder (exclude caches / local outputs).
( cd "$ROOT/skills" && \
  zip -r -q "$OUT" "distribution-engine" \
    -x '*/__pycache__/*' -x '*/out/*' -x '*.pyc' )

echo "built: ${OUT#$ROOT/}  ($(du -h "$OUT" | cut -f1))"
unzip -l "$OUT" | tail -n +2 | head -n 40
