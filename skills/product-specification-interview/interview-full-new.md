---
name: product-spec-interview-full-new
description: Complete 12-section interview for new projects (medium/complex, 25-90 min).
parent: product-spec-interview
tools: Read, Write
---

# Interview Module: Full - New Projects

Complete interview for new projects with medium/complex complexity. Target: 25-90 minutes depending on complexity.

**Multi-instance:** This module reads from and writes to the handoff payload. Each section is a natural session boundary. On entry, check `routing.current_section` and `routing.resume_point` to know where to begin.

## Entry Check

```
ON MODULE ENTRY:
    1. READ routing.current_section (1-12)
    2. READ routing.resume_point for specific instruction
    3. READ interview_data for already-captured responses
    4. READ classification.complexity for depth guidance
    5. RESUME at indicated point, skip completed sections
```

## Session Planning

| Complexity | Recommended Sessions | Sections per Session |
|------------|---------------------|---------------------|
| MEDIUM | 2-4 | 3-4 sections each |
| COMPLEX | 4-6 | 2-3 sections each |

**Natural session boundaries:** After sections 3, 6, 9, 12

## Section Overview

| Section | Topic | Skip If |
|---------|-------|---------|
| 1 | Problem Space | Never |
| 2 | Users & Context | Never |
| 3 | Stakeholders | Simple OR solo dev |
| 4 | Scope & Prioritization | Never |
| 5 | Technical Context | Never |
| 6 | Functional Requirements | Never |
| 7 | Non-Functional Requirements | Simple (ask once) |
| 8 | Data Specifications | No data storage |
| 9 | API & Contracts | No integrations |
| 10 | Dependencies & Constraints | Never |
| 11 | Risks & Mitigations | Never |
| 12 | Validation & Testing | Never |

## Section 1: Problem Space

Ask in sequence:

1. "What problem does this solve?"
2. "Who experiences it and why does solving it matter?"
3. "What's the cost of not solving it? (Lost revenue, wasted time, user churn)"
4. "What solutions have been tried? Why did they fail?"
5. "How is success measured? Give me specific, measurable targets."

**Quantify everything:**
| Vague | Push for |
|-------|----------|
| "Fast" | "Target latency at p95?" |
| "Scalable" | "Concurrent users? Requests/sec?" |
| "User-friendly" | "Task completion time? Error rate?" |

**Confidence tracking:**
- High: User gives specific numbers, has data
- Medium: Reasonable estimates, some uncertainty
- Low: Guessing, contradicts self, says "probably"

Summarize: "The problem is [X], costing [Y], and success means [metrics]. Correct?"

Update state: `problem_statement`, `success_metric`, `primary_user`

## Section 2: Users & Context

1. "Who are the primary users?"
2. "Walk through their typical workflow step by step"
3. "When and why do they reach for this solution?"
4. "What's their technical sophistication?"
5. "What friction points exist in their current experience?"
6. "Any secondary users or stakeholders affected?"

Summarize personas before moving on.

## Section 3: Stakeholders & Decisions

*Skip for solo developers*

1. "Who owns this project? Who has final sign-off?"
2. "Who needs to be consulted before key decisions?"
3. "Who needs to be informed of progress?"
4. "Any competing priorities or political considerations?"
5. "Who can block this project, and what would cause them to?"

Capture RACI: Responsible, Accountable, Consulted, Informed.

## Section 4: Scope & Prioritization

1. "What's in scope for MVP?"
2. "What's explicitly out of scope?"
3. "What are non-goals — things this won't do even if users ask?"
4. "Of the in-scope items, which are Must-Have vs Should-Have vs Could-Have?"
5. "What's the dependency chain? What blocks what?"

**Force prioritization:**
> "If you had to cut 50% of scope, what survives?"

For complex projects, sketch dependency graph mentally — will render in output.

Update state: `must_have_feature` (with acceptance criteria for at least one)

## Section 5: Technical Context

1. "What existing systems must this integrate with?"
2. "What's the tech stack and deployment environment?"
3. "Quantified performance requirements?"
   - Latency targets (e.g., "API responses < 200ms p95")
   - Scale (users, requests/sec, data volume)
   - Availability (e.g., "99.9% uptime")
4. "Security, compliance, or regulatory requirements?"
5. "Resource constraints? (budget, team size, infrastructure limits)"
6. "Known bottlenecks or hard limitations?"

Update state: `technical_constraints`

## Section 6: Functional Requirements

For each feature identified in Section 4:

1. "What does [feature] do? (One sentence)"
2. "Acceptance criteria — how do we know it works?"
3. "Give me examples: happy path, edge case, error case"
4. "Input/output formats?"
5. "Error handling expectations?"
6. "Priority: Must / Should / Could?"

**Example probing:**
> "Walk me through exactly what a user would see and do"
> "What happens if [edge case]?"
> "What if the user does [unexpected thing]?"

## Section 7: Non-Functional Requirements

**For medium complexity — probe each category:**

**Performance & Scale:**
- Response time targets?
- Throughput requirements?
- Concurrent user capacity?

**Reliability:**
- Availability/uptime targets?
- Disaster recovery expectations?
- Graceful degradation behavior?

