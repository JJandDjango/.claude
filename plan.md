# Product Specification Interview: Prompt Programming Language

**Session ID:** spec-2025-01-20-prompt-lang  
**Project:** Prompt Programming Language  
**Type:** NEW  
**Complexity:** COMPLEX  
**Format:** MARKDOWN  
**Status:** IN PROGRESS — Section 2

---

## Section 1: Problem Space ✅

### Problem Statement
Current prompt syntax is ambiguous — Claude interprets execution directives as documentation, causing agents (especially orchestrators) to misinterpret their role and execute tasks directly instead of delegating. Automated prompt generation compounds this by not adhering to consistent standards.

### Who's Affected
- Primary: You (prompt author) and automated systems generating prompts
- Downstream: Agent behavior and system reliability

### Cost of Not Solving
- Agents behave incorrectly (primary concern)
- Inconsistent outputs across the system
- Significant debugging/rewriting time

### Previous Attempts
- Manual patterns (`agentic-patterns.md`)
- Orchestrator/developer/verifier agent structure
- **Why they failed:** Syntax lacks enforcement mechanism; no distinction between "execution syntax" and "documentation syntax"

### Success Metrics
| Metric | Target | Current Baseline |
|--------|--------|------------------|
| Orchestrator delegation accuracy | 95%+ | ~50% |
| Prompt validation pass rate | 100% | N/A (no validation) |
| Auto-generated prompt quality | <10% manual correction | ~60-70% need fixes |

---

## Section 2: Users & Context ✅

### Primary Users
| User | Role | Technical Level |
|------|------|-----------------|
| You (Prompt Author) | Designs and writes all prompt definitions | Expert |
| Claude/LLMs (Interpreter) | Executes prompts; must parse syntax unambiguously | N/A |
| Automated Systems | Generates prompts programmatically | Deterministic |

### Current Workflow
1. Interview/create prompt
2. Validate format (LLM-based, inconsistent)
3. Execute prompt via LLM
4. Manual validation of results

### Desired Workflow
1. Create prompt using strict syntax
2. Deterministic "build" validation (catches ambiguity)
3. Execute with unambiguous interpretation
4. Automated result validation

### When Used
Every non-conversational prompt — agents, skills, workflows, automated tasks

### Key Friction Points
- **Primary:** No enforced syntax → inconsistent results
- **Secondary:**
  - Verbose boilerplate
  - Inconsistent section ordering
  - Unclear required vs optional sections
  - Difficult to compose/reuse prompt fragments

---

## Section 3: Stakeholders & Decisions ✅

**Skipped** — Solo project. You are the sole owner, decision-maker, and primary user. Project will be hosted on GitHub for potential community refinement over time.

---

## Section 4: Scope & Prioritization ✅

### Syntax Decision
Use Anthropic's recommended XML tags as the foundation:

| Tag | Purpose | Semantic Meaning |
|-----|---------|------------------|
| `<instructions>` | Execution directives | "Do this" — steps Claude MUST follow |
| `<context>` | Background/documentation | "Know this" — reference material |
| `<examples>` | Input/output pairs | "Like this" — behavioral guidance |
| `<constraints>` | Boundaries | "Not this" — explicit prohibitions |
| `<output>` | Response format | "Return this" — expected structure |

Custom tags can be defined later as needed.

### Must-Have Features (MVP)

| # | Feature | Acceptance Criteria |
|---|---------|---------------------|
| 1 | Language specification | Formal syntax doc defining all tags, their semantics, and nesting rules |
| 2 | Standard sections | Required/optional sections defined (Frontmatter, Purpose, Variables, Instructions, Workflow, Report per `agentic-patterns.md`) |
| 3 | Validation/build step | Tool that checks prompts for ambiguity before deployment; returns pass/fail + errors |
| 4 | File format | `.md` files with YAML frontmatter + markdown + XML tags |
| 5 | Claude-first optimization | Syntax leverages Claude's XML training; follows Anthropic best practices |
| 6 | Cross-LLM compatibility | Prompts work with other LLMs (may require adapter or degraded experience) |
| 7 | Automated generation support | Rules strict enough that LLM-generated prompts pass validation |
| 8 | Composability | Import/reference other prompt fragments; modular design |

### Out of Scope
- GUI/visual editor (already exist)
- Runtime execution engine (LLM interpretation is the engine)
- Version control integration (use GitHub)
- Prompt marketplace/sharing platform (use GitHub)

### Non-Goals
- Replace natural language entirely (still markdown-based)
- Guarantee deterministic LLM reasoning (impossible)
- Support non-text modalities (images, audio)
- Backward compatibility with arbitrary existing prompts

### Determinism Philosophy
| Aspect | Approach |
|--------|----------|
| LLM reasoning/interpretation | Non-deterministic (inherent to LLMs) |
| Command execution | **Deterministic** — code blocks in `<instructions>` MUST be called |
| Sequence ordering | **Deterministic** — steps execute in specified order |
| Tool/script invocation | **Deterministic** — explicit calls are mandatory, not suggestions |

