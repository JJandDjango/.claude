---
name: testing
description: Generates automated unit tests and integration specs to provide deterministic validation of code logic.
---

# Purpose
To eliminate "hallucinations of success" by creating independent, runnable test suites. This skill provides the objective evidence required for the **Senior Verifier** to close a thread.

## Variables
- `$1`: Source file path to be tested (Required).
- `$2`: Target test directory (Default: `tests/` or `__tests__/`).
- `$3`: Testing framework (Default: `vitest` | Options: `jest`, `pytest`, `playwright`).

## Thread Integration
- **Implementation (I)**: The Lead Developer uses this to "self-test" before submitting a handoff report.
- **Review (R)**: The Senior Verifier uses this to generate "edge-case" tests that the Developer might have missed.
- **Debugging (D)**: Used to create a "Reproduction Test Case" that proves a bug exists before attempting a fix.

## Instructions
1. **Logic Mapping**: Read the source file ($1) and identify all public exports, edge cases, and conditional branches.
2. **Spec Generation**: Create a new file in $2 following the naming convention `[filename].spec.[ext]`.
3. **Assertive Coverage**:
    - **Happy Path**: Test standard expected inputs.
    - **Pessimistic Paths**: Test nulls, undefined, empty strings, and out-of-range numbers.
    - **Mocking**: Identify external dependencies and generate mocks to ensure the test is isolated and fast.
4. **Validation**: Run the test command to ensure the generated spec is syntactically valid and runs against the source.

## Workflow
1. `Read` source code.
2. `Glob` to check for existing test configurations.
3. `Write` the new spec file.
4. `Bash` to execute the test and verify it passes (or fails as expected).

## Success Criteria
- [ ] Test file is correctly imported and linked to the source logic.
- [ ] Includes at least one test case for every public function/method.
- [ ] The test suite passes in a clean environment.

## Report
- **Test Suite**: [Path to created file]
- **Framework**: $3
- **Coverage Map**: [List of functions covered by the new specs]