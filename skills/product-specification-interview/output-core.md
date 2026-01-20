---
name: product-spec-interview-output
description: Handles template selection, format adaptation, and spec generation.
parent: product-spec-interview
tools: Read, Write, Glob
---

# Output Core: Selection & Generation Logic

This module handles output selection, format adaptation, and versioning. Templates are loaded from [templates/](templates/).

**Multi-instance:** This module reads from the handoff payload. All interview data needed for spec generation is in `interview_data`. This module can run in a fresh instance with only the payload as context.

## Entry Check

```
ON MODULE ENTRY:
    1. READ routing.phase (should be OUTPUT)
    2. READ classification for template selection
    3. READ interview_data for spec content
    4. READ hard_reqs and soft_reqs for requirements
    5. READ flags for any special conditions (partial_spec, discovery)
    6. GENERATE spec from payload data
```

## Output Flow

```
1. SELECT    → Choose template based on state
2. ADAPT     → Apply format-specific transformations
3. VERSION   → Assign version number and status
4. GENERATE  → Load template, populate with interview data
5. PRESENT   → Show summary first, offer full spec
```

---

## Step 1: Template Selection

Based on state, select the appropriate template:

```
IF output_type = discovery:
    → templates/summary.md#discovery-summary
    
ELSE IF complexity = simple:
    → templates/lite.md
    
ELSE IF type = new AND complexity ≥ medium:
    → templates/full-new.md
    
ELSE IF type = existing AND complexity ≥ medium:
    → templates/full-existing.md
```

### Additional Components

Include these based on conditions:

| Condition | Additional Template |
|-----------|---------------------|
| Always | templates/summary.md#executive-summary (present first) |
| complexity = complex | templates/diff-graph.md#dependency-graph |
| Updating existing spec | templates/diff-graph.md#diff-summary |

---

## Step 2: Format Adaptation

Apply transformations based on `state.format`:

### Markdown (Default)
- No transformations needed
- Fenced code blocks for code/config
- Mermaid diagrams render natively

### Notion
- Convert blockquotes to callout blocks: `> ⚠️ **Warning:** text`
- Convert long sections to toggle blocks: `<details><summary>Title</summary>content</details>`
- Replace Mermaid with: "Dependency diagram: paste code at [mermaid.live](https://mermaid.live)"
- Use database tables for feature lists where appropriate

### Confluence
- Add status macros for priority: `{status:colour=Green|title=Must-Have}`
- Use panel macros for risks: `{panel:title=Risk|borderColor=#ff0000}content{panel}`
- Use expand macros for detailed sections: `{expand:title=Details}content{expand}`
- Replace Mermaid with: "See attached diagram or create at mermaid.live"

