# Fix Orchestrator Agent Delegation Loop

## Executive Summary

**Problem**: The Orchestrator agent writes code directly instead of delegating to the Developer agent, wasting tokens since Orchestrator uses a stronger/costlier model.

**Solution**: Update `orchestrator.md` with explicit Task tool delegation instructions, remove Edit tool access, and add clear decision boundaries.

---

## Root Cause Analysis

### Finding 1: `@developer` is Conceptual, Not Executable

The orchestrator.md uses `@developer` notation:
```markdown
**Delegate to specialists** for file modifications:
- `@developer` → code changes (requires verification)
```

However, Claude Code has no built-in understanding that `@developer` means "use the Task tool with subagent_type=developer". This is documentation syntax, not executable syntax.

### Finding 2: No Task Tool Invocation Examples

The orchestrator says "delegate to specialists" but never explains HOW to delegate using the Task tool. There are no concrete examples showing:
- What prompt structure to use
- How to embed agent definitions
- The exact Task tool parameters

### Finding 3: Tool Access Contradiction

Current tools list (line 4):
```yaml
tools: Bash, Read, Edit, Glob, Grep, Task
```

The Orchestrator has `Edit` tool access but is told "never write code directly". This creates a conflict - the model CAN edit files, so it sometimes does despite the instruction.

### Finding 4: Weak Delegation Boundaries

The instruction "Respond directly for questions, explanations, planning, and file reads" is ambiguous. The boundary between "planning" and "implementation" is fuzzy, causing the model to interpret requests as planning and start implementing.

### Finding 5: Missing Decision Tree

No clear flowchart exists for determining when to:
- Respond directly (no delegation)
- Spawn Developer agent
- Spawn Verifier agent
- Spawn Doc-Explorer agent

---

## Solution Design

### Phase 1: Modify `agents/orchestrator.md`

#### 1.1 Remove Edit from Tools List (Line 4)

```yaml
# BEFORE
tools: Bash, Read, Edit, Glob, Grep, Task

# AFTER
tools: Bash, Read, Glob, Grep, Task
```

**Rationale**: If Orchestrator should "never write code directly," it should not have Edit access. This removes temptation and prevents accidental direct implementation.

---

#### 1.2 Add "Delegation Protocol" Section (After Line 31)

Insert new section explaining how `@developer` maps to the Task tool:

```markdown
## Delegation Protocol

The `@agent` notation is shorthand for spawning a subagent via the **Task tool**. To delegate:

1. **Read the agent definition** using the Read tool
2. **Invoke the Task tool** with the agent's full instructions embedded

### Example: Delegate to Developer

When code changes are required, spawn the Developer agent:

**Step 1**: Read the agent definition
> Read file: agents/developer.md

**Step 2**: Use the Task tool with this prompt structure:

---
Adopt the Developer persona from agents/developer.md:

[Paste the full contents of developer.md here]

Your task:
[Describe the specific implementation work]

Context:
- Thread Type: [Base/Chained/Long]
- Modified files will require verification
- Generate a handoff report when complete
---

### Example: Delegate to Verifier

After Developer completes, spawn the Verifier agent:

**Step 1**: Read the agent definition
> Read file: agents/verifier.md

**Step 2**: Use the Task tool:

---
Adopt the Verifier persona from agents/verifier.md:

[Paste the full contents of verifier.md here]

Your task:
Validate the changes described in the handoff report.

Handoff report location: primitives/handoff.md
Verification command: [specific command, e.g., npm test]
---

### Example: Delegate to Doc-Explorer

For research and documentation tasks:

**Step 1**: Read the agent definition
> Read file: agents/doc-explorer.md

**Step 2**: Use the Task tool:

---
Adopt the Doc-Explorer persona from agents/doc-explorer.md:

[Paste the full contents of doc-explorer.md here]

Your task:
[Describe the exploration or documentation task]

Scope: [directories or patterns to explore]
---
```

---

#### 1.3 Add "Decision Tree" Section (Before Workflow)