**Usability:**
- Accessibility standards (WCAG level)?
- Internationalization needs?
- Browser/platform support?

**Maintainability:**
- Code quality standards?
- Documentation requirements?
- On-call expectations?

**For complex — push harder on each with specific numbers.**

## Section 8: Data Specifications

*Skip if no data storage*

1. "What data needs to be stored, processed, or transmitted?"
2. "What's the data lifecycle? (Create, Read, Update, Delete, Archive)"
3. "How long must data be retained?"
4. "Privacy and security requirements? (PII handling, encryption)"
5. "Data volume projections?"

## Section 9: API & Contract Specifications

*Skip if no integrations*

1. "What APIs will this system expose?"
   - Endpoints, methods, auth
   - Request/response schemas
   - Rate limits
2. "What external APIs will this consume?"
   - Contract expectations
   - Fallback behavior
3. "Backward compatibility guarantees?"

## Section 10: Dependencies & Constraints

1. "External APIs or services required?"
2. "Third-party libraries or frameworks?"
3. "Timeline constraints? Hard deadlines?"
4. "Team size and skills?"
5. "Budget limitations?"
6. "What can't change? (Legacy, contracts, regulations)"

Update state: `timeline`

## Section 11: Risks & Mitigations

1. "What technical risks concern you most?"
2. "What happens if timeline slips? Fallback plan?"
3. "External factors that could derail this?"
4. "Contingency if a key dependency fails?"
5. "What assumptions might be wrong?"

**Anti-patterns to probe:**
- Scope creep signals (every feature is "must-have")
- Metric gaming potential
- Single points of failure
- Optimistic timelines without buffers

Update state: `key_risk`

## Section 12: Validation & Testing

1. "How will you know this works before users see it?"
2. "Testing approaches needed? (Unit, integration, E2E, perf, security)"
3. "Who performs UAT? Sign-off process?"
4. "Test data or environments needed?"
5. "Rollout strategy? (Big bang, phased, canary, feature flags)"
6. "How long after launch before you know it succeeded?"

## Checkpoint Protocol

**Offer checkpoint when:**
- ~15 exchanges without completion
- 6+ sections covered
- User shows fatigue (short answers)

**Checkpoint format:**
> "We've covered a lot. Status:
> ✅ Completed: [sections]
> 🔄 In progress: [current]
> ⏳ Remaining: [sections]
> 
> Continue, or generate partial spec with what we have?"

## Handling Conflicts

When detecting contradictory input:

> "I'm seeing different perspectives on [topic]. Should we:
> (a) Pick one as authoritative
> (b) Document both for later resolution
> (c) Flag for alignment discussion"

Record as: `[Conflict: A wants X, B wants Y — resolution pending]`

## Transition to Gate

After all applicable sections complete:
> "I have a comprehensive picture. Let me verify the essentials before generating the spec..."

**Payload update on interview complete:**
```yaml
routing:
  phase: GATE
  current_module: "gate.md"
  current_section: 0
  next_action: "Validate hard requirements"
  resume_point: "Full-new interview complete. Run gate validation."
history:
  - timestamp: [now]
    action: "Full-new interview complete"
    phase: INTERVIEW
    notes: "Sections completed: [list]. Transitioning to gate."
```

Proceed to [gate.md](gate.md).

## Session Boundary Guidelines

**Recommended save points:**
- After Section 3 (Stakeholders) — Opening + context complete
- After Section 6 (Functional) — Core requirements captured
- After Section 9 (API) — Technical depth complete
- After Section 12 — Full interview done

**Resume point examples:**
```yaml
# After Section 3
resume_point: "Sections 1-3 complete. Problem, users, stakeholders captured. Begin Section 4 (Scope), Q1: 'What's in scope for MVP?'"

# Mid-Section 6 (multiple features)
resume_point: "Section 6 in progress. Features captured: [list]. Currently on: [feature name]. Resume with acceptance criteria."

# After Section 9
resume_point: "Sections 1-9 complete. Technical context captured. Begin Section 10 (Dependencies). Key integration: [name] — probe for fallback."
```

**Context management:**
- Summarize captured data at session end
- Include key details in resume_point
- Reference specific user statements that need follow-up

## Success Criteria

- [ ] All applicable sections completed (based on complexity level)
- [ ] Hard requirements captured: problem_statement, success_metric, must_have_feature, primary_user
- [ ] Each hard requirement has quality flags set
- [ ] Conflicts documented with resolution status
- [ ] Checkpoint offered if session exceeded 15 exchanges
- [ ] Payload updated with accurate resume_point after each section

## Report

| Field | Value |
|-------|-------|
| **Status** | [Complete \| In Progress \| Paused] |
| **Complexity** | [Medium \| Complex] |
| **Sections Complete** | [X/12] |
| **Features Captured** | [count] |
| **Hard Reqs Status** | [X/4 captured, Y/4 quality-passed] |
| **Conflicts** | [count or None] |
| **Sessions** | [instance_count] |
| **Duration** | [estimated minutes] |
| **Next Action** | [gate.md \| Continue Section X \| Paused] |
