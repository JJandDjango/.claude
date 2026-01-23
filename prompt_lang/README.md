# prompt_lang

A Prompt Programming Language validator that ensures prompt files conform to an unambiguous, structured specification using XML tags, YAML frontmatter, and semantic checks.

## Features

- **Structural Validation**: Validates YAML frontmatter and XML tag structure
- **Semantic Analysis**: Detects ambiguous/hedging language in instructions
- **Token Counting**: Warns or fails on excessive token counts
- **Configurable Rules**: YAML-based configuration for custom validation
- **CLI Integration**: Structured exit codes for CI/CD pipelines
- **Recursive Scanning**: Validates entire directories of prompt files

## Installation

The module is self-contained Python. Ensure you have Python 3.10+.

Optional dependency for accurate token counting:
```bash
pip install tiktoken
```

## Quick Start

Validate a single file:
```bash
python -m prompt_lang path/to/prompt.md
```

Validate a directory:
```bash
python -m prompt_lang path/to/prompts/
```

## Prompt File Format

Prompt files use a combination of YAML frontmatter and XML tags.

### Minimal Valid Prompt

```markdown
---
name: my-skill
description: Brief description of what this prompt does
---

# My Skill

<purpose>
Clear statement of what this prompt accomplishes.
</purpose>

<instructions>
1. First step
2. Second step
3. Third step
</instructions>
```

### Full Example

```markdown
---
name: full-skill
description: A prompt using all available tags
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
</variables>

<context>
Background information for the agent.
</context>

<instructions>
1. Read the input file
2. Process the data
3. Write the output
</instructions>

<workflow>
START → Read input → Process → Write output → END
</workflow>

<constraints>
- Do not modify the original file
- Do not execute destructive commands
</constraints>

<examples>
**Input:** User provides a file path
**Output:** Agent reads and processes the file
</examples>

<output>
- **Status**: [Complete | Failed]
- **Result**: [description]
</output>

<criteria>
- [ ] Input file read successfully
- [ ] Processing completed without errors
</criteria>
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the prompt |
| `description` | Yes | Brief description of the prompt's purpose |
| `model` | No | Target model (e.g., "sonnet", "opus") |
| `argument-hint` | No | CLI argument format hint |
| `tools` | No | Available tools (comma-separated) |
| `agent` | No | Agent designation |
| `reference` | No | If `true`, skip tag validation |
| `color` | No | UI color hint |

## XML Tags

| Tag | Required | Description |
|-----|----------|-------------|
| `<purpose>` | Yes | Clear statement of what the prompt accomplishes |
| `<instructions>` | Yes | Step-by-step instructions for the agent |
| `<variables>` | No | Variable definitions (typically as a table) |
| `<context>` | No | Background information and architectural context |
| `<workflow>` | No | Process flow diagram or description |
| `<constraints>` | No | Limitations and boundaries |
| `<examples>` | No | Input/output examples |
| `<output>` | No | Expected output format |
| `<criteria>` | No | Success criteria checklist |

## Validation Rules

### Structural Validation

| Rule | Description |
|------|-------------|
| Frontmatter | Must start with `---`, contain valid YAML, end with `---` |
| Required fields | `name` and `description` must be present in frontmatter |
| Required tags | `<purpose>` and `<instructions>` must be present |
| Tag format | XML-style: `<tagname>content</tagname>` |
| No nesting | Tags cannot be nested inside other tags |
| Recognized tags | Only configured tags are allowed |
| Closed tags | All opening tags must have matching closing tags |

### Semantic Validation

Ambiguous language is forbidden in `<instructions>` tags. The following patterns trigger errors:

- "maybe"
- "might"
- "consider"
- "optionally"
- "try to"
- "possibly"
- "it would be good to"
- "you could"
- "perhaps"

### Tag Order Validation

When `enforce_tag_order` is enabled, tags must appear in the order specified by `tag_order`. Only tags present in the document are checked; missing optional tags are skipped.

**Example error:**
```
Line 8: Tag <instructions> is out of order: expected <purpose> at this position
```

### Token Limits

| Threshold | Action |
|-----------|--------|
| 2000 tokens | Warning |
| 4000 tokens | Error (validation fails) |

## CLI Usage

```
usage: prompt_lang.validate [-h] [--config CONFIG] [--no-semantic] [--verbose] path

Validate prompt files against the Prompt Programming Language specification.

positional arguments:
  path                  Path to a prompt file (.md) or directory to validate

options:
  -h, --help            show this help message and exit
  --config, -c CONFIG   Path to config file (default: prompt-lang.config.yaml)
  --no-semantic         Skip semantic validation (ambiguous language detection)
  --verbose, -v         Verbose output (show passing files)
```

### Examples

```bash
# Validate a single file
python -m prompt_lang prompt.md

# Validate with verbose output
python -m prompt_lang prompt.md -v

# Validate a directory
python -m prompt_lang prompts/

# Use custom config
python -m prompt_lang prompt.md --config custom.yaml

# Skip semantic checks
python -m prompt_lang prompt.md --no-semantic
```

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | All files passed validation |
| 1 | VALIDATION_ERROR | Structural or semantic errors found |
| 2 | CONFIG_ERROR | Configuration file problem |
| 3 | FILE_NOT_FOUND | Specified path does not exist |

## Configuration

Create a `prompt-lang.config.yaml` file to customize validation:

```yaml
validation:
  tokens:
    warn_at: 2000
    fail_at: 4000

  semantic_check: true

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

  # Tag order enforcement
  enforce_tag_order: true
  tag_order:
    - purpose
    - variables
    - context
    - instructions
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
      - agent
      - reference
      - color
```

### Tag Order Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enforce_tag_order` | bool | `false` | Enable tag order validation |
| `tag_order` | list | `[]` | Ordered list of tag names defining expected sequence |

When `enforce_tag_order` is `true` and `tag_order` is non-empty, tags must appear in the specified order. Tags not listed in `tag_order` are ignored for ordering purposes.

## Architecture

```
prompt_lang/
├── __init__.py       # Package metadata (version 1.0.0)
├── __main__.py       # CLI entry point
├── config.py         # Configuration management
├── errors.py         # Error and result data classes
├── parser.py         # Structural validation engine
├── semantic.py       # Ambiguous language detection
├── validate.py       # CLI orchestration
└── tests/
    ├── test_parser.py    # Structural validation tests
    ├── test_semantic.py  # Semantic validation tests
    ├── test_validate.py  # CLI integration tests
    └── fixtures/         # Test prompt files
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `validate.py` | CLI entry point, argument parsing, result reporting |
| `parser.py` | YAML frontmatter parsing, XML tag extraction, nesting checks, token counting |
| `semantic.py` | Ambiguous language pattern detection in `<instructions>` |
| `config.py` | Configuration loading from YAML with defaults |
| `errors.py` | `ValidationError` and `ValidationResult` data classes |

## Testing

Run the test suite:

```bash
python -m pytest prompt_lang/tests/
```

Run with coverage:

```bash
python -m pytest prompt_lang/tests/ --cov=prompt_lang
```

## Reference Flag

Set `reference: true` in frontmatter to skip tag validation. This is useful for documentation files that reference the prompt format but aren't actual prompts:

```yaml
---
name: format-reference
description: Documentation about the prompt format
reference: true
---
```

## Version

Current version: **1.0.0**