```markdown
## Decision Tree

Use this flowchart to determine whether to respond directly or delegate:

User Request
    |
    v
Does it require file mutations (create/edit/delete)?
    |
    +-- YES --> Is it code? --> YES --> Delegate to @developer
    |                      --> NO  --> Delegate to @doc-explorer
    |
    +-- NO --> Is it research/exploration of existing code?
                  |
                  +-- YES --> Delegate to @doc-explorer
                  |
                  +-- NO --> Respond directly (planning, questions, explanations)

### Examples of Direct Response (No Delegation)

- "What does this function do?" (explanation)
- "How should we approach this refactor?" (planning)
- "Show me the contents of config.json" (file read, no mutation)
- "What is the project structure?" (exploration via Glob/Grep)

### Examples Requiring Delegation

- "Add a new endpoint to the API" --> @developer
- "Fix the bug in auth.ts" --> @developer
- "Update the README" --> @doc-explorer (or @developer if code-adjacent)
- "Create a new agent definition" --> @developer
```

---

#### 1.4 Strengthen Constraints Section (Lines 34-38)

```markdown
## Constraints

- **CRITICAL: Never use Edit or Write tools** — You do not have these tools. All file modifications must go through `@developer`.
- **Delegation is mandatory for mutations** — If the task requires creating, modifying, or deleting files, you MUST spawn a subagent. No exceptions.
- **Never skip verification** — After `@developer` completes, always spawn `@verifier` unless the user explicitly waives verification.
- **Always load agent definitions** — Before using the Task tool, read the target agent's .md file and include its full contents in the Task prompt.
- **Do not summarize agent definitions** — Include the complete agent definition verbatim; do not paraphrase or abbreviate.
```

---

#### 1.5 Update Workflow Section (Lines 40-48)

```markdown
## Workflow

1. **Init** — Confirm "Operating as **Orchestrator**"
2. **Classify** — Use the Decision Tree to determine:
   - Thread type (Base/Chained/Long)
   - Required specialist (@developer/@verifier/@doc-explorer)
   - Whether to respond directly or delegate
3. **Prepare** — If delegating:
   - Read the target agent's definition file using Read tool
   - Prepare the Task prompt with full agent definition embedded
4. **Delegate** — Use the Task tool with the prepared prompt
5. **Monitor** — Wait for subagent completion
6. **Verify** — If code was changed, spawn `@verifier` using Task tool
7. **Synthesize** — Report final results using the Report template
```

---

### Phase 2: Update `primitives/handoff.md`

Add "Orchestrator Metadata" section at end of file:

```markdown
## 6. Orchestrator Metadata (For Automated Routing)

This section is populated by the Orchestrator to enable automated Verifier spawning:

- **Previous Agent**: [developer | doc-explorer]
- **Verification Required**: [true | false]
- **Verification Command**: [exact command to run]
- **Max Retry Attempts**: [default: 3]
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `agents/orchestrator.md` | Remove Edit tool, add Delegation Protocol, add Decision Tree, strengthen Constraints, update Workflow |
| `primitives/handoff.md` | Add Orchestrator Metadata section |

---

## Verification Plan

1. Start a new Claude Code session
2. Confirm Orchestrator persona is adopted
3. Request a code change: "Add a comment to orchestrator.md"
4. **Expected behavior**:
   - Orchestrator classifies as "file mutation requiring code"
   - Orchestrator reads `agents/developer.md`
   - Orchestrator spawns Developer via Task tool
   - Developer makes the change and generates handoff
   - Orchestrator spawns Verifier via Task tool
   - Verifier validates and issues PASS/FAIL
   - Orchestrator synthesizes final report
5. **Failure indicators**:
   - Orchestrator uses Edit tool directly
   - No Developer task spawned
   - No Verifier task spawned after code change

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Task tool syntax may vary | Test with actual Claude Code; adjust examples |
| Agent definition files are large | Acceptable trade-off; token cost ensures correct delegation |
| Orchestrator may still attempt direct edits | Removing Edit from tools list prevents this |
| Increased orchestrator.md verbosity | Can extract examples to separate file if needed |

---

## Success Criteria

- [ ] Orchestrator no longer has `Edit` in tools list
- [ ] `orchestrator.md` contains explicit Task tool invocation examples
- [ ] Decision Tree clearly defines delegation boundaries
- [ ] Constraints section explicitly prohibits direct file mutations
- [ ] Test: Code change request results in Developer task spawn
- [ ] Test: Developer completion triggers Verifier spawn
