set -euo pipefail

root=$(git rev-parse --show-toplevel)
hook="$root/.git/hooks/pre-push"

cat > "$hook" << 'EOF'
#!/usr/bin/env bash
root=$(git rev-parse --show-toplevel)
PY=$(command -v python3 || command -v python)
"$PY" "$root/ai-review/review.py" --fail-on "${REVIEW_FAIL_ON:-none}"
EOF

chmod +x "$hook"
echo "Installed: $hook"
echo "Skip it for one push with: git push --no-verify"
