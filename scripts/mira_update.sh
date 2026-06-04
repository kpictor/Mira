#!/usr/bin/env sh
# Safely update this Mira checkout from its configured GitHub remote.

set -eu

usage() {
  cat <<'EOF'
Usage: scripts/mira_update.sh [--no-fetch] [--skip-validate] [--dry-run]

Safely updates the current Mira checkout from GitHub.

Default behavior:
  1. Check the current branch and upstream.
  2. Fetch the configured remote.
  3. Refuse to update dirty, ahead, or diverged checkouts.
  4. Run a fast-forward update only when the local checkout is strictly behind.
  5. Run `python3 scripts/validate_repo.py` after a successful update.

Status labels:
  updated
  would_update
  already_current
  blocked_dirty_worktree
  blocked_no_upstream
  blocked_ahead
  blocked_diverged
  fetch_failed
  validation_failed

Options:
  --no-fetch        Compare against existing local remote-tracking refs only.
  --skip-validate  Do not run repository validation after updating.
  --dry-run        Report what would happen without pulling or validating.
EOF
}

fetch_remote=1
run_validate=1
dry_run=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --no-fetch)
      fetch_remote=0
      ;;
    --skip-validate)
      run_validate=0
      ;;
    --dry-run)
      dry_run=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

status() {
  printf 'status=%s\n' "$1"
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git work tree." >&2
  exit 2
fi

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

branch="$(git branch --show-current)"

default_remote_ref() {
  candidate_remote="$1"
  default_ref="$(git symbolic-ref --quiet --short "refs/remotes/$candidate_remote/HEAD" 2>/dev/null || true)"
  if [ -n "$default_ref" ]; then
    echo "$default_ref"
    return 0
  fi

  if git rev-parse --verify --quiet "$candidate_remote/main" >/dev/null; then
    echo "$candidate_remote/main"
    return 0
  fi

  if git rev-parse --verify --quiet "$candidate_remote/master" >/dev/null; then
    echo "$candidate_remote/master"
    return 0
  fi

  return 1
}

upstream=""
remote=""
update_mode=""
checkout_label=""

if [ -n "$branch" ]; then
  upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  if [ -z "$upstream" ]; then
    status "blocked_no_upstream"
    echo "Branch '$branch' has no configured upstream."
    echo "Set one with: git branch --set-upstream-to <remote>/<branch>"
    exit 1
  fi
  remote="${upstream%%/*}"
  update_mode="branch"
  checkout_label="Local branch '$branch'"
else
  remote="$(git remote | sed -n '1p')"
  if [ -z "$remote" ]; then
    status "blocked_no_upstream"
    echo "Current checkout is detached and no remote is configured."
    exit 1
  fi
  upstream="$(default_remote_ref "$remote" || true)"
  if [ -z "$upstream" ]; then
    status "blocked_no_upstream"
    echo "Current checkout is detached and no default remote branch was found."
    exit 1
  fi
  update_mode="detached"
  checkout_label="Detached HEAD"
fi

if [ -n "$(git status --porcelain)" ]; then
  status "blocked_dirty_worktree"
  echo "Working tree has local changes; commit, stash, or discard them before updating."
  exit 1
fi

if [ "$fetch_remote" -eq 1 ]; then
  echo "Fetching '$remote'..."
  if ! git fetch --quiet "$remote"; then
    status "fetch_failed"
    echo "Could not fetch '$remote'. Check network access, credentials, or worktree permissions." >&2
    exit 1
  fi
else
  echo "Skipping network fetch; comparing local refs only."
fi

local_head="$(git rev-parse HEAD)"
remote_head="$(git rev-parse "$upstream")"
merge_base="$(git merge-base HEAD "$upstream")"

if [ "$local_head" = "$remote_head" ]; then
  status "already_current"
  echo "Mira is already current with $upstream."
  exit 0
fi

if [ "$remote_head" = "$merge_base" ]; then
  status "blocked_ahead"
  echo "$checkout_label is ahead of $upstream; no update was applied."
  exit 1
fi

if [ "$local_head" != "$merge_base" ]; then
  status "blocked_diverged"
  echo "$checkout_label and $upstream have diverged; review manually."
  echo "Suggested review: git log --oneline --graph --decorate --all -20"
  exit 1
fi

echo "$checkout_label is behind $upstream."

if [ "$dry_run" -eq 1 ]; then
  status "would_update"
  if [ "$update_mode" = "branch" ]; then
    echo "Dry run only; would run: git pull --ff-only"
  else
    echo "Dry run only; would run: git merge --ff-only $upstream"
  fi
  exit 0
fi

if [ "$update_mode" = "branch" ]; then
  git pull --ff-only
else
  git merge --ff-only "$upstream"
fi

if [ "$run_validate" -eq 1 ]; then
  if ! python3 scripts/validate_repo.py; then
    status "validation_failed"
    echo "Update completed, but repository validation failed." >&2
    exit 1
  fi
fi

status "updated"
echo "Mira updated from $upstream."
