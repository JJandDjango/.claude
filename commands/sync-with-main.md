---
name: Sync-With-Main
allowed-tools: Bash
description: Update current git branch from main
---

# Sync With Main

Update the current branch with changes from main

## Workflow

Execute the following git commands in sequence
If any command fails: stop immediately and report the failure

1. git add . && git commit -m "WIP: sync with main"
2. git checkout main
3. git fetch origin
4. git pull origin main
5. git checkout -
6. git merge main && git push

## Report

Confirm: "Current branch is updated from main"