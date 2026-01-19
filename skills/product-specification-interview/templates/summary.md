# Summary Templates

Contains Executive Summary (all projects) and Discovery Summary (unready projects).

---

## Executive Summary

**Always generated first, regardless of project type or complexity.**

```markdown
# [Product Name] — Spec Summary

**Version:** [X.Y]
**Status:** [Draft | In Review | Changes Requested | RC | Approved | Superseded]
**Type:** [New Project | Existing Project Revision]
**Complexity:** [Simple | Medium | Complex]
**Owner:** [Name]
**Last Updated:** [Date]
**Format:** [Target format]

## One-Liner

[What this is in one sentence — the elevator pitch]

## Problem

[2-3 sentences on the problem and why it matters. Include: who has it, what the impact is, why now.]

## Solution

[2-3 sentences on the approach. What are we building and why this approach?]

## Success Metrics

| Metric | Target | Confidence |
|--------|--------|------------|
| [Primary metric] | [Specific target] | High/Med/Low |
| [Secondary metric] | [Specific target] | High/Med/Low |

## Scope (MVP)

**Must Have:**
- [Feature 1] — [one-line description]
- [Feature 2] — [one-line description]

**Should Have:**
- [Feature 3] — [one-line description]

**Out of Scope:**
- [Exclusion 1]
- [Exclusion 2]

## Key Risks

1. **[Risk 1]** — Mitigation: [approach]
2. **[Risk 2]** — Mitigation: [approach]

## Timeline

| Milestone | Target Date |
|-----------|-------------|
| [Milestone 1] | [Date] |
| [Milestone 2] | [Date] |
| Launch | [Date] |

## Open Questions

| Question | Owner | Due |
|----------|-------|-----|
| [Question 1] | [Who] | [When] |
| [Question 2] | [Who] | [When] |

---

*Full spec available on request.*
```

### Executive Summary Guidelines

- **One page maximum** — this is a summary, not the spec
- **Lead with the one-liner** — reader should understand the project in 10 seconds
- **Metrics must be quantified** — no "improve user satisfaction"
- **Risks should have mitigations** — don't just list problems
- **Open questions need owners** — unowned questions don't get answered

---

## Discovery Summary

**Generated when project isn't ready for full spec.**

```markdown
# [Project Name] — Discovery Summary

**Date:** [Date]
**Status:** Paused — needs [specific gap] before full spec
**Facilitator:** [Who ran this session]
**Participants:** [Who was interviewed]

## Purpose

This document captures current understanding of [project name]. It is NOT a specification — key questions remain unanswered. Use this to guide discovery work before returning for a full spec interview.

## What We Know

### Problem Area
[General domain and context — what space are we in?]

### Potential Users
[Who might use this, based on current understanding]

### Initial Feature Ideas
- [Idea 1]
- [Idea 2]
- [Idea 3]

### Constraints Identified
- [Constraint 1]
- [Constraint 2]

## What's Missing

| Gap | Why It Matters | Suggested Next Step | Owner |
|-----|----------------|---------------------|-------|
| [Gap 1] | [Impact if unresolved] | [Specific action] | [Who] |
| [Gap 2] | [Impact if unresolved] | [Specific action] | [Who] |
| [Gap 3] | [Impact if unresolved] | [Specific action] | [Who] |

## Assumptions Made

These assumptions were made during the session. If any are wrong, conclusions may change.

| Assumption | Risk if Wrong | How to Validate |
|------------|---------------|-----------------|
| [Assumption 1] | [Impact] | [Validation method] |
| [Assumption 2] | [Impact] | [Validation method] |

## Recommended Next Steps

1. **[Action 1]** — [Who] — [By when]
   - [Details/context]
   
2. **[Action 2]** — [Who] — [By when]
   - [Details/context]

3. **[Action 3]** — [Who] — [By when]
   - [Details/context]

## Resume Spec Interview When

Return for a full specification interview when you can answer:

- [ ] Who specifically has this problem? (Not "users" — specific roles/personas)
- [ ] What is the measurable cost of not solving it?
- [ ] How will you know if the solution worked? (Specific metric + target)
- [ ] What is the ONE feature that must work for this to be useful?

**Trigger:** [Specific event — e.g., "User interviews complete" or "Budget approved" or "Stakeholder alignment achieved"]

---

## Session Notes

[Raw notes, quotes, or observations from the interview that might be useful later]
```

### Discovery Summary Guidelines

- **Be specific about gaps** — "Need user research" is useless; "Need to interview 5 warehouse managers about their current workflow" is actionable
- **Assign owners** — Every gap and next step needs a name attached
- **Set a resume trigger** — Make it concrete and verifiable
- **Preserve raw notes** — Context gets lost; capture direct quotes and observations
- **Don't pretend certainty** — This is explicitly incomplete; frame it that way
