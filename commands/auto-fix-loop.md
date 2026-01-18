---
name: Auto-Fix-Loop
description: Runs a continuous loop of testing and fixing until all tests pass or a maximum retry limit is reached.
allowed-tools: Bash, Read, Write, Edit
model: sonnet
---

# Purpose
To maximize agent autonomy in **Long Threads** by automating the "test-fail-fix" cycle without requiring human input for every iteration.

## Variables
- `$1`: The test command to run (e.g., `npm test`, `pytest`).
- `$2`: The maximum number of retry attempts (Default: 3).

## Instructions
1. Execute the provided test command ($1).
2. If the tests pass (Exit Code 0), stop and report success.
3. If the tests fail:
    - Analyze the terminal output to identify the specific error.
    - Locate the relevant source file and read its content.
    - Propose and apply a targeted fix using the `Edit` tool.
    - Increment the retry counter.
4. Repeat the process until success or the limit ($2) is reached.

## Workflow
1. **Initialize**: Set `attempt = 1`.
2. **Test**: Run `$1`.
3. **Check**: 
   - If Success: Go to **Report**.
   - If Failure AND `attempt < $2`: Go to **Fix**.
   - If Failure AND `attempt >= $2`: Stop and report "Max Retries Reached."
4. **Fix**:
   - Analyze stderr/stdout.
   - Edit the code.
   - `attempt++`.
   - Return to **Test**.

## Report
- **Status**: [Success | Failed | Max Retries]
- **Attempts**: [Number of loops executed]
- **Resolution**: [Brief summary of the final fix applied]