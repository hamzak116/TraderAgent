#!/usr/bin/env bash
# State sync for trading-agent routines. The GitHub repo is the source of
# truth, so every routine pulls fresh state before working and pushes its
# changes after. Safe to run locally or in a cloud sandbox.
#
#   sync.sh pull             # fetch latest state before a routine runs
#   sync.sh push "message"   # commit + push state changes after a routine
#
# Never fails the routine on a sync hiccup — prints a warning and continues,
# so a transient network/git issue can't block a market-open brief.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 0   # repo root

cmd="${1:-}"
case "$cmd" in
  pull)
    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "sync: not a git repo, skipping"; exit 0; }
    if git remote get-url origin >/dev/null 2>&1; then
      git pull --rebase --autostash origin main 2>&1 || echo "sync: pull failed (continuing with local state)"
    else
      echo "sync: no 'origin' remote, skipping pull"
    fi
    ;;
  push)
    msg="${2:-"trading-agent: routine state update"}"
    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "sync: not a git repo, skipping"; exit 0; }
    git add -A
    if git diff --cached --quiet; then
      echo "sync: no changes to commit"
      exit 0
    fi
    git -c user.name="trading-agent" -c user.email="moodysamkary@gmail.com" \
        commit -q -m "$msg" || { echo "sync: commit failed"; exit 0; }
    if git remote get-url origin >/dev/null 2>&1; then
      # Push current HEAD to main regardless of the checked-out branch name.
      # Local runs sit on main; cloud-routine sandboxes check out a claude/* work
      # branch — HEAD:main makes both persist state to origin/main.
      git push origin HEAD:main 2>&1 || echo "sync: push failed (committed locally; will sync next run)"
    else
      echo "sync: committed locally (no remote to push to)"
    fi
    ;;
  *)
    echo "usage: sync.sh {pull|push [message]}" >&2
    exit 1
    ;;
esac
