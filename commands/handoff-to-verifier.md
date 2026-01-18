---
name: Handoff-To-Verifier
description: Prepares a technical handoff report and triggers the Verifier Agent for a Review Thread.
allowed-tools: Bash, Read, Write, Glob
model: sonnet
---

# Purpose
To bridge the gap between **Implementation** and **Review** phases by providing a structured, data-rich report for the auditor.

## Instructions
1. **Identify Changes**: Use `git diff` or `Glob` to list every file modified in the current thread.
2. **Gather Evidence**: Capture the output of the most recent successful test run.
3. **Populate Primitive**: Fill out the `primitives/handoff.md` template with the gathered data.
4. **Notify**: State clearly that the implementation phase is complete and provide the path to the report.

## Workflow
1. **Detect**: Run `git status` to confirm all changes are staged.
2. **Document**: Open `primitives/handoff.md` and write the "Summary of Changes" and "Technical Impact".
3. **Specify Audit**: List the exact command the Verifier should run (e.g., `npm test`).
4. **Finalize**: Commit the handoff report and prompt the user to "Initiate Review Thread".

## Report
- **Files Delivered**: [List of modified files]
- **Verification Command**: [The command for the Verifier]
- **Next Agent**: Senior Verifier