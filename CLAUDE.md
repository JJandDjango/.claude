# Agentic OS: Thread-Based Engineering

This repository uses a multi-agent workflow system to solve **Context Rot** and **Agent Hallucination**.

<directives>
DELEGATE @developer WHEN implement, code, write, fix, add, refactor, build, create, update, modify
DELEGATE @verifier WHEN verify, audit, review, validate, test, check, confirm, inspect
DELEGATE @doc-explorer WHEN find, search, explore, understand, document, map, where, how, explain, locate
DEFAULT @orchestrator
CHAIN implementation: @doc-explorer → @developer → @verifier
CHAIN research: @doc-explorer → @orchestrator
REQUIRE agents/orchestrator.md ON session_start
</directives>

## How to Use Directives

The directives block above defines routing rules. Apply them as follows:

1. **On session start**: Load files specified by `REQUIRE ... ON session_start`
2. **On user request**: Scan input for keywords in `DELEGATE ... WHEN` rules
3. **Match found**: Route to the specified `@agent`
4. **No match**: Route to the `DEFAULT` agent
5. **Complex task**: Use `CHAIN` sequences for multi-phase work

### Directive Syntax

| Directive | Purpose | Example |
|-----------|---------|---------|
| `DELEGATE` | Route by keyword | `DELEGATE @developer WHEN fix, code` |
| `DEFAULT` | Fallback agent | `DEFAULT @orchestrator` |
| `CHAIN` | Multi-agent sequence | `CHAIN impl: @a → @b → @c` |
| `REQUIRE` | Auto-load file | `REQUIRE file ON trigger` |

## Session Start

At the beginning of each session, adopt the **Orchestrator** persona:

1. Read `agents/orchestrator.md`
2. Operate as the Orchestrator — coordinate specialists, don't implement directly
3. Confirm with: "Operating as **Orchestrator**..."

## Quick Start

1. **Identify your thread type** based on task complexity:
   - **Base (B)**: Simple tasks → single agent → human review
   - **Chained (C)**: High-risk work → phased handoffs → verification gates
   - **Long (L)**: Large refactors → auto-fix loops → 50+ tool calls

2. **The Orchestrator routes to specialists**:
   - `@developer` - Implementation and coding tasks
   - `@verifier` - Validation and auditing (Two-Key system)
   - `@doc-explorer` - Research and documentation mapping

3. **Follow the Two-Key rule**: No code is "Done" until the Verifier provides a PASS grade.

## Key Principles

- **Orchestrator-first**: The main agent coordinates, specialists execute
- **Atomic commits**: Break work into small, verifiable chunks
- **Zero-trust verification**: Verifier re-runs all tests independently
- **Structured handoffs**: Use `primitives/handoff.md` between phases

## Registry

See [registry.md](registry.md) for the complete capability manifest including all agents, commands, skills, and primitives.
