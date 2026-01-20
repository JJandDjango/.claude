---
name: product-spec-interview-lite
description: Streamlined 4-section interview for simple projects (10-15 min).
parent: product-spec-interview
tools: Read, Write
---

# Interview Module: Lite (Simple Projects)

Streamlined interview for simple projects. Target: 10-15 minutes, ~1 page output.

**Multi-instance:** This module reads from and writes to the handoff payload. On entry, check `routing.current_section` and `routing.resume_point` to know where to begin.

## Entry Check

```
ON MODULE ENTRY:
    1. READ routing.current_section (1-4)
    2. READ routing.resume_point for specific instruction
    3. READ interview_data for already-captured responses
    4. RESUME at indicated point, skip completed sections
```

## Sections to Cover

Cover these 4 sections. Skip stakeholders. Streamline NFRs to one question.

### Section 1: Problem Space

Ask in sequence, wait for response:

1. "What problem does this solve?"
2. "Who experiences it and why does solving it matter?"
3. "How will you measure success? Give me a specific target."

**Quantify vague answers:**
| They say | You ask |
|----------|---------|
| "Lots of users" | "What number? 100? 1000?" |
| "Save time" | "How much time per task?" |
| "Make money" | "Revenue target for month 1?" |

After responses, summarize:
> "So the problem is [X], affecting [Y], and success means [metric]. Correct?"

**Payload update after Section 1:**
```yaml
hard_reqs:
  problem_statement:
    value: "[captured - who, what, why]"
    quality_passed: [true if ≥15 words with who+why]
    quality_notes: "[any concerns]"
  success_metric:
    value: "[captured - specific target]"
    quality_passed: [true if contains number]
    quality_notes: null
  primary_user:
    value: "[captured - specific persona]"
    quality_passed: [true if not generic]
    quality_notes: null
interview_data:
  section_1_problem:
    problem: "[response to Q1]"
    who_affected: "[from Q2]"
    why_matters: "[from Q2]"
    confidence: HIGH | MEDIUM | LOW
routing:
  current_section: 2
  sections_complete: [1]
  resume_point: "Section 1 complete. Begin Section 2: Users & Context."
```

### Section 2: Users & Context

1. "Who are the primary users?"
2. "Walk me through their typical workflow — what triggers them to use this?"
3. "What's their technical level: novice, intermediate, or expert?"

Summarize before moving on.

### Section 3: Scope & Features

1. "What are the must-have features for v1? Let's list them."
2. "For each feature, what does 'done' look like? How do we know it works?"
3. "What's explicitly out of scope — things this won't do even if asked?"

**Force prioritization if needed:**
> "If you could only ship one of these, which one?"

For each must-have, capture:
- What it does (one sentence)
- Acceptance criteria (testable statement)

**Payload update after Section 3:**
```yaml
hard_reqs:
  must_have_feature:
    value: "[first feature with acceptance criteria]"
    quality_passed: [true if has testable criteria]
    quality_notes: null
interview_data:
  section_4_scope:
    must_have:
      - feature: "[name]"
        description: "[one sentence]"
        acceptance_criteria: ["[testable criterion]"]
        depends_on: null
        confidence: HIGH | MEDIUM | LOW
    out_of_scope: ["[exclusion 1]", "[exclusion 2]"]
routing:
  current_section: 4
  sections_complete: [1, 2, 3]
  resume_point: "Section 3 complete. Begin Section 4: Technical Notes & Risks."
```

### Section 4: Technical Notes & Risks

**Single NFR question:**
> "Any specific requirements for performance, reliability, or security? If not, I'll assume standard defaults."

Standard defaults (if accepted):
- Performance: Reasonable response times, no SLA
- Reliability: Best effort, no uptime guarantee
- Security: HTTPS, basic auth, no PII exposure

Then ask:
1. "What's the tech stack?"
2. "What's the main risk that could derail this? What's your fallback?"

## Section Completion Checklist

Before proceeding to gate:

```
[x] Section 1 complete — problem, success metric, primary user captured
[x] Section 2 complete — user workflow understood
[x] Section 3 complete — at least one must-have with acceptance criteria
[x] Section 4 complete — tech stack and one risk noted
```

## Handling "I Don't Know"

| Context | Response |
|---------|----------|
| Success metric | "Even a rough guess — what would make you happy in month 1?" |
| User workflow | "What would trigger someone to open this for the first time?" |
| Tech stack | "What language/framework are you most comfortable with?" |

If >2 critical "I don't know" responses → suggest pausing, generate Discovery Summary.

## Escalation Check

Before routing to gate, check:

- [ ] Did ≥5 features emerge as must-have? → Escalate to medium
- [ ] Did ≥3 integrations get mentioned? → Escalate to medium
- [ ] Did interview exceed 20 minutes? → Escalate to medium

If escalation triggered:
> "This is more complex than a simple project. Should we go deeper on [stakeholders/NFRs/risks], or proceed with what we have?"

Update `state.complexity` if user agrees.

## Transition to Gate

After all sections complete:
> "I think I have what I need for a lite spec. Let me verify..."

**Payload update on interview complete:**
```yaml
routing:
  phase: GATE
  current_module: "gate.md"
  current_section: 0
  sections_complete: [1, 2, 3, 4]
  next_action: "Validate hard requirements"
  resume_point: "Lite interview complete. Run gate validation."
history:
  - timestamp: [now]
    action: "Lite interview complete"
    phase: INTERVIEW
    notes: "4 sections completed. Transitioning to gate."
```

Proceed to [gate.md](gate.md) for validation.

## Session Boundary Guidelines

**Save payload and end session when:**
- Section 2 complete (natural midpoint)
- Context approaching 35%
- User requests pause

**Good resume points for lite interview:**
```yaml
# After Section 1
resume_point: "Section 1 complete. Problem: [summary]. Begin Section 2, Q1: 'Who are the primary users?'"

# After Section 2  
resume_point: "Sections 1-2 complete. Users: [summary]. Begin Section 3, Q1: 'What are the must-have features?'"

# Mid-Section 3 (multiple features)
resume_point: "Section 3 in progress. Captured features: [list]. Remaining: acceptance criteria for [feature]. Ask: 'What does done look like for [feature]?'"
```

## Success Criteria

- [ ] Section 1 complete with problem, success metric, primary user
- [ ] Section 2 complete with user workflow documented
- [ ] Section 3 complete with at least one must-have feature + acceptance criteria
- [ ] Section 4 complete with tech stack and one risk noted
- [ ] All hard requirements captured and quality-flagged
- [ ] Escalation check performed before gate transition
- [ ] Payload updated with accurate resume_point

## Report

| Field | Value |
|-------|-------|
| **Status** | [Complete \| In Progress \| Paused] |
| **Sections Complete** | [X/4] |
| **Features Captured** | [count] |
| **Hard Reqs Status** | [X/4 captured] |
| **Escalation** | [None \| Triggered to Medium] |
| **Duration** | [estimated minutes] |
| **Next Action** | [gate.md \| Continue Section X \| Paused] |
