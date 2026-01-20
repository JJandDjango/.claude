---
name: auto-fix-loop
description: Runs a continuous loop of testing and fixing until all tests pass or a maximum retry limit is reached. This is the engine for Long Threads, enabling high-autonomy debugging cycles.
---

# Purpose

To maximize agent autonomy in **Long Threads** by automating the "test-fail-fix" cycle without requiring human input for every iteration. This skill enables deterministic debugging loops that either resolve issues or escalate with full context.

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | The test command to run (e.g., `npm test`, `pytest`) | Required |
| `$2` | The maximum number of retry attempts | 3 |

## Thread Integration

**Thread Type:** Long (L)

This skill is the **engine** for Long Threads, enabling high-autonomy test-fail-fix cycles without human intervention.

| Context | Usage |
|---------|-------|
| **Long Thread (L)** | Primary use case - autonomous debugging loops |
| **Implementation (I)** | Post-implementation cleanup when tests fail |
| **Debugging (D)** | Automated fix attempts before escalation |

**Autonomy Level**: High - runs until success or max retries with no checkpoints.

**Handoff Points**:
- On success: Returns control to calling agent with success report
- On max retries: Escalates to human with failure analysis

## Instructions

1. **Execute** the provided test command (`$1`)
2. **If tests pass** (Exit Code 0): Stop and report success
3. **If tests fail**:
   - Analyze the terminal output to identify the specific error
   - Locate the relevant source file and read its content
   - Propose and apply a targeted fix using the `Edit` tool
   - Increment the retry counter
4. **Repeat** until success or the limit (`$2`) is reached

## Constraints

- Do NOT modify files unrelated to the failing test
- Do NOT apply speculative fixes without analyzing the error
- Do NOT exceed the retry limit under any circumstances
- Do NOT skip the analysis step - always understand before fixing

## Workflow

```
1. INITIALIZE  -> Set attempt = 1
2. TEST        -> Run $1
3. CHECK       -> 
   - If Success: Go to REPORT
   - If Failure AND attempt < $2: Go to FIX
   - If Failure AND attempt >= $2: Go to REPORT (Max Retries)
4. FIX         ->
   - Analyze stderr/stdout
   - Identify root cause
   - Edit the code
   - attempt++
   - Return to TEST
5. REPORT      -> Generate final status
```

## Success Criteria

- [ ] Test command executes without syntax errors
- [ ] Each fix attempt targets the specific failing test/assertion
- [ ] No unrelated code is modified during fix attempts
- [ ] Retry counter accurately tracks attempts
- [ ] Final report includes all attempted fixes
- [ ] Exit on first success (no unnecessary iterations)

## Report

| Field | Value |
|-------|-------|
| **Status** | [Success \| Failed \| Max Retries] |
| **Attempts** | [Number of loops executed] |
| **Test Command** | `$1` |
| **Resolution** | [Brief summary of the final fix applied, or failure reason] |

### Fix History (if multiple attempts)

| Attempt | Error | Fix Applied |
|---------|-------|-------------|
| 1 | [Error summary] | [Fix summary] |
| 2 | [Error summary] | [Fix summary] |
| ... | ... | ... |
