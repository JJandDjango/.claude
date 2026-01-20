---
name: product-spec-interview-gate
description: Validates hard requirements and quality checks before output generation.
parent: product-spec-interview
tools: Read, Write
---

# Gate Module: Validation & Quality Checks

This module enforces hard requirements before output generation. **No output without passing the gate.**

**Multi-instance:** This module reads from the handoff payload and validates statelessy — it does not require conversation history. All data needed for validation is in the payload.

## Entry Check

```
ON MODULE ENTRY:
    1. READ routing.phase (should be GATE)
    2. READ hard_reqs for presence and quality flags
    3. READ interview_data for validation context
    4. READ classification for completeness check
    5. RUN validation sequence
```

## Gate Sequence

```
1. PRESENCE CHECK  → All hard_reqs must be non-null
2. QUALITY CHECK   → Each hard_req must meet substance criteria
3. ESCALATION      → Verify complexity wasn't underestimated
4. COMPLETENESS    → Required sections for complexity level
5. READBACK        → Summarize and confirm before output
```

---

## Step 1: Presence Check

**Verify ALL four hard requirements are non-null:**

```
[ ] problem_statement is not null
[ ] success_metric is not null  
[ ] must_have_feature is not null
[ ] primary_user is not null
```

### Presence Failure Response

For each null hard requirement, prompt for that specific item:

| Missing | Prompt |
|---------|--------|
| problem_statement | "I need to understand the problem better. Who experiences this and why does solving it matter?" |
| success_metric | "How will you know this succeeded? Even a rough target helps — what would make you happy in month 1?" |
| must_have_feature | "What's the one feature that absolutely must work for this to be useful? What does 'done' look like for it?" |
| primary_user | "Who's the main person using this? What's their role or context?" |

**Never ask for all missing items at once.** Ask for the first missing item, wait for response, then check again.

---

## Step 2: Quality Check

**After presence check passes, validate substance.**

Each hard requirement must meet quality criteria. Presence ≠ quality.

| Field | Quality Criteria | Failure Test | Remediation Prompt |
|-------|------------------|--------------|-------------------|
| problem_statement | ≥15 words AND includes who has the problem AND why it matters | Fewer than 15 words OR missing "who" OR missing "why/impact" | "That's thin. Who specifically has this problem, and what's the cost of not solving it?" |
| success_metric | Contains a number OR comparison operator (>, <, %, increase, decrease, reduce) | No quantifiable element | "That metric isn't measurable. What number would tell you this succeeded? Give me a target." |
| must_have_feature | Includes testable acceptance criteria (how we know it works) | No "done when" or testable condition | "How will we know this feature works? Give me a specific test: 'It works when [X]'" |
| primary_user | Specific role, persona, or segment (not "users" or "everyone") | Generic terms like "users", "people", "customers", "everyone" | "Who specifically? Give me a role, job title, or specific segment." |

### Quality Check Examples

**problem_statement:**
- ❌ FAIL: "Checkout is slow" (7 words, no who, no why)
- ❌ FAIL: "Users don't like the current system" (no impact)
- ✅ PASS: "E-commerce customers on mobile devices are abandoning carts due to a 12-second checkout flow, costing us approximately $50,000 per month in lost revenue" (26 words, who=mobile customers, why=$50K/month)

**success_metric:**
- ❌ FAIL: "Users are happy"
- ❌ FAIL: "Faster checkout"
- ❌ FAIL: "Improved conversion"
- ✅ PASS: "Reduce cart abandonment from 68% to 45%"
- ✅ PASS: "Checkout completion time < 3 seconds"
- ✅ PASS: "Increase monthly revenue by $30K"

**must_have_feature:**
- ❌ FAIL: "One-click checkout"
- ❌ FAIL: "Fast payment processing"
- ✅ PASS: "One-click checkout: Works when returning users can complete purchase without re-entering payment info, in under 2 seconds"
- ✅ PASS: "Guest checkout: Done when users can purchase without creating an account, verified by completing test purchase with new email"

**primary_user:**
- ❌ FAIL: "Users"
- ❌ FAIL: "Our customers"
- ❌ FAIL: "Everyone who uses the app"
- ✅ PASS: "Mobile shoppers completing purchases on iOS/Android"
- ✅ PASS: "First-time buyers unfamiliar with our platform"
- ✅ PASS: "Warehouse managers processing 50+ orders/day"

### Quality Failure Response

When a field passes presence but fails quality:

> "I have [field] recorded as: '[current value]'
> 
> That doesn't quite meet the bar — [specific issue]. [Remediation prompt]"

**One field at a time.** Fix, then re-check.

---

## Step 3: Escalation Check

Before passing to output, verify complexity wasn't underestimated.

### Escalation Triggers

| Trigger | From | To |
|---------|------|-----|
| ≥5 Must-Have features | Simple | Medium |
| ≥3 integration points | Simple | Medium |
| ≥8 Must-Have features | Medium | Complex |
| ≥5 integration points | Medium | Complex |
| Interview exceeded expected duration by 50% | Any | Next level |
| User said "more complicated than I thought" | Any | Next level |

### Escalation Response

If escalation triggered and not already at max complexity:

> "Based on what we've discussed, this is more complex than initially assessed. I'm adjusting to [new complexity level].
> 
> This means I'll include additional sections in the spec: [list new sections].
> 
> Should I ask a few more questions about [new areas], or proceed with what we have?"

Update state:
```yaml
state:
  complexity: [new level]
  flags:
    escalation_triggered: true
```

If user declines deeper interview, proceed but note in spec:
> `[Note: Complexity escalated from [X] to [Y] mid-interview. Some sections may benefit from additional detail.]`

