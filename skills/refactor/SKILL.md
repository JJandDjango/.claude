---
name: refactor
description: Migrates prompt files to the Prompt Programming Language specification. Validates files using prompt_lang and converts non-compliant markdown to XML tag format.
agent: developer
tools: Bash, Read, Edit
---

# Refactor

<purpose>
Migrate prompt files to comply with the Prompt Programming Language specification. Run validation, identify issues, and convert markdown-headed sections to XML tags.
</purpose>

<variables>
| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | Target file or directory to migrate | Required |
</variables>

<context>
The Prompt Programming Language uses XML tags to distinguish execution from documentation.

**Required tags:** purpose, instructions

**Optional tags:** variables, context, workflow, constraints, examples, output, criteria

**Validation tool location:** prompt_lang package in this repository

**Common migrations (markdown heading to XML tag):**

| Old Format | New Format |
|------------|------------|
| `## Purpose` | purpose tag |
| `## Instructions` | instructions tag |
| `## Variables` | variables tag |
| `## Context` or `## Structure` | context tag |
| `## Workflow` | workflow tag |
| `## Constraints` | constraints tag |
| `## Examples` | examples tag |
| `## Report` or `## Output` | output tag |
| `## Success Criteria` | criteria tag |

**Frontmatter requirements:**
- `name` (required)
- `description` (required)
- `model`, `tools`, `argument-hint`, `agent` (optional)

**Reference:** See prompt_lang/tests/fixtures/valid/ for valid examples.
</context>

<instructions>
1. Run the validator on the target path
   ```bash
   python -m prompt_lang.validate $1
   ```
2. If validation passes, report success and stop
3. If validation fails, read each failing file
4. For each failing file:
   - Add YAML frontmatter if missing (name, description fields)
   - Convert markdown headings to their corresponding XML tags
   - Remove ambiguous/hedging language from instructions (see config for patterns)
   - Ensure no nested tags (all tags must be top-level)
5. Re-run validation to confirm fixes
   ```bash
   python -m prompt_lang.validate $1
   ```
6. Report results
</instructions>

<workflow>
VALIDATE -> if PASS: done -> if FAIL: READ files -> MIGRATE to XML tags -> RE-VALIDATE -> REPORT
</workflow>

<constraints>
- Do not delete content, only restructure it
- Do not modify files that already pass validation
- Do not add tags that have no corresponding content
- Do not nest XML tags inside each other
- Do not use ambiguous language in instructions
</constraints>

<output>
| Field | Value |
|-------|-------|
| **Target** | $1 |
| **Files checked** | [count] |
| **Already compliant** | [count] |
| **Migrated** | [count] |
| **Status** | [PASS / FAIL] |
</output>

<criteria>
- [ ] Validator run on target path
- [ ] All failing files identified
- [ ] Each file migrated to XML tag format
- [ ] Frontmatter present with name and description
- [ ] No ambiguous language in instructions
- [ ] No nested tags
- [ ] Re-validation passes
</criteria>
