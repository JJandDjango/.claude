---
name: interview-full-existing
description: Complete 13-section interview for existing projects with tribal knowledge capture (45-180 min).
parent: product-spec-interview
phase: INTERVIEW
complexity: MEDIUM | COMPLEX
project_type: EXISTING
---

# Interview Module: Full - Existing Projects

Complete interview for existing projects with medium/complex complexity. Emphasizes current state analysis, tribal knowledge capture, and change management.

**Multi-instance:** This module reads from and writes to the handoff payload. Each section is a natural session boundary. On entry, check `routing.current_section` and `routing.resume_point` to know where to begin.

## Entry Check

```
ON MODULE ENTRY:
    1. READ routing.current_section (1-13)
    2. READ routing.resume_point for specific instruction
    3. READ interview_data for already-captured responses
    4. READ existing_project for keep/modify/add/remove data
    5. RESUME at indicated point, skip completed sections
```

## Session Planning

| Complexity | Recommended Sessions | Sections per Session |
|------------|---------------------|---------------------|
| MEDIUM | 3-5 | 2-3 sections each |
| COMPLEX | 5-8 | 2 sections each |

**Natural session boundaries:** After sections 4, 8, 11, 13

**Note:** Section 13 (Current State) often requires significant tribal knowledge capture — plan a dedicated session.

## Key Difference from New Projects

Existing project interviews focus on:
- **What exists** vs what was planned
- **What works** vs what doesn't
- **What to keep, modify, add, remove**
- **Migration and backward compatibility**
- **Tribal knowledge capture** (often the most valuable output)

## Section Overview

| Section | Topic | Focus for Existing |
|---------|-------|-------------------|
| 1 | Problem Space | Original vs evolved problem |
| 2 | Users & Context | Expected vs actual usage |
| 3 | Stakeholders | Same as new |
| 4 | Scope | Keep/Modify/Add/Remove |
| 5 | Technical Context | Current architecture + what to change |
| 6 | Functional Requirements | Existing features + modifications |
| 7 | Non-Functional Requirements | Current vs target metrics |
| 8 | Data Specifications | Migration needs |
| 9 | API & Contracts | Breaking changes |
| 10 | Dependencies | Problematic dependencies |
| 11 | Risks | What's broken before |
| 12 | Validation | Regression + rollout |
| 13 | Current State Analysis | **New section** — ops, maintenance, tribal knowledge |

## Section 1: Problem Space (Evolved)

1. "What problem was this originally built to solve?"
2. "How has the problem evolved since launch?"
3. "What's the current problem that needs addressing?"
4. "What were the original success metrics vs actual results?"
5. "What are the new success targets?"

**Capture the delta:**
> "So originally it was [X], but now the real problem is [Y]. The new success target is [Z]. Correct?"

## Section 2: Users & Context (Actual vs Expected)

1. "Who were the expected users vs who actually uses it?"
2. "How does actual usage differ from original assumptions?"
3. "What surprised you about how users interact with this?"
4. "What do users complain about most?"
5. "What workarounds have users developed?"

**Probe for hidden behaviors:**
> "What do users do that you didn't anticipate?"
> "What features get used in ways you didn't intend?"

## Section 3: Stakeholders

Same as new projects — skip for solo developers.

## Section 4: Scope (Keep/Modify/Add/Remove)

**Structure the conversation around change types:**

1. "What exists today and works well? (Keep)"
2. "What needs improvement? (Modify)"
3. "What's missing that needs to be added? (Add)"
4. "What should be deprecated or removed? (Remove)"
5. "What's explicitly not changing this revision? (Out of scope)"

For each modification/addition:
- Priority: Must / Should / Could
- Confidence: High / Medium / Low
- Dependencies

**Force prioritization:**
> "If this revision could only accomplish one thing, what would it be?"

## Section 5: Technical Context (Current + Changes)

1. "What's the current architecture? (Stack, patterns, deployment)"
2. "What works well technically?"
3. "What doesn't work? What would you change?"
4. "What technical debt needs addressing?"
5. "What API contract changes are needed? Any breaking changes?"
6. "What constraints remain? (Budget, timeline, team)"

**Probe for pain:**
> "What's the most painful part of working with this codebase?"
> "What would break first under 10x load?"

## Section 6: Functional Requirements (Existing + New)

**For existing features being modified:**
1. "What does it do now?"
2. "What's wrong with it?"
3. "What should it do instead?"
4. "How do we know it's fixed? (Acceptance criteria)"
5. "Migration notes — how do existing users/data transition?"

