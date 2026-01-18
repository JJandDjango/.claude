---
name: Sync-With-Main
allowed-tools: Bash
description: Update current git branch from main
---

# Sync With Main

Update the current branch with changes from main

## Variables
- `$1`: Commit message for WIP changes (Default: "WIP: sync with main")

## Workflow

Execute the following git commands in sequence.
If any command fails: stop immediately and report the failure.

1. Check for uncommitted changes: `git status --porcelain`
2. If changes exist, stage and commit: `git add . && git commit -m "$1"`
   - **Warning**: This commits ALL uncommitted changes. Review `git status` first if unsure.
3. `git checkout main`
4. `git fetch origin`
5. `git pull origin main`
6. `git checkout -`
7. `git merge main`
8. If merge succeeds: `git push`
   - If merge conflicts occur: stop and report conflicts for manual resolution.

## Report

- **Status**: [Success | Failed | Merge Conflict]
- **Changes Committed**: [Yes/No + commit hash if applicable]
- **Confirmation**: "Current branch is updated from main"