---
name: handoff-schema
description: Defines the portable state structure for multi-instance execution.
parent: product-spec-interview
extends: primitives/handoff.md
---

# Handoff Schema

Defines the portable state structure for multi-instance execution. This payload is the single source of truth — each instance reads it on start, updates it on completion.

> **Note:** This schema extends the base [handoff primitive](../../primitives/handoff.md) with skill-specific fields for interview state management.

## Design Principles

1. **Stateless instances** — Any instance can resume from any handoff payload
2. **Single user, multiple sessions** — Context management across conversation boundaries
3. **File-based persistence** — Payload saved as YAML/JSON file between sessions
4. **Subagent compatible** — Can be passed to specialized agents for specific modules

---

## Handoff Payload Schema

```yaml
# handoff.yaml — Save this file between sessions
# Load at start of each instance, save updated version at end

schema_version: "1.0"

# === SESSION METADATA ===
session:
  id: string                    # Unique identifier (e.g., "spec-2025-01-13-checkout-v2")
  project_name: string          # Human-readable project name
  created_at: datetime          # ISO 8601
  updated_at: datetime          # ISO 8601
  instance_count: integer       # How many instances have touched this session

# === ROUTING STATE ===
routing:
  phase: enum                   # OPENING | INTERVIEW | GATE | OUTPUT | COMPLETE | PAUSED
  current_module: string | null # Active module filename (e.g., "interview-full-new.md")
  current_section: integer      # 0-13, section within interview module
  sections_complete: [integer]  # List of completed section numbers
  next_action: string           # Human-readable next step
  resume_point: string          # Specific instruction for next instance

# === CLASSIFICATION STATE ===
classification:
  type: enum | null             # NEW | EXISTING | null
  complexity: enum | null       # SIMPLE | MEDIUM | COMPLEX | null
  format: enum                  # MARKDOWN | NOTION | CONFLUENCE | GDOCS (default: MARKDOWN)

# === HARD REQUIREMENTS ===
# All must be non-null AND pass quality checks before output
hard_reqs:
  problem_statement:
    value: string | null
    quality_passed: boolean
    quality_notes: string | null
  success_metric:
    value: string | null
    quality_passed: boolean
    quality_notes: string | null
  must_have_feature:
    value: string | null
    quality_passed: boolean
    quality_notes: string | null
  primary_user:
    value: string | null
    quality_passed: boolean
    quality_notes: string | null

# === SOFT REQUIREMENTS ===
# Flag if missing, don't block output
soft_reqs:
  technical_constraints: string | null
  key_risk: string | null
  timeline: string | null

# === FLAGS ===
flags:
  escalation_triggered: boolean
  escalation_from: enum | null  # Original complexity before escalation
  checkpoint_offered: boolean
  materials_processed: boolean
  gate_passed: boolean
  output_generated: boolean
  user_confirmed_readback: boolean

# === INTERVIEW DATA ===
# Captured responses organized by section
# This is the actual content that populates the spec
interview_data:
  section_1_problem:
    problem: string | null
    who_affected: string | null
    why_matters: string | null
    cost_of_not_solving: string | null
    previous_attempts: [string] | null
    confidence: enum | null     # HIGH | MEDIUM | LOW
    
  section_2_users:
    personas: 
      - name: string
        goals: string
        workflow: string
        pain_points: [string]
        technical_level: enum   # NOVICE | INTERMEDIATE | EXPERT
        success_looks_like: string
    secondary_users: [string] | null
    
  section_3_stakeholders:
    owner: string | null
    approvers: [string] | null
    consulted: [string] | null
    informed: [string] | null
    blockers: string | null
    skipped: boolean            # True if solo dev
    
  section_4_scope:
    must_have:
      - feature: string
        description: string
        acceptance_criteria: [string]
        depends_on: [string] | null
        confidence: enum
    should_have: [object] | null
    could_have: [object] | null
    out_of_scope: [string]
    non_goals: [string] | null
    
  section_5_technical:
    stack: string | null
    integrations:
      - system: string
        type: string
        owner: string
        notes: string
    performance_targets: object | null
    security_requirements: string | null
    constraints: object | null
    
  section_6_functional:
    features:
      - name: string
        priority: enum          # MUST | SHOULD | COULD
        description: string
        acceptance_criteria: [string]
        examples:
          happy_path: string
          edge_case: string | null
          error_case: string | null
        confidence: enum
        
  section_7_nfr:
    performance: object | null
    reliability: object | null
    usability: object | null
    maintainability: object | null
    
  section_8_data:
    models: string | null
    storage: string | null
    lifecycle: object | null
    privacy: string | null
    skipped: boolean
    
  section_9_api:
    exposed: [object] | null
    consumed: [object] | null
    compatibility: string | null
    skipped: boolean
    
  section_10_dependencies:
    external_services: [object] | null
    libraries: [object] | null
    internal: [object] | null
    
  section_11_risks:
    risks:
      - risk: string
        likelihood: enum        # HIGH | MEDIUM | LOW
        impact: enum
        mitigation: string
        owner: string
        confidence: enum
    assumptions: [object] | null
    anti_patterns: object | null
    
  section_12_validation:
    testing_approach: object | null
    uat: object | null
    rollout_strategy: object | null
    success_validation: object | null
    
  section_13_current_state:       # Existing projects only
    what_works: [object] | null
    pain_points: [object] | null
    technical_debt: [object] | null
    tribal_knowledge: [string] | null
    operational_burden: object | null
    skipped: boolean

# === EXISTING PROJECT SPECIFIC ===
# Only populated for type: EXISTING
existing_project:
  original_problem: string | null
  what_actually_happened: string | null
  keep: [object] | null
  modify: [object] | null
  add: [object] | null
  remove: [object] | null
  migration_plan: object | null

# === OPEN ITEMS ===
open_questions:
  - question: string
    owner: string | null
    due_date: string | null
    status: enum                # OPEN | RESOLVED
    resolution: string | null

conflicts:
  - topic: string
    position_a: string
    position_b: string
    resolution: string | null
    
needs_followup:
  - item: string
    section: integer
    reason: string

# === MATERIALS ===
# Uploaded documents and extracted data
materials:
  uploaded:
    - filename: string
      type: string              # PRD | DESIGN | TECHNICAL | OTHER
      processed: boolean
  extracted_data:
    - source: string
      field: string             # Which field this populated
      value: string
      confidence: enum

# === HISTORY ===
# Audit trail of session progression
history:
  - timestamp: datetime
    instance_id: string | null  # Optional identifier for the instance
    action: string              # What happened
    phase: string               # Phase at time of action
    notes: string | null        # Additional context
```