---

## Step 4: Completeness Validation

### Required Sections by Complexity

| Complexity | Required Sections |
|------------|-------------------|
| Simple | 1 (Problem), 2 (Users), 3 (Scope), 4 (Tech/Risks) |
| Medium | 1-7, 10-12 |
| Complex | 1-12 (all) |

For existing projects, also require Section 13 (Current State) for medium/complex.

### Incomplete Section Handling

If required sections are incomplete:

> "We haven't covered [section names]. These are typically important for [complexity] projects.
> 
> Should we:
> (a) Cover them now (5-10 min)
> (b) Mark as TBD and proceed
> (c) Generate partial spec with gaps flagged"

---

## Step 5: Readback Confirmation

**Always perform readback before proceeding to output.**

> "Before I generate the spec, let me confirm I understood correctly:
> 
> **Problem:** [1-2 sentence summary]
> **Success:** [primary metric with target]
> **Primary User:** [specific persona]
> **Must-Haves:** [feature list with key acceptance criteria]
> **Key Risk:** [primary risk if captured]
> **Timeline:** [if captured]
> 
> What did I miss or misunderstand?"

**Wait for explicit confirmation before proceeding.**

Acceptable confirmations: "yes", "correct", "looks good", "proceed", thumbs up, etc.

If user provides corrections, update state and re-confirm the corrected items.

---

## Soft Requirements Check

After hard requirements pass (presence + quality), flag missing soft requirements:

```
[ ] technical_constraints — Stack, integrations, infrastructure
[ ] key_risk — At least one risk identified
[ ] timeline — Deadline or target date
```

**Soft requirements don't block output.** Note them in the spec as `[TBD]` or `[Not specified]`.

Prompt once:
> "I can generate the spec now. I'm missing [soft reqs]. Want to address these quickly, or should I mark them as TBD?"

---

## Unready Project Detection

If during validation you detect the project isn't ready for a spec:

### Red Flags (any 2+ → suggest Discovery Summary instead)

- problem_statement fails quality check after 2 remediation attempts
- success_metric is purely vanity even after pushback ("lots of users", "people like it")
- Contradictions exist between stakeholders that can't be resolved
- More unknowns than knowns (>50% of hard reqs needed multiple attempts)
- User repeatedly says "I'm not sure" or "we haven't decided"

### Pre-Discovery Detection

If >50% of gaps are problem/user related:
> "It sounds like we're still in discovery phase — we're not yet clear on the problem or users. A spec now would be premature.
> 
> I'd recommend:
> 1. User interviews (5-10 conversations)
> 2. Problem validation research
> 3. Return for spec interview once you can articulate: who has this problem, why it matters, and how you'll measure success.
> 
> Want me to generate a Discovery Summary capturing what we know and the specific questions to answer?"

### Discovery Summary Route

If user chooses Discovery Summary:
```yaml
state:
  flags:
    gate_passed: true  # Special case - passing to discovery output
output_type: discovery
```

Route to [output-core.md](output-core.md) with discovery flag.

---

## Gate Passed

When ALL checks pass:

**Payload update on gate pass:**
```yaml
routing:
  phase: OUTPUT
  current_module: "output-core.md"
  next_action: "Generate spec"
  resume_point: "Gate passed. Generate spec using [template] in [format]."
flags:
  gate_passed: true
  user_confirmed_readback: true
history:
  - timestamp: [now]
    action: "Gate validation passed"
    phase: GATE
    notes: "All hard requirements present and quality-checked. Readback confirmed."
```

> "Everything checks out. Generating the spec now..."

Proceed to [output-core.md](output-core.md).

## Gate Failed — Return to Interview

When validation fails:

**Payload update on gate fail:**
```yaml
routing:
  phase: INTERVIEW
  current_module: "[appropriate interview module]"
  next_action: "Capture missing/failed requirement"
  resume_point: "Gate failed: [specific issue]. Ask: '[remediation prompt]'"
flags:
  gate_passed: false
history:
  - timestamp: [now]
    action: "Gate validation failed"
    phase: GATE
    notes: "Failed check: [which]. Returning to interview."
```

---

## Success Criteria

- [ ] All four hard requirements are non-null (presence check)
- [ ] All four hard requirements pass quality validation
- [ ] Complexity level accurately reflects discovered scope
- [ ] Required sections for complexity level are complete
- [ ] User confirmed readback summary
- [ ] Payload updated with gate results and routing

## Report

| Field | Value |
|-------|-------|
| **Status** | [Passed \| Failed \| Discovery] |
| **Presence Check** | [4/4 \| X/4 missing] |
| **Quality Check** | [4/4 \| X/4 failed] |
| **Escalation** | [None \| Simple→Medium \| Medium→Complex] |
| **Readback** | [Confirmed \| Pending] |
| **Next Module** | [output-core.md \| interview-*.md \| discovery] |

---

## Gate Summary Checklist

Before routing to output, verify:

```
PRESENCE (all must be non-null):
[ ] problem_statement
[ ] success_metric
[ ] must_have_feature
[ ] primary_user

QUALITY (all must pass):
[ ] problem_statement: ≥15 words, has who, has why
[ ] success_metric: has number or comparator
[ ] must_have_feature: has acceptance criteria
[ ] primary_user: specific, not generic

ESCALATION:
[ ] Complexity level is accurate for scope discovered

COMPLETENESS:
[ ] Required sections for complexity level are covered

READBACK:
[ ] User confirmed summary is accurate

→ All pass? Proceed to output-core.md
→ Any fail? Return to interview or route to discovery
```