**Rule:** Any code block (``` ```) inside `<instructions>` is a mandatory execution, not a suggestion.

### Priority Tiers

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **Core** | 1. Language specification | Foundation — everything depends on this |
| **Core** | 2. Standard sections | Structure — defines what goes where |
| **Core** | 3. Validation/build step | Enforcement — catches ambiguity |
| **Core** | 4. File format | Implementation — how it's stored |
| Secondary | 5. Claude-first optimization | Implicit in design decisions |
| Secondary | 6. Cross-LLM compatibility | Can be layered on later |
| Secondary | 7. Automated generation support | Follows from strict spec |
| Secondary | 8. Composability | Enhancement, not foundation |

### Dependency Chain

```
1. Language Spec
       ↓
2. Standard Sections (uses spec)
       ↓
4. File Format (implements spec + sections)
       ↓
3. Validation (enforces all of the above)
```

---

## Section 5: Technical Context ✅

### Tech Stack
| Component | Technology |
|-----------|------------|
| File format | Markdown (`.md`) |
| Metadata | YAML frontmatter |
| Semantic markup | XML tags |
| Storage | Filesystem / GitHub |
| Validation tool | Bash + LLM (Claude validates prompts) |

### Integrations
- **Claude Code** (primary runtime)
- **Existing `agentic-patterns.md` structure** (foundation)
- **GitHub** for storage/versioning
- **GitHub CI/CD** (nice to have — automated validation)

### Constraints
- **Budget-conscious:** Minimize token usage
- **Progressive disclosure:** Load details only when needed
- **Concise prompts preferred**

### Not a Concern (for now)
- Performance optimization
- Security/compliance

---

## Section 6: Functional Requirements ✅

### XML Tags (Final)

| Tag | Purpose | Required? |
|-----|---------|-----------|
| `<purpose>` | Mission statement | Yes |
| `<variables>` | Dynamic inputs | Optional |
| `<context>` | Background, persona, structure | Optional |
| `<instructions>` | Execution logic | Yes |
| `<workflow>` | Step-by-step sequence | Optional |
| `<constraints>` | Boundaries, "do not" | Optional |
| `<examples>` | Input/output pairs | Optional |
| `<output>` | Report template | Optional |
| `<criteria>` | Success checklist | Optional |

**Rules:**
- No nesting allowed — all tags are top-level only
- Code blocks inside `<instructions>` are mandatory executions
- Ambiguous language inside `<instructions>` is a hard fail

### Feature 1: Language Specification

**Acceptance Criteria:**
- [ ] Every valid tag documented with purpose and usage
- [ ] No nesting rule is explicit — all tags top-level only
- [ ] Required vs optional clearly marked
- [ ] At least 3 complete examples of valid prompts
- [ ] At least 3 examples of invalid prompts with explanations

### Feature 2: Standard Sections

**Acceptance Criteria:**
- [ ] All 9 XML tags documented with purpose and usage
- [ ] Required tags identified: `<purpose>`, `<instructions>`
- [ ] Optional tags: `<variables>`, `<context>`, `<workflow>`, `<constraints>`, `<examples>`, `<output>`, `<criteria>`
- [ ] YAML frontmatter fields documented (name, description required; model, argument-hint, tools optional)
- [ ] Canonical structure template provided
- [ ] Mapping from old `agentic-patterns.md` to new format documented

### Feature 3: Validation/Build Step

**Acceptance Criteria:**
- [ ] Validates frontmatter structure (required fields: name, description)
- [ ] Validates required tags present (`<purpose>`, `<instructions>`)
- [ ] Detects nesting violations
- [ ] Detects unclosed/mismatched tags
- [ ] Detects unrecognized tag names
- [ ] Detects ambiguous language (hard fail)
- [ ] Returns clear error messages with line numbers
- [ ] Exit code 0 for pass, non-zero for fail
- [ ] Can validate single file or directory (batch)

**Ambiguous Language Patterns (hard fail):**
- "Maybe", "might", "consider", "optionally", "try to", "possibly"
- "It would be good to", "you could", "perhaps"
- Any hedging language inside `<instructions>`

### Feature 4: File Format

**Specification:**
| Aspect | Definition |
|--------|------------|
| Extension | `.md` |
| Encoding | UTF-8 |
| Frontmatter | YAML between `---` delimiters |
| Body | Markdown + XML tags |
| Line endings | LF or CRLF — both accepted |

**Acceptance Criteria:**
- [ ] File extension is `.md`
- [ ] UTF-8 encoding
- [ ] YAML frontmatter at top (between `---`)
- [ ] XML tags are top-level, not nested
- [ ] Standard markdown formatting supported within tags
- [ ] Code blocks supported within `<instructions>`

### Canonical Prompt Structure

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

<workflow>
START → Validate input → Process → Output → END
</workflow>

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

## Section 7: Non-Functional Requirements ✅

### Token Limits
- Configurable per project
- Default: warn at 2000 tokens, fail at 4000 tokens per file
- Over-limit files should be split for progressive disclosure

### Validation Layers

