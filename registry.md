# Agentic Registry: Thread-Based Engineering OS

This registry serves as the central manifest for all autonomous capabilities within the repository.

## 1. Agents (Personas)
- **[Lead Developer](agents/developer.md)**: The **Optimistic Creator**. Handles high-autonomy implementation and refactor threads.
- **[Senior Verifier](agents/verifier.md)**: The **Pessimistic Auditor**. Hardened "Review Node" that validates all implementation before thread closure.
- **[Doc-Explorer](agents/doc-explorer.md)**: The **Context Architect**. Specializes in Exploration Threads and building repository knowledge maps.

## 2. Commands (Thread-Specific Skills)
- **[Auto-Fix-Loop](commands/auto-fix-loop.md)**: **Long Thread (L)** engine. Automates the "test-fail-fix" cycle until success.
- **[Handoff-to-Verifier](commands/handoff-to-verifier.md)**: **Chained Thread (C)** engine. Automates the transition from Implementation to Review.
- **[Sync-With-Main](commands/sync-with-main.md)**: **Base Thread (B)** utility. Synchronizes the local environment with the main branch.

## 3. Skills (Task-Specific Logic)
- **[DocGen](skills/documentation/SKILL.md)**: Generates JSDoc/Docstrings for identified code blocks.
- **[SpecGen](skills/testing/SKILL.md)**: Creates Vitest/Jest spec files for new implementations.

## 4. Core Primitives (The Rules)
- **[Thread Catalog](primitives/patterns/thread-catalog.md)**: Defines the 7 operational modes and trust levels.
- **[Thread Handoff](primitives/handoff.md)**: The standard context bridge for all agent-to-agent communication.
- **[Standard Patterns](primitives/patterns/agentic-patterns.md)**: Core pillars and formatting standards for the "Core 4" framework.
- **[Success Criteria](primitives/patterns/success-criteria.md)**: Reusable verification checklists for thread completion.
