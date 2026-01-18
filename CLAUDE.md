# Agentic OS: Thread-Based Engineering

This repository uses a multi-agent workflow system to solve **Context Rot** and **Agent Hallucination**.

## Quick Start

1. **Identify your thread type** based on task complexity:
   - **Base (B)**: Simple tasks → single agent → human review
   - **Chained (C)**: High-risk work → phased handoffs → verification gates
   - **Long (L)**: Large refactors → auto-fix loops → 50+ tool calls

2. **Select your agent**:
   - `@developer` - Implementation and coding tasks
   - `@verifier` - Validation and auditing (Two-Key system)
   - `@doc-explorer` - Research and documentation mapping

3. **Follow the Two-Key rule**: No code is "Done" until the Verifier provides a PASS grade.

## Key Principles

- **Atomic commits**: Break work into small, verifiable chunks
- **Zero-trust verification**: Verifier re-runs all tests independently
- **Structured handoffs**: Use `primitives/handoff.md` between phases

## Registry

See [registry.md](registry.md) for the complete capability manifest including all agents, commands, skills, and primitives.
