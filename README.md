# Agentic OS: Thread-Based Engineering Framework

A high-autonomy **Agentic Operating System** for Claude Code that coordinates specialist agents through structured workflows. Built on **Thread-Based Engineering** principles to eliminate context rot and agent hallucination.

## Intent

This framework solves two core problems:

- **Context Rot**: Information degrades as it passes between prompts and agents
- **Agent Hallucination**: LLMs confirm their own work and "pass their own tests"

The solution: an **Orchestrator** that delegates to specialists, with a **Two-Key System** (Developer + Verifier) ensuring every code change is independently validated.

---

## Quick Start

### 1. Session Initialization

At the start of each Claude Code session, the main agent adopts the Orchestrator persona:

```
Read agents/orchestrator.md and operate as the Orchestrator.
```

The Orchestrator will confirm: *"Operating as Orchestrator..."*

### 2. Just Describe Your Task

The Orchestrator automatically:
- Classifies the work and selects the appropriate thread type
- Delegates to specialist agents (`@developer`, `@verifier`, `@doc-explorer`)
- Enforces verification gates before reporting completion
- Synthesizes results for you

### 3. The Two-Key Rule

No code is "Done" until the Verifier provides a **PASS** grade. The Verifier independently re-runs all tests—it never trusts the Developer's logs.

---

## Architecture

### The Orchestrator Model

```
┌─────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                       │
│         (Coordinates • Routes • Synthesizes)            │
└─────────────────────────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │  Developer  │   │  Verifier   │   │ Doc-Explorer│
   │ (Implement) │──▶│  (Audit)    │   │  (Research) │
   └─────────────┘   └─────────────┘   └─────────────┘
```

- **Orchestrator**: Routes tasks, enforces gates, never implements directly
- **Developer**: Optimistic creator—writes code, runs tests, produces handoffs
- **Verifier**: Pessimistic auditor—zero-trust validation, independent test runs
- **Doc-Explorer**: Context architect—maps codebases, maintains documentation

### Thread Types

Work is categorized into thread types that set autonomy levels and verification requirements:

| Thread | Description | Verification |
|--------|-------------|--------------|
| **Base (B)** | Simple tasks, single-file changes | Human review |
| **Parallel (P)** | Multiple independent tasks running simultaneously | Per-task |
| **Chained (C)** | Multi-phase work with mandatory handoffs | Gate per phase |
| **Long (L)** | Large refactors, 50+ tool calls, auto-fix loops | Automated + final |
| **Zero-Touch (Z)** | Fully automated with 100% test coverage | Verifier only |
| **Fusion (F)** | Cross-model validation *(planned)* | Multi-model consensus |

---

## Repository Structure

```
.claude-master/
├── CLAUDE.md                 # Entry point — session initialization
├── registry.md               # Capability manifest for all components
├── settings.json             # Configuration defaults
│
├── agents/                   # Specialist Personas
│   ├── orchestrator.md       # Default coordinator (adopt at session start)
│   ├── developer.md          # Implementation specialist
│   ├── verifier.md           # Audit specialist (zero-trust)
│   └── doc-explorer.md       # Research & documentation specialist
│
├── primitives/               # System Rules
│   ├── handoff.md            # Context bridge template for agent transitions
│   └── patterns/
│       ├── thread-catalog.md # Thread type definitions
│       ├── agentic-patterns.md # Core 4 framework & formatting standards
│       └── success-criteria.md # Verification checklists by task type
│
├── commands/                 # Executable Workflows
│   ├── auto-fix-loop.md      # Test-fail-fix cycle for Long Threads
│   ├── handoff-to-verifier.md # Developer → Verifier transition
│   └── sync-with-main.md     # Git sync utility
│
└── skills/                   # Task-Specific Expertise
    ├── documentation/SKILL.md # JSDoc/Docstring generation
    └── testing/SKILL.md       # Test spec generation
```

---

## Core Concepts

### The Core 4 Pillars

Every agentic system has four tunable dimensions:

1. **Context**: Information available to the agent (files, history, handoffs)
2. **Prompt**: The instructions defining behavior (agent personas, skills)
3. **Tools**: External capabilities (Bash, Read, Write, Edit, Task)
4. **Models**: The underlying reasoning engine (Sonnet, Haiku, etc.)

### Structured Handoffs

When work transitions between agents (especially Developer → Verifier), the handoff primitive captures:

- Thread metadata and confidence score
- Executive summary of changes
- Modified files and side effects
- Verification requirements and commands

This prevents context rot by making transitions explicit and auditable.

### Auto-Fix Loops

For Long Threads, the auto-fix-loop command enables high-autonomy operation:

1. Run tests
2. If failure: analyze error, apply fix, increment counter
3. Repeat until success or max attempts reached

This eliminates the "Ralph Wiggum" anti-pattern—agents that cheerfully persist through failures without self-awareness.

---

## Usage Examples

### Simple Implementation

> "Add input validation to the signup form"

Orchestrator delegates to Developer → Developer implements → Verifier audits → PASS/FAIL

### Complex Refactor

> "Migrate the authentication system from sessions to JWT"

Orchestrator:
1. Decomposes into phases (research → plan → implement → migrate data → verify)
2. Runs as Chained Thread with handoffs between each phase
3. Enforces verification gate after implementation phases

### Documentation Update

> "Update the API docs to reflect the new endpoints"

Orchestrator delegates to Doc-Explorer (no verification gate for docs-only changes)

---

## Compliance

- All agents must follow patterns in `primitives/patterns/agentic-patterns.md`
- New capabilities must be registered in `registry.md`
- Code changes require Verifier PASS before completion
- Handoffs must use the `primitives/handoff.md` template

---

## Customization

Edit `settings.json` to adjust:

- Default model for agents
- Auto-fix loop max attempts
- Thread-specific trust levels and requirements

Add new skills in `skills/[name]/SKILL.md` following the standard template.
