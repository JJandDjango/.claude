# Primitive: Thread Handoff
**Purpose**: To provide a deterministic "Context Bridge" between agents, preventing context rot and ensuring high trust during thread transitions.

## 1. Thread Metadata
- **Originating Thread Type**: [Base | Chained | Parallel | Fusion | Big | Long]
- **Current Phase**: [e.g., Phase 2 of 5]
- **Confidence Score**: [0-100%] (Developer's self-assessment)

## 2. Executive Summary
- **Mission Status**: [Success | Partial | Failure | Blocked]
- **The "Big Idea"**: A 2-sentence summary of the architectural change or discovery.

## 3. Technical Changes (The Diff)
- **Modified Files**:
  - `path/to/file`: [Change description]
- **New Dependencies**: [List any added libraries/packages]
- **Side Effects**: [Potential impact on other modules]

## 4. Verification Requirements (For the Verifier)
- **Primary Validation Tool**: [e.g., npm test, vitest, rspec]
- **Mandatory Checks**:
  - [ ] Linter passes without warnings.
  - [ ] Unit tests for new logic (specify file: `path/to/test`).
  - [ ] Security audit of modified inputs/outputs.

## 5. Handoff Message
> [Natural language instructions from the previous agent to the next, clarifying any ambiguity or "gotchas" encountered during the thread.]