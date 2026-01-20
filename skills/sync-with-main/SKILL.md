---
name: sync-with-main
description: Update current git branch from main. A Base Thread utility for safe branch synchronization with automatic WIP commits.
tools: Bash
argument-hint: [commit-message]
---

# Purpose

To safely synchronize the current working branch with the main branch, handling uncommitted changes gracefully and stopping on conflicts for human resolution.

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | Commit message for WIP changes | "WIP: sync with main" |

## Thread Integration

**Thread Type:** Base (B)

This skill is a **utility** for Base Threads, providing safe branch synchronization.

| Context | Usage |
|---------|-------|
| **Base Thread (B)** | Primary use case - quick sync before starting work |
| **Long Thread (L)** | Periodic sync during extended development |
| **Any Thread** | Pre-merge preparation |

**Autonomy Level**: Low - stops immediately on any failure for human review.

**Failure Modes**:
- Merge conflicts: Stops and reports for manual resolution
- Network errors: Stops and reports connection issue
- Uncommitted changes: Commits staged changes with WIP message

## Instructions

Execute the following git commands in sequence. If any command fails, stop immediately and report the failure.

1. Check for uncommitted changes: `git status --porcelain`
2. If there are **staged** changes, commit them: `git commit -m "$1"`
   - **Note**: Only staged changes are committed. Unstaged changes are preserved.
3. `git checkout main`
4. `git fetch origin`
5. `git pull origin main`
6. `git checkout -` (return to original branch)
7. `git merge main`
8. If merge succeeds: `git push`
   - If merge conflicts occur: stop and report conflicts

## Constraints

- Do NOT force push under any circumstances
- Do NOT auto-resolve merge conflicts - always stop for human review
- Do NOT commit unstaged changes automatically
- Do NOT continue after any git command failure

## Workflow

```
1. CHECK      -> git status --porcelain
2. COMMIT     -> git commit -m "$1" (if staged changes exist)
3. SWITCH     -> git checkout main
4. FETCH      -> git fetch origin
5. PULL       -> git pull origin main
6. RETURN     -> git checkout -
7. MERGE      -> git merge main
8. PUSH       -> git push (if merge successful)
9. REPORT     -> Generate status
```

## Success Criteria

- [ ] Current branch identified correctly
- [ ] Staged changes committed (if present) with WIP message
- [ ] Main branch fetched and pulled successfully
- [ ] Original branch checked out after main update
- [ ] Merge from main completed without conflicts
- [ ] Changes pushed to remote (if merge successful)
- [ ] Clear status report generated

## Report

| Field | Value |
|-------|-------|
| **Status** | [Success \| Failed \| Merge Conflict] |
| **Original Branch** | [branch name] |
| **Changes Committed** | [Yes/No + commit hash if applicable] |
| **Merge Result** | [Clean \| Conflicts in: file1, file2...] |
| **Confirmation** | "Current branch is updated from main" |

### On Merge Conflict

If conflicts occur, the report includes:
- List of conflicting files
- Instructions: "Resolve conflicts manually, then run `git add` and `git commit`"
- Current branch state: "Merge in progress"
