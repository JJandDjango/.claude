---
name: agentic-patterns
description: Reference documentation for core agentic thinking pillars, standard prompt sections, and advanced repeatable patterns.
reference: true
---

# Agentic Thinking: Core Pillars & Prompt Patterns

<purpose>
Define the foundational concepts and standard patterns for building effective agentic prompts and skills.
</purpose>

<context>
## The Core 4 (The Pillars)

1. **Context**: Information the agent has access to (efficiency and persistence)
2. **Prompt**: The fundamental unit of work (tokens in, tokens out)
3. **Tools**: External capabilities (e.g., MCP servers, Slash Commands)
4. **Models**: The underlying reasoning engine (the brain)
</context>

<variables>
## Standard Prompt/Skill Sections

| Section | Purpose | Location |
|---------|---------|----------|
| **Frontmatter** | Metadata for progressive disclosure | Top of file |
| **name** | Skill identifier (required) | Frontmatter |
| **description** | Skill description (required) | Frontmatter |
| **model** | Target model (optional) | Frontmatter |
| **argument-hint** | Positional variables (optional) | Frontmatter |
| **tools** | Allowed tool calls (optional) | Frontmatter |
| **agent** | Executing agent (optional) | Frontmatter |
| **reference** | Skip validation flag (optional) | Frontmatter |
</variables>

<examples>
## XML Tag Mapping

| Tag | Purpose | Required |
|-----|---------|----------|
| `purpose` | High-level mission statement | Yes |
| `instructions` | Core execution logic | Yes |
| `variables` | Dynamic inputs | No |
| `context` | Background/architectural info | No |
| `workflow` | Step-by-step sequence | No |
| `constraints` | Boundaries and prohibitions | No |
| `examples` | Input/output pairs | No |
| `output` | Response template | No |
| `criteria` | Success checklist | No |

## Advanced Repeatable Patterns

### 1. Constraints (The "Do Not" List)
Explicit boundaries to prevent common failure modes.
- Example: "Do not refactor existing code unless it is broken."

### 2. Few-Shot Examples
Demonstrating desired behavior through input/output pairs.
- Example: "Input: 'Fix bug in auth'; Output: [Correct Git Workflow steps]."

### 3. Persona/Context
Establishing the role and assumptions.
- Example: "Act as a Senior Security Engineer conducting a white-box audit."

### 4. Success Criteria (Verification)
Checklist for agent self-evaluation before concluding.
- Example: "Verify that all new exports are documented in README.md."
</examples>
