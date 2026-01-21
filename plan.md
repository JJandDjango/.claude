# Implementation Plan: Prompt Programming Language

**Spec Version:** 1.0.0  
**Created:** 2025-01-20  
**Updated:** 2025-01-20  
**Status:** Phases 1-5 Complete

---

## Overview

This plan implements the Prompt Programming Language specification (`spec.md`) — a formal syntax for unambiguous prompts using XML tags, YAML frontmatter, and a validation pipeline.

### Goals

1. Build a validation tool (`validate.py`) with structural and semantic checks
2. Create the configuration file (`prompt-lang.config.yaml`)
3. Establish test infrastructure with valid/invalid fixtures
4. Document runtime validation requirements (deferred implementation)

### Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Structural validation | 100% deterministic | **DONE** |
| All test fixtures pass/fail correctly | 100% | **DONE** (67 tests) |
| Clear error messages with line numbers | Yes | **DONE** |
| Config-driven validation rules | Yes | **DONE** |

---

## Implementation Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Foundation | **COMPLETE** |
| Phase 2 | Structural Validation | **COMPLETE** |
| Phase 3 | Semantic Validation | **COMPLETE** |
| Phase 4 | CLI Interface | **COMPLETE** |
| Phase 5 | Integration | **COMPLETE** |
| Phase 6 | Runtime Validation | Deferred |

### Test Results

```
67 passed in 0.79s
├── test_parser.py: 23 tests
├── test_semantic.py: 17 tests
└── test_validate.py: 27 tests
```

### Migration Status (Existing Prompts)

Validation of existing agents and skills shows what needs migration:

| Directory | Files | Status |
|-----------|-------|--------|
| `agents/` | 4 | 0 passed, 4 failed (missing `<purpose>`, `<instructions>`) |
| `skills/` | 37 | 0 passed, 37 failed (various issues) |

**Note:** Migration is out of scope for this implementation plan.

---

## Project Structure (Implemented)

```
E:\.claude\
├── prompt_lang/              # Note: underscore for Python import
│   ├── __init__.py          # Package init with version
│   ├── __main__.py          # Module entry point
│   ├── errors.py            # ValidationError, ValidationResult
│   ├── config.py            # Config loader with dataclasses
│   ├── parser.py            # Structural parser
│   ├── semantic.py          # Semantic validation
│   └── validate.py          # CLI entry point
├── tests/
│   ├── __init__.py
│   ├── test_parser.py       # 23 tests
│   ├── test_semantic.py     # 17 tests
│   ├── test_validate.py     # 27 tests
│   └── fixtures/
│       ├── valid/           # 3 valid prompts
│       └── invalid/         # 8 invalid prompts
├── prompt-lang.config.yaml  # Default configuration
├── requirements.txt         # Python dependencies
└── spec.md                  # Language specification
```

---

## CLI Usage

