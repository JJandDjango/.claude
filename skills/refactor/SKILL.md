---
name: refactor
description: Reviews prompt and skill files against repository standards and generates actionable change proposals. Ensures all .md files conform to patterns defined in primitives/patterns/agentic-patterns.md.
---

# Purpose

Review prompt and skill files against repository standards and generate actionable change proposals. Ensures all `.md` files conform to the patterns defined in `primitives/patterns/agentic-patterns.md`.

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | Target file or directory to analyze (FILEPATH) | Required (prompt if missing) |

## Thread Integration

**Thread Type:** Base (B)

This skill is a **standards analyzer** that initiates refactor workflows.

| Context | Usage |
|---------|-------|
| **Base Thread (B)** | Quick compliance check on single files |
| **Exploration (E)** | Discovery phase - audit repository for non-compliance |
| **Refactor (R)** | Pre-implementation analysis before bulk updates |

**Workflow Position**:
1. `refactor` skill generates `proposed-changes.md`
2. Orchestrator routes to `@developer` for implementation
3. `@verifier` validates compliance post-implementation

**Output Handoff**: `proposed-changes.md` serves as input for Developer agent.

## Instructions

1. **Pattern Matching**: Compare target files against `primitives/patterns/agentic-patterns.md` for structural compliance
2. **Recursive Analysis**: When given a directory, scan all `.md` files and evaluate each independently
3. **Non-Destructive**: Do not modify files directly. Output proposed changes for human review
4. **Precision**: Be specific about line-level changes needed, referencing exact sections

## Constraints

- Do NOT modify files directly - output proposals only
- Do NOT propose changes to files that already comply with standards
- Do NOT reference pattern violations without citing the specific standard
- Do NOT scope beyond `.md` files within the Agentic OS repository structure

## Workflow

```
1. VALIDATE   -> If no FILEPATH provided, prompt user and end
2. LOAD       -> Read primitives/patterns/agentic-patterns.md
               Read primitives/handoff.md (for transition patterns)
3. SCAN       -> Glob FILEPATH recursively for all .md files
4. COMPARE    -> Check each file against standard sections:
               - Frontmatter (name, description)
               - Purpose
               - Variables
               - Structure (if applicable)
               - Instructions
               - Constraints (if applicable)
               - Workflow
               - Report
5. GENERATE   -> Create proposed-changes.md with remediation tasks
```

## Success Criteria

- [ ] Target path validated (file or directory exists)
- [ ] `primitives/patterns/agentic-patterns.md` loaded as reference
- [ ] All `.md` files in scope identified
- [ ] Each file compared against standard sections
- [ ] Non-compliant files documented with specific violations
- [ ] `proposed-changes.md` generated with actionable remediation tasks
- [ ] Compliant files excluded from proposals
- [ ] Line-level change references provided where applicable

## Report

| Field | Value |
|-------|-------|
| **Scope** | [Files analyzed] |
| **Compliant** | [Count of files meeting standards] |
| **Non-Compliant** | [Count of files requiring updates] |
| **Output** | `proposed-changes.md` |

## Next Steps

After generating `proposed-changes.md`, the Orchestrator should:
1. Route to `@developer` to implement approved changes
2. Route to `@verifier` to validate compliance post-implementation
