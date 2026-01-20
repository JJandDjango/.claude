---
name: handoff-to-verifier
description: Prepares a technical handoff report and triggers the Verifier Agent for a Review Thread. This is the bridge for Chained Threads, automating Implementation-to-Review transitions.
---

# Purpose

To bridge the gap between **Implementation** and **Review** phases by providing a structured, data-rich report for the auditor. This skill ensures the Two-Key rule is enforced: no code is "Done" until the Verifier provides a PASS grade.

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | Verification command for Verifier | Auto-detected or prompted |

## Thread Integration

**Thread Type:** Chained (C)

This skill is the **bridge** for Chained Threads, automating the transition from Implementation to Review phases.

| Phase Transition | Description |
|------------------|-------------|
| **Implementation -> Review** | Primary use case - prepares handoff payload for Verifier |
| **Debugging -> Review** | After fix validation, hands off for audit |
| **Refactor -> Review** | After code changes, triggers verification |

**Handoff Points**:
- **Input**: Completion of implementation work (code changes committed)
- **Output**: Structured handoff report ready for Senior Verifier

**Two-Key Integration**: This skill is the first key; the Verifier's PASS is the second key required to close a thread.

## Instructions

1. **Identify Changes**: Use `git diff` or `git status` to list every file modified in the current thread
2. **Gather Evidence**: Capture the output of the most recent successful test run
3. **Populate Primitive**: Fill out the `primitives/handoff.md` template with the gathered data
4. **Notify**: State clearly that the implementation phase is complete and provide the path to the report

## Constraints

- Do NOT modify source code - this skill is documentation-only
- Do NOT skip the test evidence step - Verifier requires proof
- Do NOT submit handoff without `git status` showing clean or staged state
- Do NOT proceed if there are uncommitted changes unrelated to the thread

## Workflow

```
1. DETECT    -> Run `git status` to confirm all changes are staged
2. DOCUMENT  -> Open `primitives/handoff.md` and write:
               - Summary of Changes
               - Technical Impact
               - Modified file list
3. SPECIFY   -> List the exact command the Verifier should run
4. FINALIZE  -> Commit the handoff report
5. NOTIFY    -> Prompt the user to "Initiate Review Thread"
```

## Success Criteria

- [ ] All modified files identified via `git diff` or `git status`
- [ ] Test evidence captured (most recent passing test output)
- [ ] `primitives/handoff.md` template fully populated
- [ ] Verification command clearly specified for Verifier
- [ ] Handoff report committed to repository
- [ ] User notified to initiate Review Thread

## Report

| Field | Value |
|-------|-------|
| **Files Delivered** | [List of modified files] |
| **Verification Command** | `$1` |
| **Handoff Location** | `primitives/handoff.md` |
| **Next Agent** | Senior Verifier |

## Handoff Payload Structure

Reference: `primitives/handoff.md`

The handoff report includes:
1. **Thread Metadata**: Type, phase, confidence score
2. **Executive Summary**: Mission status, architectural summary
3. **Technical Changes**: Modified files, dependencies, side effects
4. **Verification Requirements**: Commands, mandatory checks
5. **Handoff Message**: Natural language context for Verifier