**For new features:**
Same as new projects — description, acceptance criteria, examples.

## Section 7: Non-Functional Requirements (Current vs Target)

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Latency (p95) | ? | ? | ? |
| Availability | ? | ? | ? |
| Error rate | ? | ? | ? |

1. "What are current performance metrics?"
2. "What are the targets?"
3. "What must change to hit those targets?"

## Section 8: Data Specifications (Migration Focus)

1. "What data model changes are needed?"
2. "Is migration required? What's the plan?"
3. "Backward compatibility requirements?"
4. "Rollback plan if migration fails?"

## Section 9: API & Contracts (Breaking Changes)

| API | Change Type | Breaking? | Migration Plan |
|-----|-------------|-----------|----------------|
| ? | Add/Modify/Remove | Yes/No | ? |

1. "What API changes are needed?"
2. "Which are breaking changes?"
3. "What's the versioning/migration strategy?"
4. "How will consumers be notified?"

## Section 10: Dependencies (Problematic)

1. "Which current dependencies are problematic?"
2. "What needs upgrading?"
3. "What needs to be added or removed?"
4. "Any vendor lock-in concerns?"

## Section 11: Risks (Historical + Current)

1. "What's broken before? What almost broke?"
2. "What lessons were learned?"
3. "What risks exist for this revision?"
4. "What's the rollback plan?"

**Anti-patterns specific to existing projects:**
- Scope creep during "small" revisions
- Underestimating migration complexity
- Breaking backward compatibility accidentally
- Losing tribal knowledge during refactors

## Section 12: Validation (Regression + Rollout)

1. "What regression testing is needed?"
2. "How do we ensure existing functionality isn't broken?"
3. "Rollout strategy? (Feature flags, canary, phased)"
4. "Rollback plan if things go wrong?"
5. "Success validation timeline?"

## Section 13: Current State Analysis (Existing Only)

**This section captures tribal knowledge — push hard here.**

1. "What monitoring and observability exists?"
2. "What's the maintenance burden? (Hours/week, on-call frequency)"
3. "What documentation exists? What's missing or outdated?"
4. "What tribal knowledge needs capturing?"
5. "What would break if key team members left?"
6. "What's the deployment process? How painful is it?"

**Tribal knowledge probes:**
> "What do you know about this system that isn't written down anywhere?"
> "What gotchas would you warn a new team member about?"
> "What's the 'if it breaks, do this' knowledge?"

**Capture format:**
```
Tribal knowledge:
- [Thing that isn't documented]
- [Non-obvious behavior]
- [Historical decision and why]
```

## Checkpoint Protocol

Same as new projects — offer after ~15 exchanges or 6+ sections.

For existing projects, also offer:
> "We've captured a lot about current state. Want me to generate a Current State Summary before we discuss changes?"

## Transition to Gate

After all applicable sections complete:
> "I have a comprehensive picture of the current state and proposed changes. Let me verify the essentials..."

**Payload update on interview complete:**
```yaml
routing:
  phase: GATE
  current_module: "gate.md"
  current_section: 0
  next_action: "Validate hard requirements"
  resume_point: "Full-existing interview complete. Run gate validation."
history:
  - timestamp: [now]
    action: "Full-existing interview complete"
    phase: INTERVIEW
    notes: "Sections completed: [list]. Tribal knowledge captured: [count items]."
```

Proceed to [gate.md](gate.md).

## Session Boundary Guidelines

**Recommended save points:**
- After Section 4 (Scope) — Keep/modify/add/remove captured
- After Section 8 (Data) — Migration needs understood
- After Section 11 (Risks) — Historical lessons captured
- After Section 13 (Current State) — Tribal knowledge complete

**Resume point examples:**
```yaml
# After Section 4 (most critical for existing)
resume_point: "Sections 1-4 complete. Scope: Keep [n], Modify [n], Add [n], Remove [n]. Begin Section 5 (Technical), Q1: 'What's the current architecture?'"

# Mid-Section 13 (tribal knowledge)
resume_point: "Section 13 in progress. Tribal knowledge captured: [list]. Still needed: 'If it breaks' procedures, deployment gotchas. Ask: 'What would you warn a new team member about?'"

# After Section 11
resume_point: "Sections 1-11 complete. Past incidents documented: [list]. Begin Section 12 (Validation), Q1: 'What regression testing is needed?'"
```

**Existing project specifics:**
- `existing_project` payload section tracks keep/modify/add/remove
- Tribal knowledge items go in `interview_data.section_13_current_state.tribal_knowledge`
- Always note source of tribal knowledge (who said it)
