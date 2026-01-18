# Agentic OS: Thread-Based Engineering Framework

This repository is a high-autonomy **Agentic Operating System** designed to facilitate complex software engineering tasks through structured agent coordination. Built on the principles of **Thread-Based Engineering**, it moves beyond simple prompting into a deterministic, multi-agent workflow.

## 🎯 Intent
The primary goal of this repository is to solve **Context Rot** and **Agent Hallucination**. By breaking work into specialized "Threads" and utilizing a "Two-Key" system (Developer + Verifier), we ensure that every code change is provably correct and architecturally sound.

---

## 🧵 Thread-Based Engineering
We categorize work into seven distinct thread types to optimize for speed, safety, and autonomy.

| Thread Type | Description | Trust Level |
| :--- | :--- | :--- |
| **Base (B)** | 1 Prompt -> Agent Execution -> 1 Human Review. | Low |
| **Parallel (P)** | Multiple independent threads running simultaneously for scale. | Medium |
| **Chained (C)** | High-risk work broken into phases with mandatory handoffs. | High |
| **Fusion (F)** | Cross-referencing outputs from multiple models (Claude/Gemini). | Critical |
| **Big (B)** | Meta-threads where a master agent coordinates hidden sub-agents. | Variable |
| **Long (L)** | High-autonomy runs (50+ tool calls) using auto-fix loops. | High |
| **Zero-Touch (Z)** | Target state: Automated Verifier replaces human review entirely. | Ultimate |

---

## 🏗️ Repository Structure
This project follows the **Core 4** pillar architecture (Context, Prompt, Tools, Models).

```text
Root/
├── agents/                 # Specialized Personas (The "Brains")
│   ├── developer.md        # Optimistic Implementation Agent
│   ├── verifier.md         # Pessimistic Audit Agent (The Firewall)
│   └── doc-explorer.md     # Context & Knowledge Map Agent
├── primitives/             # The Rules of the System
│   ├── patterns/           
│   │   ├── thread-catalog.md # Definitions of Thread physics
│   │   └── agentic-patterns.md # Formatting & Core 4 standards
│   └── handoff.md          # The "DNA" bridge between threads
├── commands/               # Thread-Specific Skills (The Engine)
│   ├── auto-fix-loop.md    # Ralph Wiggum self-correction loop
│   └── handoff-to-verifier.md # Automation for Chained Threads
├── skills/                 # Task-Specific Expertise (The Tools)
│   ├── documentation/      # SKILL.md for JSDoc/Docstrings
│   └── testing/            # SKILL.md for Spec generation
└── registry.json           # Machine-readable capability manifest
```

## 🚀 Usage Details
1. Initializing a Thread
To start a new task, identify the required Thread Type from the thread-catalog.md. For research, call the Doc-Explorer. For coding, call the Lead Developer.

2. The Handoff Protocol
When an agent completes a phase in a Chained Thread, it must execute the handoff-to-verifier command. This populates the primitives/handoff.md file, providing the Senior Verifier with the necessary technical context for an audit.

3. Verification (The Two-Key System)
No code is considered "Done" until the Senior Verifier provides a PASS grade. The Verifier is trained to ignore Developer logs and re-run all tests independently to ensure zero-hallucination results.

4. Maximizing Autonomy
For large refactors, use the Auto-Fix-Loop command. This enables Long Thread behavior, allowing the agent to recursively fix linting and test failures until the code reaches a deterministic success state.

## 📜 Compliance
All agents and skills must adhere to the formatting standards defined in primitives/patterns/agentic-patterns.md. New capabilities must be registered in registry.json to ensure agent-to-agent discoverability.
