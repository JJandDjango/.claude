---
name: code-documentation-generator
description: Generates progressive disclosure documentation for C# codebases optimized for LLM consumption.
multi_instance: false
thread_type: long
tools: [Bash, Read, Write, Glob, Grep]
argument-hint: [config-path] [target-folder] [output-dir]
---

# Purpose

Automate the creation of structured API documentation that mirrors codebase folder structure. Prevents context rot by generating LLM-optimized documentation with progressive disclosure, enabling high-autonomy agents to navigate C# repositories efficiently.

This skill solves the problem of maintaining accurate, navigable documentation for large C# codebases by:
- Generating documentation that mirrors source structure
- Using progressive disclosure (detail increases with depth)
- Extracting public interfaces and signatures for LLM consumption
- Consolidating partial classes and detecting interface implementations
- Validating output without blocking generation

## Variables

- `$1`: Configuration file path (Required; default: `./documentation-config.yaml`)
- `$2`: Target folder path (Optional; default: `.`)
- `$3`: Output directory (Optional; default: `./generated-documentation/`)

## Thread Integration

- **Thread Type**: Long (L) — High autonomy, 50-200+ tool calls, subagent orchestration
- **Exploration (E)**: Use to generate documentation for legacy codebases during RAG sweeps
- **Implementation (I)**: Run after major refactors to update API documentation
- **Refactor (R)**: Regenerate when public interfaces change

### Why Long Thread?

This skill qualifies as a Long Thread because it:
- Spawns subagents for recursive folder processing
- Can involve 50-200+ tool calls for large codebases
- Uses batched processing for context-limited scenarios
- Operates with high autonomy during execution
- Requires minimal human intervention until completion

## Persona

Operate as a **Documentation Architect** with expertise in:
- C# language features and idioms
- API documentation best practices
- LLM consumption patterns
- Progressive disclosure information design

Assume the codebase follows standard .NET conventions unless the configuration specifies otherwise.

## Instructions

1. **Load Configuration**: Read and validate `$1` per [CONFIG-REFERENCE.md](CONFIG-REFERENCE.md)
2. **Discover Files**: Execute `git ls-files` from `$2`, apply focus/ignore patterns
3. **Auto-Detect Interfaces**: If enabled, scan for interface implementations
4. **Generate Root Documentation**: Create `{project}.docs.md` and glossary (if configured)
5. **Process Folders Recursively**: Spawn subagents per [ORCHESTRATOR.md](ORCHESTRATOR.md)
6. **Run Validation**: Execute all checks per [VALIDATION.md](VALIDATION.md)
7. **Finalize INDEX.md**: Aggregate warnings and complete navigation index
8. **Prepare Handoff**: Generate verification payload for `/handoff-to-verifier`

## Constraints

- Do NOT modify source code files — documentation generation is read-only for source
- Do NOT delete existing documentation without explicit `overwrite: true` in config
- Do NOT process files outside the target folder (`$2`) or project root
- Do NOT generate documentation for patterns matching `ignore` configuration
- Do NOT spawn parallel subagents — sequential processing ensures correctness
- Do NOT include private/internal members unless explicitly configured

## Workflow

Reference: See [ORCHESTRATOR.md](ORCHESTRATOR.md) for detailed execution flow.

```
1. PARSE config     → Load $1, validate schema
2. DISCOVER files   → git ls-files, apply focus/ignore
3. DETECT interfaces→ Build implementation mappings
4. GENERATE root    → {project}.docs.md, glossary
5. RECURSE folders  → Spawn subagents per ORCHESTRATOR.md
6. VALIDATE         → Run all checks per VALIDATION.md
7. FINALIZE         → Update INDEX.md with warnings
8. HANDOFF          → Trigger /handoff-to-verifier
```

## Success Criteria

