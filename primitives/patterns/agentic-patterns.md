# Agentic Thinking: Core Pillars & Prompt Patterns

## The Core 4 (The Pillars)
1. **Context**: Information the agent has access to (efficiency and persistence).
2. **Prompt**: The fundamental unit of work (tokens in, tokens out).
3. **Tools**: External capabilities (e.g., MCP servers, Slash Commands).
4. **Models**: The underlying reasoning engine (the brain).

---

## Standard Prompt/Skill Sections
These sections define the "Skill" or "Command" architecture in agentic tools like Claude Code.

| Section | Purpose | Location |
| :--- | :--- | :--- |
| **Frontmatter** | Metadata positioned at the top of the prompt, used in skills for progressive disclosure. Begins and ends with three hypens. | Top of file |
| **name** | Name of the skill. Required | Frontmatter |
| **description** | Description of the skill. Required | Frontmatter |
| **model** | Name of the model to use with this skill. Optional | Frontmatter |
| **argument-hint** | Variables passed to this skill (ex: [branch-name] [port-offset]), assigned to positional variables. Optional | Frontmatter |
| **tools** | Tool calls this skill is allowed to make (ex: Bash, Read, Write, Edit, Glob, Grep). Optional | Frontmatter |
| **Purpose** | High-level mission statement; helps the agent decide when to use the skill. | Main Body |
| **Variables** | Dynamic inputs required (paths, branch names, API keys). Variables are positional (ex: $1 is the first variable passed to this skill) | Main Body |
| **Structure** | Relevant files, directories, or architectural context the agent needs to understand before executing. | Main Body |
| **Instructions** | The core logic telling the agent *how* to execute the task. | Main Body |
| **Workflow** | The deterministic, step-by-step sequence to be followed. | Main Body |
| **Report** | The template for summarizing output results to the user. | Main Body |

---

## Advanced Repeatable Patterns
Use these to harden your prompts against hallucinations and errors.

### 1. Constraints (The "Do Not" List)
* **Description**: Explicit boundaries to prevent common failure modes.
* **Example**: "Do not refactor existing code unless it is broken."

### 2. Few-Shot Examples
* **Description**: Demonstrating the desired behavior through input/output pairs.
* **Example**: "Input: 'Fix bug in auth'; Output: [Correct Git Workflow steps]."

### 3. Persona/Context
* **Description**: Establishing the role the agent plays and the assumptions it should make.
* **Example**: "Act as a Senior Security Engineer conducting a white-box audit."

### 4. Success Criteria (Verification)
* **Description**: A checklist for the agent to self-evaluate before concluding.
* **Example**: "Verify that all new exports are documented in README.md."

---