### Google Docs
- Simplify to basic formatting only
- Bold headers (no markdown #)
- Simple tables (no merged cells)
- Add at document top: "Table of Contents: Insert > Table of contents"
- Replace Mermaid with: "Dependency diagram available separately"
- No code blocks — use monospace font for technical terms

### Linear/Jira (Ticket Mode)
- Break features into individual ticket descriptions
- Focus on: Title, Description, Acceptance Criteria
- Link to full spec document
- Use ticket-appropriate formatting

---

## Step 3: Versioning

### Version Number Assignment

| Context | Version |
|---------|---------|
| First draft | 0.1 |
| Subsequent drafts | 0.2, 0.3, ... 0.8 |
| Draft complete, ready for review | 0.9 |
| Release candidate | 1.0-RC |
| First approved version | 1.0 |
| Minor updates post-approval | 1.1, 1.2, ... |
| Major scope change | 2.0 |

### Status Assignment

| Status | When |
|--------|------|
| Draft | Initial creation, iterating |
| In Review | Sent for stakeholder feedback |
| Changes Requested | Feedback received, updates needed |
| RC | Release candidate, final review |
| Approved | Signed off, ready for implementation |
| Superseded | Replaced by newer version |

**Default for new specs:** Version 0.1, Status Draft

### Revision Handling

When updating an existing spec:
1. Increment version appropriately
2. Generate Diff Summary (see templates/diff-graph.md)
3. Update Change Log in spec
4. Preserve previous version reference

---

## Step 4: Template Population

Load the selected template and populate with interview data.

### Data Mapping

Map state and interview responses to template fields:

```yaml
mapping:
  # From state.hard_reqs
  problem_statement → Problem section
  success_metric → Success Metrics table
  must_have_feature → Must-Have Features list
  primary_user → User Personas section
  
  # From state.soft_reqs
  technical_constraints → Technical Context section
  key_risk → Risks & Mitigations table
  timeline → Timeline section
  
  # From interview sections
  section_1 → Problem Statement
  section_2 → Users & Context
  section_3 → Stakeholders (if captured)
  section_4 → Scope
  section_5 → Technical Context
  section_6 → Functional Requirements
  section_7 → Non-Functional Requirements
  section_8 → Data Specifications (if applicable)
  section_9 → API & Contracts (if applicable)
  section_10 → Dependencies
  section_11 → Risks
  section_12 → Validation Strategy
  section_13 → Current State (existing projects only)
```

### Handling Missing Data

| Data Status | Template Handling |
|-------------|-------------------|
| Captured | Populate normally |
| Not captured (soft req) | Insert `[TBD]` or `[Not specified]` |
| Not applicable | Omit section entirely |
| Marked for follow-up | Insert `[Needs follow-up: reason]` |
| Conflicting | Insert `[Conflict: A says X, B says Y — resolution pending]` |

### Source Attribution

When data came from uploaded materials:
- Add inline: `[Source: uploaded PRD]`
- Add to metadata: `Sources: [list of documents]`

---

## Step 5: Presentation

### Always Present Executive Summary First

After generating full spec:

1. Output Executive Summary (from templates/summary.md)
2. Prompt: "Here's the executive summary. Want the full detailed spec?"
3. If yes → output full spec
4. If no → confirm they can request it later

### Full Spec Delivery

When delivering full spec:

1. Output complete spec in selected format
2. End with: "Any sections you'd like me to expand or clarify?"

### Revision Delivery

For spec updates:

1. Output Executive Summary (updated)
2. Output Diff Summary (what changed)
3. Prompt: "Should I show the full updated spec, or just the changed sections?"

---

## Special Outputs

### Discovery Summary

When `output_type = discovery`:

1. Load templates/summary.md#discovery-summary
2. Populate with:
   - What's known (partial interview data)
   - What's missing (gaps identified)
   - Assumptions made
   - Recommended next steps
   - Resume trigger (when to return for full spec)
3. Do NOT offer full spec — project isn't ready

### Partial Spec

When user requests spec despite incomplete sections:

1. Generate normally but:
   - Flag incomplete sections prominently: `## [Section Name] — INCOMPLETE`
   - Add to metadata: `Completeness: Partial — missing [sections]`
   - Add warning at top: "⚠️ This spec has incomplete sections. Review flagged areas before implementation."

---

## Template Reference

| Template | Location | Contents |
|----------|----------|----------|
| Executive Summary | [templates/summary.md#executive-summary](templates/summary.md) | One-page overview |
| Discovery Summary | [templates/summary.md#discovery-summary](templates/summary.md) | Pre-spec capture |
| Lite Spec | [templates/lite.md](templates/lite.md) | Simple project template |
| Full New | [templates/full-new.md](templates/full-new.md) | New project template |
| Full Existing | [templates/full-existing.md](templates/full-existing.md) | Existing project template |
| Diff Summary | [templates/diff-graph.md#diff-summary](templates/diff-graph.md) | Change tracking |
| Dependency Graph | [templates/diff-graph.md#dependency-graph](templates/diff-graph.md) | Feature dependencies |

---

## Post-Output Checklist

After generating any output:

```
[ ] Executive summary presented first
[ ] Format adaptations applied
[ ] Version and status assigned
[ ] Missing data marked appropriately
[ ] Sources attributed
[ ] User prompted for next action
```

**Payload update on output complete:**
```yaml
routing:
  phase: COMPLETE
  current_module: null
  next_action: "Session complete"
  resume_point: "Spec generated and delivered. Session complete."
flags:
  output_generated: true
session:
  updated_at: [now]
history:
  - timestamp: [now]
    action: "Spec generated"
    phase: OUTPUT
    notes: "Template: [template]. Format: [format]. Version: [version]."
```

## Session Complete

When spec is generated and delivered:

> "Here's your spec. Let me know if you'd like me to:
> - Expand any section
> - Adjust the format
> - Start a revision
> 
> The session data is saved — you can reference it for future updates."

**Final payload state:**
```yaml
routing:
  phase: COMPLETE
flags:
  gate_passed: true
  output_generated: true
session:
  instance_count: [total instances used]
```

Save final payload with `.COMPLETE` suffix for reference.

## Success Criteria

- [ ] Correct template selected based on classification
- [ ] Format adaptations applied for target platform
- [ ] Version number and status assigned appropriately
- [ ] All hard requirements populated in spec
- [ ] Missing/incomplete data clearly marked
- [ ] Executive summary presented first
- [ ] User prompted for clarification or expansion
- [ ] Payload updated with output_generated flag

## Report

| Field | Value |
|-------|-------|
| **Status** | [Complete \| Partial \| Discovery] |
| **Template** | [lite \| full-new \| full-existing \| discovery] |
| **Format** | [Markdown \| Notion \| Confluence \| Google Docs \| Linear/Jira] |
| **Version** | [X.Y] |
| **Spec Status** | [Draft \| In Review \| RC \| Approved] |
| **Completeness** | [Full \| Partial - missing sections] |
| **Output File** | [filename or inline] |
