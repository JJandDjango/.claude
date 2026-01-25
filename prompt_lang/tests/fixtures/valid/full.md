---
name: full-skill
description: A prompt using all available tags to demonstrate complete structure
model: sonnet
argument-hint: "[arg1] [arg2]"
tools: Bash, Read, Edit
---

# Full Skill

<purpose>
Demonstrate all available XML tags in proper usage.
</purpose>

<variables>
| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | First argument | None |
| `$2` | Second argument | "default" |
</variables>

<context>
This is background information for the agent.
It provides architectural context and relevant details.
The agent should use this information to inform decisions.
</context>

<instructions>
1. LOAD the input file
   ```bash
   cat $1
   ```
2. PARSE the data
3. EXECUTE output to the specified location
</instructions>

<constraints>
- Do not modify the original file
- Do not execute destructive commands
- Do not access files outside the working directory
</constraints>

<examples>
**Input:** User provides a file path
**Output:** Agent reads and processes the file

**Input:** User provides two arguments
**Output:** Agent uses both in processing
</examples>

<output>
- **Status**: [Complete | Failed]
- **Files processed**: [count]
- **Result**: [description]
</output>

<criteria>
- [ ] Input file read successfully
- [ ] Processing completed without errors
- [ ] Output generated in correct format
</criteria>
