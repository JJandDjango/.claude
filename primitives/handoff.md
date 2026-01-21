---
name: handoff
description: Template for thread handoffs between agents. Provides a deterministic Context Bridge to prevent context rot.
reference: true
---

# Thread Handoff

<purpose>
Provide a deterministic "Context Bridge" between agents, preventing context rot and ensuring high trust during thread transitions.
</purpose>

<context>
This template is used when one agent hands off work to another. Fill in each section to create a complete handoff report.
</context>

<variables>
| Variable | Description |
|----------|-------------|
| Thread Type | Base, Chained, Parallel, Fusion, Big, Long |
| Current Phase | e.g., Phase 2 of 5 |
| Confidence Score | 0-100% (Developer's self-assessment) |
</variables>

<output>
## 1. Thread Metadata
- **Originating Thread Type**: [Base | Chained | Parallel | Fusion | Big | Long]
- **Current Phase**: [e.g., Phase 2 of 5]
- **Confidence Score**: [0-100%]

## 2. Executive Summary
- **Mission Status**: [Success | Partial | Failure | Blocked]
- **The "Big Idea"**: [2-sentence summary of the architectural change or discovery]

## 3. Technical Changes (The Diff)
- **Modified Files**:
  - `path/to/file`: [Change description]
- **New Dependencies**: [List any added libraries/packages]
- **Side Effects**: [Potential impact on other modules]

## 4. Verification Requirements (For the Verifier)
- **Primary Validation Tool**: [e.g., npm test, vitest, rspec]
- **Mandatory Checks**:
  - [ ] Linter passes without warnings
  - [ ] Unit tests for new logic (specify file: `path/to/test`)
  - [ ] Security audit of modified inputs/outputs

## 5. Handoff Message
> [Natural language instructions from the previous agent to the next, clarifying any ambiguity or "gotchas" encountered during the thread.]
</output>
