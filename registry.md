# Agentic Registry: Thread-Based Engineering OS

This registry serves as the central manifest for all autonomous capabilities within the repository.

## 1. Agents (Personas)
- **[Lead Developer](agents/developer.md)**: The **Optimistic Creator**. Handles high-autonomy implementation and refactor threads.
- **[Senior Verifier](agents/verifier.md)**: The **Pessimistic Auditor**. Hardened "Review Node" that validates all implementation before thread closure.
- **[Doc-Explorer](agents/doc-explorer.md)**: The **Context Architect**. Specializes in Exploration Threads and building repository knowledge maps.

## 2. Skills (Task-Specific Logic)

### Thread Engines
- **[Auto-Fix-Loop](skills/auto-fix-loop/SKILL.md)**: **Long Thread (L)** engine. Automates the "test-fail-fix" cycle until success or max retries.
- **[Handoff-to-Verifier](skills/handoff-to-verifier/SKILL.md)**: **Chained Thread (C)** engine. Automates the transition from Implementation to Review.

### Utilities
- **[Sync-With-Main](skills/sync-with-main/SKILL.md)**: **Base Thread (B)** utility. Synchronizes the local branch with main.
- **[Refactor](skills/refactor/SKILL.md)**: **Base Thread (B)** analyzer. Reviews .md files against repository standards.

### Generators
- **[DocGen](skills/documentation/SKILL.md)**: Generates JSDoc/Docstrings for identified code blocks.
- **[SpecGen](skills/testing/SKILL.md)**: Creates Vitest/Jest spec files for new implementations.
- **[Code-Documentation-Generator](skills/code-documentation-generator/SKILL.md)**: **Long Thread (L)** generator. Creates progressive disclosure documentation for C# codebases.

### Interview Skills
- **[Product-Spec-Interview](skills/product-specification-interview/SKILL.md)**: **Chained Thread (C)** skill. Generates product specifications through structured interviews with multi-phase validation.

## 3. Core Primitives (The Rules)
- **[Thread Catalog](primitives/patterns/thread-catalog.md)**: Defines the 7 operational modes and trust levels.
- **[Thread Handoff](primitives/handoff.md)**: The standard context bridge for all agent-to-agent communication.
- **[Standard Patterns](primitives/patterns/agentic-patterns.md)**: Core pillars and formatting standards for the "Core 4" framework.