- [ ] Configuration file parsed without errors
- [ ] All focused files discovered via git ls-files
- [ ] INDEX.md generated with complete file tree
- [ ] Root document ({project}.docs.md) generated
- [ ] Glossary generated (if configured)
- [ ] All focused folders processed (recursively)
- [ ] All focused files documented
- [ ] Validation checks executed
- [ ] Warnings aggregated in INDEX.md
- [ ] Handoff report prepared for Verifier

## Report

```markdown
## Generation Report

- **Status**: [Success | Partial | Failed]
- **Config**: $1
- **Target**: $2
- **Output**: $3

### Generation Summary

| Metric | Count |
|--------|-------|
| Folders processed | N |
| Files documented | N |
| Interfaces detected | N |
| Partial classes consolidated | N |

### Validation Summary

| Warning Type | Count |
|--------------|-------|
| missing_section | N |
| broken_link | N |
| stale_reference | N |
| (other) | N |

### Verification Handoff

Prepared for `/handoff-to-verifier` with:
- Output directory existence check
- INDEX.md validation warnings review
- Sample document structure verification
```

## Handoff Schema

For `/handoff-to-verifier` integration, this skill produces:

```yaml
# 1. Thread Metadata
thread_metadata:
  type: "Long"
  skill: "code-documentation-generator"
  phase: "1 of 1"
  confidence: 0.85-0.95  # Based on validation warning count

# 2. Executive Summary
executive_summary:
  mission_status: "[Success | Partial | Failed]"
  big_idea: "Generated LLM-optimized documentation for {project_name} with progressive disclosure structure."

# 3. Technical Changes
changes:
  output_directory: "$3"
  files_generated: [list of .docs.md paths]
  index_path: "$3/INDEX.md"
  warning_count: N
  side_effects: "Read-only operation; no source code modified"

# 4. Verification Requirements
verification:
  primary_tool: "Read"
  mandatory_checks:
    - "Output directory exists and is non-empty"
    - "INDEX.md contains valid navigation tree"
    - "Validation warnings < threshold (default: 10)"
    - "Sample 3 random .docs.md files have required sections"

# 5. Handoff Message
handoff_message: >
  Documentation generated for {project_name}. Check INDEX.md for
  validation warnings. Key areas to verify: root document structure,
  interface implementation mappings, and partial class consolidation.
```

## Verification Commands

Commands for Verifier agent to validate output:

```bash
# 1. Verify output directory exists
ls -la $3

# 2. Check INDEX.md structure
head -100 $3/INDEX.md

# 3. Count validation warnings
grep -c "⚠️" $3/INDEX.md || echo "0"

# 4. Verify root document exists
test -f "$3/{project-name}.docs.md" && echo "PASS" || echo "FAIL"

# 5. Sample file structure check (pick 3 random .docs.md files)
find $3 -name "*.docs.md" | shuf -n 3 | xargs -I {} sh -c 'echo "--- {} ---" && head -30 {}'
```

**Pass Criteria:**
- Output directory contains INDEX.md
- Root document exists
- Validation warning count < 10 (configurable)
- Sample files contain "## Purpose" section

## Module Reference

| Module | Purpose |
|--------|---------|
| [README.md](README.md) | Overview and quick start |
| [ORCHESTRATOR.md](ORCHESTRATOR.md) | Execution flow and subagent coordination |
| [CONFIG-REFERENCE.md](CONFIG-REFERENCE.md) | Configuration schema |
| [VALIDATION.md](VALIDATION.md) | Validation rules and warning types |
| [TEMPLATES/](TEMPLATES/) | Output document templates |
| [RULES/](RULES/) | C# processing and documentation rules |
| [EXAMPLES/](EXAMPLES/) | Worked examples |

### Module Loading by Task

| Task | Load These Modules |
|------|-------------------|
| Understanding the system | `README.md`, `ORCHESTRATOR.md` |
| Configuring generation | `CONFIG-REFERENCE.md` |
| Processing a folder | `TEMPLATES/folder.md`, `TEMPLATES/file.md`, `RULES/*` |
| Understanding validation | `VALIDATION.md` |
| Seeing examples | `EXAMPLES/*` |
