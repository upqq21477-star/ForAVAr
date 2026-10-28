#!/bin/sh
set -eu

# Build a public static artifact from the single authoritative source file.
# Cloudflare Pages build settings: command "sh scripts/build_static_site.sh",
# output directory "dist", framework preset "None".
# Do not publish the repository root: it contains private research material.

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
SOURCE="$REPO_ROOT/index.html"
OUTPUT="$REPO_ROOT/dist"

if [ ! -f "$SOURCE" ]; then
  printf '%s\n' "BUILD_ERROR: missing root index.html" >&2
  exit 2
fi

# Keep the deploy artifact isolated from the private repository source tree.
case "$OUTPUT" in
  "$REPO_ROOT/dist") ;;
  *)
    printf '%s\n' "BUILD_ERROR: unsafe output path" >&2
    exit 3
    ;;
esac

rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"
cp "$SOURCE" "$OUTPUT/index.html"

if ! cmp -s "$SOURCE" "$OUTPUT/index.html"; then
  printf '%s\n' "BUILD_ERROR: output does not match root index.html" >&2
  exit 4
fi

FILE_COUNT=$(find "$OUTPUT" -type f | wc -l | tr -d '[:space:]')
if [ "$FILE_COUNT" != "1" ] || [ ! -f "$OUTPUT/index.html" ]; then
  printf '%s\n' "BUILD_ERROR: dist must contain exactly one file: index.html" >&2
  exit 5
fi

printf '%s\n' "STATIC_BUILD_OK: dist/index.html; published files=1"
