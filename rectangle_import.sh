#!/usr/bin/env bash
set -euo pipefail

DOMAIN="com.knollsoft.Rectangle"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PLIST_PATH="${SCRIPT_DIR}/Rectangle.plist"

if [[ ! -f "$PLIST_PATH" ]]; then
  echo "error: not found: $PLIST_PATH" >&2
  exit 1
fi

# Quit Rectangle so it doesn't overwrite prefs on exit.
osascript -e 'tell application "Rectangle" to quit' >/dev/null 2>&1 || true
sleep 0.5

# Optional: uncomment if you want an exact sync (removes keys not present in the plist)
# defaults delete "$DOMAIN" 2>/dev/null || true

defaults import "$DOMAIN" "$PLIST_PATH"

# Relaunch
open -a Rectangle

echo "Imported Rectangle prefs from: $PLIST_PATH"
