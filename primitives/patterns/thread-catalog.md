---
name: thread-catalog
description: Defines operational parameters, risk levels, and trust requirements for different thread types (Base, Parallel, Chained, etc.).
reference: true
---

# Thread Catalog (Operational Modes)

<purpose>
Define the operational parameters, risk levels, and trust requirements for different engineering workstreams.
</purpose>

<context>
Threads are the fundamental unit of agentic work. Each thread type has different autonomy levels, verification requirements, and use cases.
</context>

<examples>
## 1. Base Thread (B)
- **Structure**: 1 Human Prompt -> Agent Loop -> 1 Human Review
- **Usage**: General tasks, small feature requests, or individual file edits
- **Trust Level**: Low. Requires 100% human verification of all tool calls

## 2. Parallel Threads (P)
- **Structure**: Multiple independent Base Threads running simultaneously
- **Usage**: Bulk updates (e.g., updating 20 documentation files) or broad codebase audits
- **Constraint**: No cross-thread dependencies; each task must be atomic

## 3. Chained Threads (C)
- **Structure**: High-risk work broken into sequential phases with mandatory handoffs
- **Usage**: Major architectural changes or migrations
- **Protocol**: Requires use of `primitives/handoff.md` after every phase

## 4. Fusion Threads (F) — Planned/Aspirational
- **Structure**: One prompt executed by 2-3 different models (e.g., Claude and Gemini)
- **Usage**: High-stakes logic or security-sensitive code
- **Protocol**: A "Synthesizer" agent must compare outputs and highlight discrepancies
- **Status**: Not yet implemented. Requires external orchestration

## 5. Big Threads (B)
- **Structure**: A meta-prompt that triggers hidden sub-agents to perform specialized work
- **Usage**: High-level commands like "Fix all accessibility issues in the dashboard"
- **Focus**: User only sees the final result, not internal sub-agent coordination

## 6. Long Threads (L)
- **Structure**: High-autonomy runs involving 50-200+ tool calls with minimal human intervention
- **Usage**: Refactoring large modules or complex debugging
- **Requirement**: Must use auto-fix loops for self-correction

## 7. Zero-Touch Threads (Z)
- **Structure**: Target state where automated validation (Verifier Agent) replaces human review
- **Usage**: Low-risk maintenance, styling, and documented repetitive tasks
- **Trust Level**: Critical. Requires 100% test coverage and a passing Verifier grade
</examples>
