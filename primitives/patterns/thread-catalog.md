# Primitive: Thread Catalog (Operational Modes)
**Purpose**: To define the operational parameters, risk levels, and trust requirements for different engineering workstreams.

## 1. Base Thread (Standard)
- **Structure**: 1 Human Prompt -> Agent Loop -> 1 Human Review.
- **Usage**: General tasks, small feature requests, or individual file edits.
- **Trust Level**: Low. Requires 100% human verification of all tool calls.

## 2. Parallel Threads (P)
- **Structure**: Multiple independent Base Threads running simultaneously across different terminals or agents.
- **Usage**: Bulk updates (e.g., updating 20 separate documentation files) or broad codebase audits.
- **Constraint**: No cross-thread dependencies; each task must be atomic.

## 3. Chained Threads (C)
- **Structure**: High-risk work broken into sequential phases with mandatory handoffs and human checkpoints.
- **Usage**: Major architectural changes or migrations.
- **Protocol**: Requires use of `primitives/handoff.md` after every phase.

## 4. Fusion Threads (F)
- **Structure**: One prompt executed by 2-3 different models (e.g., Claude 3.5 and Gemini 1.5).
- **Usage**: High-stakes logic or security-sensitive code.
- **Protocol**: A "Synthesizer" agent must compare outputs and highlight discrepancies.

## 5. Big Threads (B)
- **Structure**: A meta-prompt that triggers hidden sub-agents to perform specialized work.
- **Usage**: High-level commands like "Fix all accessibility issues in the dashboard."
- **Focus**: The user only sees the final result, not the internal sub-agent coordination.

## 6. Long Threads (L)
- **Structure**: High-autonomy runs involving 50-200+ tool calls with minimal human intervention.
- **Usage**: Refactoring large modules or complex debugging.
- **Requirement**: Must use "Ralph Wiggum" auto-fix loops for self-correction.

## 7. Zero-Touch Threads (Z)
- **Structure**: Target state where automated validation (Verifier Agent) replaces human review entirely.
- **Usage**: Low-risk maintenance, styling, and documented repetitive tasks.
- **Trust Level**: Critical. Requires 100% test coverage and a passing Verifier grade.