```bash
# Single file
python -m prompt_lang.validate path/to/skill.md

# Directory (batch)
python -m prompt_lang.validate path/to/skills/

# Custom config
python -m prompt_lang.validate path/to/skill.md --config custom.yaml

# Skip semantic checks
python -m prompt_lang.validate path/to/skill.md --no-semantic

# Verbose output
python -m prompt_lang.validate path/to/skill.md -v
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All files passed |
| 1 | Validation errors found |
| 2 | Configuration error |
| 3 | File not found |

---

## Validation Checks

### Structural (Layer 1) — Deterministic

| Check | Implementation |
|-------|----------------|
| Frontmatter present | Regex for `---` delimiters |
| Frontmatter valid YAML | `pyyaml` parser |
| Required frontmatter fields | `name`, `description` |
| Tag extraction | Regex for `<tag>...</tag>` |
| Required tags | `<purpose>`, `<instructions>` |
| Nesting detection | Stack-based tracking |
| Unclosed tags | Open/close count comparison |
| Mismatched tags | Stack validation |
| Unrecognized tags | Config-driven allowlist |
| Token counting | `tiktoken` with cl100k_base |
| Token limits | Configurable warn/fail thresholds |

### Semantic (Layer 2) — Pattern Matching

| Check | Implementation |
|-------|----------------|
| Ambiguous language | Word-boundary regex matching |
| Scope | Only `<instructions>` tag |
| Patterns | Config-driven list |
| LLM fallback | Placeholder (not implemented) |

---

## Phase 6: Runtime Validation (Deferred)

### Scope

Runtime validation tests actual LLM behavior against prompts.

### Metrics to Implement

| Metric | Description |
|--------|-------------|
| Instruction adherence | Did Claude follow steps in order? |
| Command execution | Were mandatory code blocks executed? |
| Constraint compliance | Did Claude avoid prohibited actions? |
| Output format | Does response match `<output>` template? |

### Implementation Notes

- Requires test harness that executes prompts against Claude
- Needs mock/sandbox environment for command execution
- Results are non-deterministic; statistical validation required
- Consider integration with existing `verifier` agent

---

## Task Checklist

### Phase 1: Foundation
- [x] Create `prompt_lang/` directory structure
- [x] Create `prompt_lang/__init__.py`
- [x] Create `prompt-lang.config.yaml`
- [x] Create `requirements.txt`
- [x] Create `tests/` directory structure
- [x] Create `tests/fixtures/valid/` sample files
- [x] Create `tests/fixtures/invalid/` sample files

### Phase 2: Structural Validation
- [x] Implement `prompt_lang/errors.py`
- [x] Implement `prompt_lang/config.py`
- [x] Implement `prompt_lang/parser.py` — frontmatter extraction
- [x] Implement `prompt_lang/parser.py` — tag extraction
- [x] Implement `prompt_lang/parser.py` — nesting detection
- [x] Implement `prompt_lang/parser.py` — token counting
- [x] Write `tests/test_parser.py`

### Phase 3: Semantic Validation
- [x] Implement `prompt_lang/semantic.py` — pattern matching
- [x] Implement `prompt_lang/semantic.py` — LLM fallback (placeholder)
- [x] Write `tests/test_semantic.py`

### Phase 4: CLI Interface
- [x] Implement `prompt_lang/validate.py` — argument parsing
- [x] Implement `prompt_lang/validate.py` — single file validation
- [x] Implement `prompt_lang/validate.py` — batch validation
- [x] Implement `prompt_lang/validate.py` — output formatting
- [x] Implement `prompt_lang/__main__.py` — module entry point
- [x] Write `tests/test_validate.py`

### Phase 5: Integration
- [x] Run full test suite (67 passed)
- [x] Validate against existing agents (4 failed — need migration)
- [x] Validate against existing skills (37 failed — need migration)
- [x] Update plan.md with implementation status

### Phase 6: Runtime Validation (Deferred)
- [ ] Design test harness architecture
- [ ] Implement instruction adherence checking
- [ ] Implement command execution verification
- [ ] Implement constraint compliance checking
- [ ] Implement output format validation

---

## Next Steps

1. **Migrate existing prompts** — Convert agents and skills to new XML tag format
2. **CI integration** — Add validation to GitHub workflow
3. **Runtime validation** — Implement Phase 6 when needed

---

## Risks & Mitigations

| Risk | Status | Mitigation |
|------|--------|------------|
| Regex edge cases in tag parsing | Mitigated | Comprehensive test fixtures |
| Token counting discrepancy | Mitigated | Using official `tiktoken` library |
| LLM semantic check latency | Mitigated | Pattern-match first, LLM optional |
| Config file not found | Mitigated | Sensible defaults, clear error message |

---

## Notes

- Renamed `prompt-lang/` to `prompt_lang/` for Python import compatibility
- **Migration of existing prompts** is out of scope (to be done separately)
- **Cross-LLM compatibility** is secondary; Claude-first optimization
- **Composability/imports** deferred to future version
