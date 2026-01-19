---
name: product-spec-interview
description: Generate product specifications through structured interviews with multi-phase validation.
version: 7.2
multi_instance: true
thread_type: chained
---

# Purpose

Generate comprehensive product specifications through structured interviews. This skill guides users from problem definition through validated output, using a multi-phase workflow with quality gates. Supports new projects, existing project documentation, and spec revisions with appropriate depth (lite/full) based on complexity.

## Variables

- `$1`: Project name or slug (Optional; used for handoff file naming)
- `$2`: Handoff file path (Optional; for resuming existing sessions)

## Thread Integration

**Thread Type:** Chained (C)

This skill implements a Chained Thread pattern with mandatory handoffs between phases and human checkpoints throughout.

**Phases:**
| Phase | Type | Description |
|-------|------|-------------|
| OPENING | Base | Classification (3 questions), no handoff needed |
| INTERVIEW | Chained | Multi-section data gathering with optional checkpoints |
| GATE | Verification | Quality validation before output (mandatory checkpoint) |
| OUTPUT | Execution | Spec generation |
| COMPLETE | Delivery | Final review and revision cycle |
| PAUSED | Checkpoint | State preservation for later resumption |

**Handoff Points:**
- After each interview section (optional checkpoint)
- Before GATE (mandatory - all data captured)
- After GATE pass (mandatory - verified ready for output)
- After OUTPUT (complete or revision cycle)

## Instructions

1. **Load State**: Check for existing handoff payload (`$2`) or create new session
2. **Route by Phase**: Read `routing.phase` and execute appropriate module
3. **Execute Module**: Run phase-specific logic, capture user responses
4. **Update Payload**: Modify state with new data after each exchange
5. **Save State**: Persist payload (always, even on error)
6. **Decide**: Continue in same instance OR checkpoint and end session

## Workflow

```
LOAD → ROUTE → EXECUTE → UPDATE → SAVE → DECIDE
                 ↓
    ┌────────────┼────────────┐
    ↓            ↓            ↓
 OPENING    INTERVIEW      GATE
    │            │            │
    └────────────┴─────┬──────┘
                       ↓
                    OUTPUT
                       │
                       ↓
                   COMPLETE
```

**Module Routing:**

| type | complexity | Module |
|------|------------|--------|
| NEW | SIMPLE | [interview-lite.md](interview-lite.md) |
| NEW | MEDIUM/COMPLEX | [interview-full-new.md](interview-full-new.md) |
| EXISTING | SIMPLE | [interview-lite.md](interview-lite.md) |
| EXISTING | MEDIUM/COMPLEX | [interview-full-existing.md](interview-full-existing.md) |

## Success Criteria

- [ ] All four hard requirements captured (problem_statement, success_metric, must_have_feature, primary_user)
- [ ] Each hard requirement passes quality check (see [gate.md](gate.md))
- [ ] Complexity level matches actual scope discovered
- [ ] User confirmed readback before output generation
- [ ] Spec generated in requested format
- [ ] No unresolved conflicts or critical open questions
- [ ] Handoff payload saved with accurate resume_point

## Report

- **Status**: [Complete | Paused | Discovery]
- **Project**: $1
- **Type**: [New | Existing]
- **Complexity**: [Simple | Medium | Complex]
- **Output**: [Spec filename or "Paused at {phase}"]
- **Sessions**: [instance_count]
- **Open Items**: [count or "None"]

---

## Module Reference

| Module | Purpose | Phase |
|--------|---------|-------|
| [handoff-schema.md](handoff-schema.md) | Payload structure and lifecycle | All |
| [interview-lite.md](interview-lite.md) | Streamlined 4-section interview | INTERVIEW |
| [interview-full-new.md](interview-full-new.md) | Complete 12-section interview (new projects) | INTERVIEW |
| [interview-full-existing.md](interview-full-existing.md) | Complete 13-section interview (existing projects) | INTERVIEW |
| [gate.md](gate.md) | Validation, quality checks, escalation | GATE |
| [output-core.md](output-core.md) | Template selection, format adaptation | OUTPUT |
| [templates/](templates/) | Spec templates | OUTPUT |

---

## Detailed Workflow Reference

### Instance Entry Point

Every instance starts here. Read the handoff payload and route accordingly.

```
ON INSTANCE START:
    
    1. CHECK for handoff payload in context or file
       - If no payload exists → CREATE new payload, set phase: OPENING
       - If payload exists → LOAD and validate
    
    2. READ routing.phase and routing.resume_point
    
    3. ROUTE to appropriate action:
       
       phase: OPENING     → Run opening sequence (Q1, Q2, Q3)
       phase: INTERVIEW   → Load routing.current_module, resume at routing.current_section
       phase: GATE        → Run gate.md validation
       phase: OUTPUT      → Run output-core.md generation
       phase: COMPLETE    → Inform user, offer revisions
       phase: PAUSED      → Show status, ask to continue
    
    4. EXECUTE module logic
    
    5. UPDATE payload with captured data
    
    6. SAVE payload (always, even on error)
    
    7. DECIDE next action:
       - Context < 35% AND more work → Continue in same instance
       - Context ≥ 35% OR section complete OR user pause → End instance, save payload
```

### Opening Sequence (Phase: OPENING)

Ask these three questions, one at a time:

**Q1: Classification**
> "Are you defining a new project or documenting/refining an existing one?"

**Q2: Complexity**
> "How would you characterize complexity: simple, medium, or complex?"

| Response | Approach | Duration |
|----------|----------|----------|
| Simple | Lite interview | 10-15 min |
| Medium | Full interview | 25-40 min |
| Complex | Full interview + edge cases | 45-90 min |

**Q3: Format**
> "What format for the final spec? (Markdown, Notion, Confluence, Google Docs)"

### Context Management

**Target: Keep context under 40% of window.**

End session and save payload when:
- Section complete (natural breakpoint)
- Context approaching 35%
- User says "pause" / "save" / "continue later"
- Complexity escalation triggered
- Gate validation complete

### Checkpoint Protocol

Offer checkpoint when ~15 exchanges without section completion, context approaching 35%, or user responses getting shorter:

```
"We've covered a lot. Current status:
✅ Complete: [sections]
🔄 Current: [section] — [progress]
⏳ Remaining: [sections]

Options:
(a) Continue now
(b) Save progress and resume later
(c) Generate partial spec with what we have"
```

### Escalation Triggers

Mid-interview complexity escalation:
- ≥5 Must-Have features → escalate to medium
- ≥3 integration points → escalate to medium
- ≥8 Must-Have features → escalate to complex
- ≥5 integration points → escalate to complex
- Interview exceeds expected duration by 50%

### Interview Mantras

- One question at a time
- Quantify vague terms ("fast" → "< 200ms p95")
- Probe thin answers once, then mark `[Needs follow-up]` and continue
- Summarize after each section before moving on
- Update and save payload after every section

### Recognizing Unready Projects

Red flags (any 2+ → suggest pausing):
- Can't articulate problem after 10 min
- "I don't know" to >50% of Section 1
- Fundamental self-contradictions
- Scope doubles during interview
- No decision-making authority present

Generate Discovery Summary instead of spec when project is unready.

### Processing User Materials

When user shares documents:
1. Acknowledge receipt
2. Extract: problem, users, features, constraints, metrics
3. Present extraction for validation
4. Streamline interview — skip sections already covered
5. Mark source in spec: `[Source: uploaded PRD]`

Conflict handling:
> "Your doc says [X], but you mentioned [Y]. Which should I use?"
