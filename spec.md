# Prompt Programming Language Specification

**Version:** 1.0.0  
**Status:** Draft  
**Author:** Solo project  
**Created:** 2025-01-20

---

## Executive Summary

A programming language for prompts that provides strict, unambiguous syntax to distinguish execution directives from documentation. Built on Markdown with YAML frontmatter and XML tags, optimized for Claude with cross-LLM compatibility as a secondary goal.

### Problem

Current prompt syntax is ambiguous — Claude interprets execution directives as documentation, causing agents (especially orchestrators) to misinterpret their role and execute tasks directly instead of delegating. Automated prompt generation compounds this by not adhering to consistent standards.

### Solution

A formal language specification with:
- XML tags that semantically distinguish execution from documentation
- Strict validation (structural + semantic) before deployment
- Config-driven rules for flexibility
- Progressive disclosure for token efficiency

### Success Metrics

| Metric | Target | Baseline |
|--------|--------|----------|
| Orchestrator delegation accuracy | 95%+ | ~50% |
| Prompt validation pass rate | 100% | N/A |
| Auto-generated prompt quality | <10% manual correction | ~60-70% |

---

## Table of Contents

1. [Language Specification](#1-language-specification)
2. [Standard Sections](#2-standard-sections)
3. [File Format](#3-file-format)
4. [Validation](#4-validation)
5. [Configuration](#5-configuration)
6. [Dependencies](#6-dependencies)
7. [Testing](#7-testing)
8. [Risks & Mitigations](#8-risks--mitigations)

---

## 1. Language Specification

### 1.1 XML Tags

Nine semantic XML tags define prompt structure:

| Tag | Purpose | Required? |
|-----|---------|-----------|
| `<purpose>` | High-level mission statement | **Yes** |
| `<variables>` | Dynamic inputs (paths, args, keys) | Optional |
| `<context>` | Background, persona, architecture | Optional |
| `<instructions>` | Execution logic — "do this" | **Yes** |
| `<constraints>` | Boundaries, "do not" rules | Optional |
| `<examples>` | Input/output pairs | Optional |
| `<output>` | Report template, response format | Optional |
| `<criteria>` | Success checklist for self-evaluation | Optional |

### 1.2 Core Rules

#### No Nesting

All XML tags are **top-level blocks only**. No nesting allowed.

**Valid:**
```markdown
<context>
Background info here.
</context>

<instructions>
1. Do this
2. Do that
</instructions>
```

**Invalid:**
```markdown
<instructions>
1. Do this
<context>
Nested context  <!-- NOT ALLOWED -->
</context>
2. Do that
</instructions>
```

#### Mandatory Code Execution

Any code block (```) inside `<instructions>` is a **mandatory execution**, not a suggestion. The LLM MUST invoke these commands in the specified order.

```markdown
<instructions>
1. Validate the input
   ```bash
   python scripts/validate.py input.json
   ```
2. If validation passes, deploy
   ```bash
   bash scripts/deploy.sh
   ```
</instructions>
```

#### No Ambiguous Language

The following patterns are **hard failures** inside `<instructions>`:

- "maybe", "might", "consider", "optionally"
- "try to", "possibly", "perhaps"
- "it would be good to", "you could"
- Any hedging language

**Invalid:**
```markdown
<instructions>
1. Maybe run the tests
2. You could deploy if ready
</instructions>
```

**Valid:**
```markdown
<instructions>
1. Run the tests
2. If tests pass, deploy
</instructions>
```

### 1.3 Tag Semantics

| Tag | Semantic Meaning |
|-----|------------------|
| `<purpose>` | "Why this exists" — helps agent decide when to use |
| `<variables>` | "What inputs are needed" — dynamic values |
| `<context>` | "Know this" — reference material, not execution |
| `<instructions>` | "Do this" — mandatory steps |
| `<constraints>` | "Not this" — explicit prohibitions |
| `<examples>` | "Like this" — behavioral guidance |
| `<output>` | "Return this" — expected response structure |
| `<criteria>` | "Check this" — self-evaluation before completing |

---

## 2. Standard Sections

### 2.1 YAML Frontmatter

Located at the top of every file, between `---` delimiters:

| Field | Description | Required? |
|-------|-------------|-----------|
| `name` | Skill identifier (lowercase, hyphens) | **Yes** |
| `description` | What + when to use (max 1024 chars) | **Yes** |
| `model` | Target model (e.g., sonnet, opus, haiku) | Optional |
| `argument-hint` | Positional variables (e.g., `[arg1] [arg2]`) | Optional |
| `tools` | Allowed tool calls (e.g., Bash, Read, Edit) | Optional |

### 2.2 Mapping from agentic-patterns.md

| Old Format | New Format |
|------------|------------|
| `## Purpose` | `<purpose>` |
| `## Variables` | `<variables>` |
| `## Structure` | `<context>` |
| `## Instructions` | `<instructions>` |
| `## Report` | `<output>` |
| Constraints (Advanced) | `<constraints>` |
| Few-Shot Examples (Advanced) | `<examples>` |
| Success Criteria (Advanced) | `<criteria>` |

### 2.3 Canonical Prompt Structure

```markdown
---
name: skill-name
description: What this skill does and when to use it
model: sonnet
argument-hint: [arg1] [arg2]
tools: Bash, Read, Edit
---

# Skill Name

<purpose>
High-level mission statement; helps agent decide when to use this skill.
</purpose>

<variables>
| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | First argument | None |
</variables>

<context>
Background information, persona, architectural context.
Relevant files, directories, or structures.
</context>

<instructions>
1. Step one
2. Step two
   ```bash
   mandatory-command.sh
   ```
3. Step three
</instructions>

<constraints>
- Do not do X
- Never do Y
</constraints>

<examples>
**Input:** User asks for X
**Output:** Agent does Y
</examples>

<output>
- **Status**: [Complete | Failed]
- **Result**: [description]
</output>

<criteria>
- [ ] All steps completed
- [ ] Output matches expected format
- [ ] No constraint violations
</criteria>
```

---

## 3. File Format

| Aspect | Specification |
|--------|---------------|
| Extension | `.md` |
| Encoding | UTF-8 |
| Frontmatter | YAML between `---` delimiters |
| Body | Markdown + XML tags |
| Line endings | LF or CRLF (both accepted) |
| XML tags | Top-level only, no nesting |

---

## 4. Validation

### 4.1 Validation Layers

| Layer | Method | Speed | Deterministic? |
|-------|--------|-------|----------------|
| 1. Structural | Parser (no LLM) | Fast | Yes |
| 2. Semantic | LLM | Slower | No |
| 3. Runtime | LLM behavior test | Slowest | No |

Pipeline is sequential — if any step fails, subsequent steps do not run.

### 4.2 Structural Checks (Layer 1)

| Check | Behavior |
|-------|----------|
| Frontmatter present | Required |
| `name` field | Required |
| `description` field | Required |
| `<purpose>` tag | Required |
| `<instructions>` tag | Required |
| Nesting detected | Hard error |
| Unclosed tag | Hard error |
| Mismatched tag | Hard error |
| Malformed tag | Hard error |
| Unrecognized tag | Hard error |
| Token count > fail threshold | Hard error |
| Token count > warn threshold | Warning |

### 4.3 Semantic Checks (Layer 2)

| Check | Behavior |
|-------|----------|
| Ambiguous language in `<instructions>` | Hard error |

### 4.4 Runtime Checks (Layer 3)

| Metric | Description |
|--------|-------------|
| Instruction adherence | Did Claude follow steps in order? |
| Command execution | Were mandatory commands called? |
| Constraint compliance | Did Claude avoid prohibited actions? |
| Output format | Does response match `<output>` template? |

### 4.5 Validation Script

**Location:** `validate.py` in project root

**CLI Usage:**

```bash
# Single file
python validate.py path/to/skill.md

# Directory (batch)
python validate.py path/to/skills/

# Custom config
python validate.py path/to/skill.md --config custom-config.yaml

# Structural only (skip LLM checks)
python validate.py path/to/skill.md --no-semantic
```

**Output Format:**

```
Validating: skills/orchestrator.md

ERRORS:
  Line 12: Missing required tag <purpose>
  Line 45: Nested tag detected - <context> inside <instructions>
  Line 67: Ambiguous language: "maybe" in <instructions>

WARNINGS:
  Token count: 2,847 (exceeds warn threshold of 2,000)

Result: FAIL (3 errors, 1 warning)
```

**Exit Codes:**
- `0` = Pass
- Non-zero = Fail

---

## 5. Configuration

### 5.1 Config File

**Location:** Project root (may move to `.claude/`)  
**Filename:** `prompt-lang.config.yaml`

```yaml
# prompt-lang.config.yaml

validation:
  tokens:
    warn_at: 2000
    fail_at: 4000

  semantic_check: true  # Set false to skip LLM validation

  required_tags:
    - purpose
    - instructions

  optional_tags:
    - variables
    - context
    - constraints
    - examples
    - output
    - criteria

  ambiguous_patterns:
    - "maybe"
    - "might"
    - "consider"
    - "optionally"
    - "try to"
    - "possibly"
    - "it would be good to"
    - "you could"
    - "perhaps"

  frontmatter:
    required:
      - name
      - description
    optional:
      - model
      - argument-hint
      - tools
```

### 5.2 Custom Tags

Add custom tags via config:

```yaml
validation:
  optional_tags:
    - variables
    - context
    # ... standard tags ...
    - my-custom-tag  # Custom tag
```

Unrecognized tags not in `required_tags` or `optional_tags` cause a **hard error**.

---

## 6. Dependencies

### 6.1 External Dependencies

| Dependency | Purpose | Required? |
|------------|---------|-----------|
| Python 3.12+ | Validation script | Yes |
| Claude API | Semantic + runtime validation | Yes |

### 6.2 Python Libraries

| Library | Purpose |
|---------|---------|
| `pyyaml` | Parse YAML frontmatter |
| `tiktoken` | Token counting |
| `anthropic` | Claude API client |

### 6.3 Constraints

- Claude API must be available (no offline mode for semantic/runtime validation)
- Latest Python version (3.12+)

---

## 7. Testing

### 7.1 Test Strategy

| Layer | Method | Location |
|-------|--------|----------|
| Unit tests | pytest | `tests/` |
| Integration tests | pytest | `tests/` |
| Sample prompts | Valid/invalid fixtures | `tests/fixtures/` |
| Runtime validation | LLM evaluation | Validation pipeline |

### 7.2 Validation Pipeline

```
1. Structural validation (parser, deterministic)
        ↓ pass
2. Semantic validation (LLM - ambiguous language)
        ↓ pass
3. Runtime validation (LLM - behavior testing)
```

If any step fails, subsequent steps do not run.

### 7.3 Test Artifacts

- **Test suite:** pytest
- **Test cases:** `tests/`
- **Fixtures:** `tests/fixtures/` (valid and invalid sample prompts)

---

## 8. Risks & Mitigations

### 8.1 Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Claude misinterprets prompts despite strict syntax | Medium | High | Testing, iteration, clearer semantics |
| LLM ambiguity detection inconsistent | Medium | Medium | Pattern matching fallback |
| Token counting varies | Low | Low | Use `tiktoken` |
| Spec too rigid | Medium | Medium | Custom tags via config |
| Adoption friction | Low | Low | Docs, migration guide |
| Unrecognized XML tags | Medium | High | Hard error on undefined tags |
| Malformed XML | Medium | High | Regex/parser validation |

### 8.2 Assumptions

- XML tags sufficient for execution vs documentation distinction
- Ambiguous language patterns are comprehensive
- 2000/4000 token thresholds appropriate

### 8.3 Out of Scope

- GUI/visual editor
- Runtime execution engine (LLM is the engine)
- Version control integration (use GitHub)
- Prompt marketplace (use GitHub)
- Orchestrator delegation problem (separate PR)
- Cross-LLM compatibility (secondary, future)
- Composability/imports (secondary, future)

---

## Appendix A: Valid Prompt Example

```markdown
---
name: deploy-service
description: Deploys a service to production after validation. Use when deploying new releases.
tools: Bash, Read
---

# Deploy Service

<purpose>
Automate production deployment with pre-flight validation checks.
</purpose>

<variables>
| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | Service name | Required |
| `$2` | Environment | production |
</variables>

<context>
This skill is used in CI/CD pipelines. It assumes the service has already been built and tested.
</context>

<instructions>
1. Validate the service exists
   ```bash
   python scripts/check_service.py $1
   ```
2. Run pre-flight checks
   ```bash
   python scripts/preflight.py $1 $2
   ```
3. Deploy to environment
   ```bash
   bash scripts/deploy.sh $1 $2
   ```
4. Verify deployment health
   ```bash
   python scripts/healthcheck.py $1 $2
   ```
</instructions>

<constraints>
- Do not deploy without passing pre-flight checks
- Do not skip health check verification
- Do not modify deployment scripts during execution
</constraints>

<output>
- **Service**: $1
- **Environment**: $2
- **Status**: [Deployed | Failed]
- **Health**: [Healthy | Unhealthy]
</output>

<criteria>
- [ ] Service validated
- [ ] Pre-flight passed
- [ ] Deployment completed
- [ ] Health check passed
</criteria>
```

---

## Appendix B: Invalid Prompt Examples

### B.1 Missing Required Tag

```markdown
---
name: example
description: Example skill
---

# Example

<instructions>
1. Do something
</instructions>
```

**Error:** Missing required tag `<purpose>`

### B.2 Nested Tags

```markdown
---
name: example
description: Example skill
---

# Example

<purpose>
Do a thing.
</purpose>

<instructions>
1. Start
<context>
Some nested info
</context>
2. End
</instructions>
```

**Error:** Line 14: Nested tag detected - `<context>` inside `<instructions>`

### B.3 Ambiguous Language

```markdown
---
name: example
description: Example skill
---

# Example

<purpose>
Do a thing.
</purpose>

<instructions>
1. Maybe run the tests
2. You could deploy if it looks good
3. Consider checking the logs
</instructions>
```

**Errors:**
- Line 14: Ambiguous language: "maybe"
- Line 15: Ambiguous language: "you could"
- Line 16: Ambiguous language: "consider"

---

## Appendix C: Determinism Philosophy

| Aspect | Approach |
|--------|----------|
| LLM reasoning/interpretation | Non-deterministic (inherent to LLMs) |
| Command execution | **Deterministic** — code blocks MUST be called |
| Sequence ordering | **Deterministic** — steps execute in order |
| Tool/script invocation | **Deterministic** — explicit calls are mandatory |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-20 | Initial specification |