---

## Payload Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER STARTS                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ handoff.yaml    │
                    │ exists?         │
                    └─────────────────┘
                      │           │
                     NO          YES
                      │           │
                      ▼           ▼
              ┌───────────┐  ┌───────────────┐
              │ CREATE    │  │ LOAD          │
              │ new       │  │ existing      │
              │ payload   │  │ payload       │
              └───────────┘  └───────────────┘
                      │           │
                      └─────┬─────┘
                            ▼
                    ┌─────────────────┐
                    │ READ            │
                    │ routing.phase   │
                    │ routing.resume  │
                    └─────────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │ EXECUTE         │
                    │ appropriate     │
                    │ module          │
                    └─────────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │ UPDATE          │
                    │ payload with    │
                    │ new data        │
                    └─────────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │ SAVE            │
                    │ handoff.yaml    │
                    └─────────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │ Context > 40%?  │
                    │ Section done?   │
                    │ User pause?     │
                    └─────────────────┘
                      │           │
                     YES          NO
                      │           │
                      ▼           ▼
              ┌───────────┐  ┌───────────────┐
              │ END       │  │ CONTINUE      │
              │ session   │  │ in same       │
              │ save file │  │ instance      │
              └───────────┘  └───────────────┘
```

---

## Initial Payload (New Session)

When starting fresh, create this minimal payload:

```yaml
schema_version: "1.0"

session:
  id: "spec-{timestamp}-{slugified-project-name}"
  project_name: "Unnamed Project"
  created_at: "{now}"
  updated_at: "{now}"
  instance_count: 1

routing:
  phase: "OPENING"
  current_module: null
  current_section: 0
  sections_complete: []
  next_action: "Ask classification question (new vs existing)"
  resume_point: "Start opening sequence at Q1"

classification:
  type: null
  complexity: null
  format: "MARKDOWN"

hard_reqs:
  problem_statement: { value: null, quality_passed: false, quality_notes: null }
  success_metric: { value: null, quality_passed: false, quality_notes: null }
  must_have_feature: { value: null, quality_passed: false, quality_notes: null }
  primary_user: { value: null, quality_passed: false, quality_notes: null }

soft_reqs:
  technical_constraints: null
  key_risk: null
  timeline: null

flags:
  escalation_triggered: false
  escalation_from: null
  checkpoint_offered: false
  materials_processed: false
  gate_passed: false
  output_generated: false
  user_confirmed_readback: false

interview_data: {}

existing_project: {}

open_questions: []
conflicts: []
needs_followup: []

materials:
  uploaded: []
  extracted_data: []

history:
  - timestamp: "{now}"
    instance_id: null
    action: "Session created"
    phase: "OPENING"
    notes: null
```

---

## Context Management Rules

Target: Keep context under 40% of window.

### When to End Session and Save

1. **Section boundary reached** — Natural breakpoint
2. **Context approaching 35%** — Buffer before limit
3. **User requests pause** — Explicit checkpoint
4. **Complexity escalation** — Good time to reset context
5. **After gate validation** — Clean break before output

### Resume Instructions

The `routing.resume_point` field contains a specific instruction for the next instance:

```yaml
# Examples of good resume_point values:

# After opening
resume_point: "Classification complete. Begin interview-full-new.md at Section 1."

# Mid-interview
resume_point: "Section 3 (Stakeholders) complete. Begin Section 4 (Scope). User mentioned 'payment integration' — probe this."

# At gate
resume_point: "All sections complete. Run gate validation. hard_reqs.success_metric needs quality check."

# After gate
resume_point: "Gate passed. Generate output using full-new template in Markdown format."
```

---

## Subagent Handoff

When delegating to a specialized subagent:

```yaml
# Parent agent creates scoped payload for subagent
subagent_task:
  agent_type: "technical-depth"  # Or: "risk-analysis", "user-research", etc.
  scope: "section_5_technical"
  input_context:
    # Minimal context the subagent needs
    project_summary: "E-commerce checkout optimization"
    relevant_sections: [section_1_problem, section_4_scope]
  expected_output:
    # What parent expects back
    fields: [stack, integrations, performance_targets, constraints]
    
# Subagent returns populated fields
# Parent agent merges into main payload
```

---

## File Naming Convention

```
handoff-{project-slug}-{session-id}.yaml

Examples:
handoff-checkout-optimization-20250113a.yaml
handoff-invoice-system-20250113b.yaml
```

For in-progress work, append status:
```
handoff-checkout-optimization-20250113a.INTERVIEW.yaml
handoff-checkout-optimization-20250113a.GATE.yaml
handoff-checkout-optimization-20250113a.COMPLETE.yaml
```
