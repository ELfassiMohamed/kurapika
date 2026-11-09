#!/usr/bin/env bash
# Installs a local pre-push hook that runs the AI review.
# Advisory by default: it never blocks a push unless you set REVIEW_FAIL_ON=high (or medium/low).
# Run once from inside your repo:  bash ai-review/install-hook.sh
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
