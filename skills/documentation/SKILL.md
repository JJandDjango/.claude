---
name: documentation
description: Generates standardized JSDoc or Docstrings for functions, classes, and modules to maintain project knowledge.
---

# Purpose
To ensure the codebase remains a "living document" by automating the creation of technical metadata. This prevents context rot and enables high-autonomy agents to navigate the repository efficiently.

## Variables
- `$1`: Target file path (Required)
- `$2`: Target code block name (Optional; defaults to entire file)

## Thread Integration
- **Exploration (E)**: Use this skill to add missing documentation to legacy code discovered during RAG sweeps.
- **Implementation (I)**: Run this as a final step before handoff to the Verifier to ensure new logic is documented.
- **Refactor (R)**: Use this to update stale docstrings when logic flows are modified.

## Instructions
1. **Contextual Analysis**: Read the target file ($1). If $2 is provided, locate that specific block.
2. **Logic Extraction**: Identify input parameters (types/defaults), return values, and potential exceptions or side effects.
3. **Drafting**: Generate a documentation block following the [Agentic Patterns](../../primitives/patterns/agentic-patterns.md) of the repository.
   - For JS/TS: Use standard JSDoc.
   - For Python: Use Google-style Docstrings.
4. **Application**: Use the `Edit` tool to insert the block. Ensure no existing logic is overwritten.

## Workflow
1. `Read` the code logic.
2. `Analyze` the functional intent.
3. `Edit` the file to insert documentation.
4. `Self-Correct`: Run a linter to ensure documentation syntax doesn't break the build.

## Success Criteria
- [ ] Every parameter in the block is documented.
- [ ] Return types are explicitly defined.
- [ ] Code remains lint-clean after the edit.

## Report
- **Status**: [Success | Failed]
- **Target**: $1 ($2)
- **Modifications**: [Brief summary of added documentation]