| Layer | Method | Speed | Deterministic? |
|-------|--------|-------|----------------|
| 1. Structural | Parser (no LLM) | Fast | Yes |
| 2. Semantic | LLM | Slower | No |

**Layer 1 (Structural):**
- Frontmatter present and valid
- Required tags present
- No nesting violations
- Tags closed properly
- Recognized tag names only
- Token count within limits

**Layer 2 (Semantic):**
- Ambiguous language detection
- Can be disabled via config

### Configuration File

Location: Project root (may move to `.claude/`)

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
    - workflow
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

### Quality Attributes

| Category | Requirement |
|----------|-------------|
| Reliability | Structural validation deterministic |
| Usability | Clear error messages with line numbers |
| Maintainability | Config-driven, rules externalized |
| Extensibility | Custom tags possible via config (future) |

---

## Section 8: Data Specifications ✅

**Skipped** — Purely file-based, no persistent data storage required.

---

## Section 9: API & Contract Specifications ✅

### Validation Script Contract

**Location:** Python script within the project

**Input:**
- File path(s) to validate
- Config file path (optional, defaults to `prompt-lang.config.yaml`)

**Output:**
- Pass/fail status
- List of errors/warnings with line numbers
- Exit code (0 = pass, non-zero = fail)

**CLI Usage:**

```bash
# Single file
python validate.py path/to/skill.md

# Directory (batch)
python validate.py path/to/skills/

# Custom config
python validate.py path/to/skill.md --config custom-config.yaml

# Structural only (skip LLM semantic check)
python validate.py path/to/skill.md --no-semantic
```

**Example Output:**

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

---

## Section 10: Dependencies & Constraints ✅

### External Dependencies

| Dependency | Purpose | Required? |
|------------|---------|-----------|
| Python 3.12+ | Validation script | Yes |
| Claude API | Semantic validation | Yes |

### Python Libraries

| Library | Purpose |
|---------|---------|
| `pyyaml` | Parse YAML frontmatter |
| `tiktoken` | Token counting |
| `anthropic` | Claude API client |

### Constraints

- Claude API must be available (no offline mode for semantic validation)
- Latest Python version (3.12+)

---

## Section 11: Risks & Mitigations ✅

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Claude misinterprets prompts despite strict syntax | Medium | High | Testing, iteration, clearer semantics |
| LLM ambiguity detection inconsistent | Medium | Medium | Pattern matching fallback |
| Token counting varies | Low | Low | Use `tiktoken` |
| Spec too rigid | Medium | Medium | Custom tags via config |
| Adoption friction | Low | Low | Docs, migration guide |
| Unrecognized XML tags | Medium | High | Hard error on undefined tags |
| Malformed XML | Medium | High | Regex/parser validation |

### XML Validation Rules

| Check | Behavior |
|-------|----------|
| Unrecognized tag (not in required, optional, or custom) | Hard error |
| Unclosed tag (e.g., `<instructions>` without `</instructions>`) | Hard error |
| Mismatched tag (e.g., `<instructions>...</purpose>`) | Hard error |
| Malformed tag (e.g., `<instructions` missing `>`) | Hard error |

### Assumptions

- XML tags sufficient for execution vs documentation distinction
- Ambiguous language patterns are comprehensive
- 2000/4000 token thresholds appropriate

### Out of Scope

- Orchestrator delegation problem (separate PR)

---

## Section 12: Validation & Testing ✅

### Testing Strategy

| Layer | Method | Location |
|-------|--------|----------|
| Unit tests | pytest | `tests/` |
| Integration tests | pytest | `tests/` |
| Sample prompts | Valid/invalid fixtures | `tests/fixtures/` |
| Runtime validation | LLM evaluation | Part of validation pipeline |

### Validation Pipeline (Sequential)

```
1. Structural validation (parser, deterministic)
        ↓ pass
2. Semantic validation (LLM - ambiguous language)
        ↓ pass
3. Runtime validation (LLM - behavior testing)
```

If any step fails, subsequent steps do not run.

### Runtime Validation Metrics

| Metric | Description |
|--------|-------------|
| Instruction adherence | Did Claude follow steps in order? |
| Command execution | Were mandatory commands called? |
| Constraint compliance | Did Claude avoid prohibited actions? |
| Output format | Does response match `<output>` template? |

### Test Artifacts

- **Test suite:** pytest
- **Test cases:** Separate from spec (`tests/`)
- **Fixtures:** Valid/invalid sample prompts (`tests/fixtures/`)

---

## Sections Remaining

- [x] Section 3: Stakeholders & Decisions (skipped — solo)
- [x] Section 4: Scope & Prioritization
- [x] Section 5: Technical Context
- [x] Section 6: Functional Requirements
- [x] Section 7: Non-Functional Requirements
- [x] Section 8: Data Specifications (skipped — file-based only)
- [x] Section 9: API & Contract Specifications
- [x] Section 10: Dependencies & Constraints
- [x] Section 11: Risks & Mitigations
- [x] Section 12: Validation & Testing
- [x] Gate Validation
- [x] Final Specification Output
