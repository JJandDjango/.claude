---
name: routing
description: Deterministic dispatch rules for orchestrator agent routing
---

# Routing Table

<purpose>
Define the deterministic routing logic for the Orchestrator agent. This routing table maps user input patterns, explicit commands, and complex chains to the appropriate specialist agent, ensuring consistent dispatch behavior across all threads.
</purpose>

<context>
The Orchestrator evaluates incoming requests using a priority-based matching system. This primitive serves as the single source of truth for agent dispatch decisions, preventing ambiguity and ensuring the correct specialist handles each type of work.
</context>

<instructions>
Apply routing rules in the following priority order:

1. **Explicit Command Match**: Check for `@agent` syntax first
2. **Keyword Pattern Match**: Scan user input for known action verbs
3. **Chain Detection**: Identify multi-phase workflows requiring sequential handoffs
4. **Default Fallback**: Route to orchestrator for self-handling when no match is found

Execute the first matching rule and stop evaluation. Do not apply multiple rules to a single request.
</instructions>

<workflow>
## Routing Decision Process

1. Parse user input for explicit `@agent` mentions
2. If found, route directly to specified agent
3. If not found, scan input text for keyword patterns (case-insensitive)
4. Match patterns against routing table below
5. If pattern matches, route to corresponding agent
6. Check if request requires chain execution (multiple phases)
7. If chain detected, initiate first agent in sequence
8. If no matches found, route to orchestrator (self-handle)
</workflow>

<routing>
## Keyword Patterns

| Pattern | Agent | Requires Verification |
|---------|-------|----------------------|
| `implement\|code\|write\|fix\|add\|refactor\|build\|create\|update\|modify\|change` | developer | true |
| `verify\|audit\|review\|validate\|test\|check\|confirm\|inspect` | verifier | false |
| `find\|search\|explore\|understand\|document\|map\|where\|how\|what\|explain\|show\|locate` | doc-explorer | false |
| `plan\|design\|architect\|strategy\|coordinate\|organize` | orchestrator | false |

## Explicit Commands

| Command | Target Agent | Description |
|---------|-------------|-------------|
| `@developer` | developer | Direct dispatch to implementation specialist |
| `@verifier` | verifier | Direct dispatch to validation specialist |
| `@doc-explorer` | doc-explorer | Direct dispatch to research specialist |
| `@orchestrator` | orchestrator | Explicit self-routing |

## Multi-Agent Chains

| Chain Name | Agent Sequence | Trigger Conditions |
|------------|---------------|-------------------|
| `implementation` | doc-explorer → developer → verifier | User requests code changes without existing context |
| `research` | doc-explorer → orchestrator | User asks exploratory questions requiring synthesis |
| `audit` | verifier → developer | Verification fails and fixes are required |

## Default Behavior

- **No Match Found**: Route to orchestrator (self-handle planning and coordination tasks)
- **Ambiguous Match**: Route to orchestrator for clarification
- **Multiple Pattern Matches**: Use first match in priority order (patterns listed above)
</routing>

<constraints>
- Execute only the first matching routing rule
- Do not dispatch to multiple agents simultaneously unless explicitly using a Parallel thread
- Always require verifier handoff after developer implementation (Two-Key rule)
- Do not route verification tasks to developer
- Do not route implementation tasks to doc-explorer
- Do not bypass the routing table with ad-hoc dispatch decisions
</constraints>

<examples>
## Example 1: Keyword Pattern Match
**Input**: "Fix the authentication bug in login.ts"
**Analysis**: Contains "fix" keyword
**Route**: developer
**Verify**: true

## Example 2: Explicit Command
**Input**: "@doc-explorer where is the configuration loader defined?"
**Analysis**: Explicit `@doc-explorer` command
**Route**: doc-explorer
**Verify**: false

## Example 3: Chain Detection
**Input**: "Implement a new caching layer for the API"
**Analysis**: Requires exploration (understand current architecture) + implementation + verification
**Route**: Chain → doc-explorer → developer → verifier
**Verify**: true (final phase)

## Example 4: Default Fallback
**Input**: "What should our testing strategy be for this project?"
**Analysis**: No keyword match, strategic planning question
**Route**: orchestrator (self-handle)
**Verify**: false

## Example 5: Verification Request
**Input**: "Review the recent changes to the payment processor"
**Analysis**: Contains "review" keyword
**Route**: verifier
**Verify**: false (verifier is terminal agent)
</examples>

<output>
## Routing Decision Output Format

When a routing decision is made, the Orchestrator outputs:

```
Route: [agent-name]
Reason: [matching-rule]
Verify: [true|false]
Chain: [chain-name] (if applicable)
```

Example:
```
Route: developer
Reason: Keyword pattern match (implement)
Verify: true
Chain: None
```
</output>

<criteria>
## Routing Decision Checklist

Before finalizing a routing decision, confirm:

- [ ] Input has been evaluated against all explicit commands
- [ ] Keyword patterns have been checked in priority order
- [ ] Chain requirements have been assessed
- [ ] Verification requirement has been determined
- [ ] Selected agent is capable of handling the request
- [ ] Two-Key rule is enforced for implementation work
- [ ] Routing decision is documented in thread context
</criteria>
