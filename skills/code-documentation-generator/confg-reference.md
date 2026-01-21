# Code Documentation Generator — Configuration Reference

> **Version:** 2.0.0  
> **Role:** Complete reference for `documentation-config.yaml` schema, defaults, and behavior.

## Overview

The configuration file `documentation-config.yaml` controls all aspects of documentation generation. All settings have sensible defaults; a minimal config requires only `project_name`.

---

## Minimal Configuration

```yaml
# documentation-config.yaml (minimal)
project_name: "MyProject"
```

This generates documentation for the entire codebase using all defaults.

---

## Complete Configuration Schema

```yaml
# documentation-config.yaml (complete)

# ============================================================================
# PROJECT METADATA
# ============================================================================

# Generator version - historical record of what created/last updated these docs
# NOTE: This is updated automatically after each generation run.
# The generator always uses its own version, not this value.
generator_version: "2.0.0"

# Project name - used in root document title and glossary filename
project_name: "MyProject"

# Previous generation tracking (auto-updated)
# NOTE: These fields are for audit trails only. The generator does not use
# base_commit programmatically — every run is a full regeneration.
last_generated: null  # ISO 8601 timestamp, e.g., "2024-01-15T10:30:00Z"
base_commit: null     # Commit hash at last generation (audit only)
pr_number: null       # Optional PR reference

# ============================================================================
# PATH FILTERING
# ============================================================================

# Focus patterns - explicitly include these paths
# When specified, acts as an allowlist — only matching paths are documented
# Supports glob patterns
focus:
  - "src/API/Services/**"
  - "src/API/Models/Domain/**"
  - "src/API/Controllers/**"

# Ignore patterns - exclude these from documentation
# Supports glob patterns
ignore:
  - "**/*.generated.cs"
  - "**/*.Designer.cs"
  - "**/Migrations/**"
  - "**/obj/**"
  - "**/bin/**"
  - "**/*.AssemblyInfo.cs"

# ============================================================================
# INTERFACE HANDLING
# ============================================================================

# Interface-implementation auto-detection
# When enabled, automatically discovers classes implementing interfaces
auto_detect_implementations: true  # default: true

# Interface-implementation mappings (optional overrides)
# Default: interfaces documented within implementation files
# Override to create separate docs or custom groupings
interface_mappings:
  # Example: Create separate interface documentation
  # "IAuthClient.cs": "IAuthClient.docs.md"
  # Example: Group multiple implementations
  # "IRepository.cs": "Repositories.docs.md"

# ============================================================================
# DOMAIN KNOWLEDGE
# ============================================================================

# Domain glossary (optional)
# Define project-specific terminology
# Terms are auto-linked in generated documentation
glossary:
  Tenant: "An organization or customer account in the multi-tenant system"
  Claim: "A security assertion about a user's identity or permissions"

# Architectural notes (optional)
# High-level patterns and conventions
# NOTE: Embedded in root document only, not propagated to child docs
architecture:
  - "CQRS pattern used for command/query separation in Services layer"
  - "Repository pattern with Unit of Work for data access"
  - "All services inherit from BaseService for common functionality"

# Team conventions (optional)
# NOTE: Embedded in root document only, not propagated to child docs
conventions:
  - "Controllers handle HTTP concerns only; business logic lives in Services"
  - "DTOs suffixed with 'Dto', domain models have no suffix"
  - "Async methods suffixed with 'Async'"

# ============================================================================
# VALIDATION SETTINGS
# ============================================================================

validation:
  warn_on_missing_sections: true      # default: true
  warn_on_broken_links: true          # default: true
  warn_on_stale_references: true      # default: true
  warn_on_namespace_path_mismatch: false  # default: false
  warn_on_missing_xml_docs: false     # default: false (can be noisy)
  warn_on_undocumented_generics: true # default: true
  warn_on_orphan_extensions: true     # default: true

# ============================================================================
# GLOSSARY LINKING
# ============================================================================

glossary_linking:
  enabled: true           # default: true; set false to disable auto-linking
  link_in_tables: false   # default: false; tables excluded from linking
  max_links_per_doc: null # default: null (no limit); set integer to cap links

# ============================================================================
# SIGNATURE EXTRACTION
# ============================================================================

signature_scope:
  include_internal: false  # default: false; set true for SDK/library projects
  include_protected: true  # default: true; set false to document only public API

# ============================================================================
# PARTIAL CLASS HANDLING
# ============================================================================

partial_class_handling:
  enabled: true                    # default: true; consolidate partial classes
  warn_on_incomplete: true         # default: true; warn if partials outside focus
  show_source_file_column: true    # default: true; show source file in method tables

# ============================================================================
# DEPENDENCY INJECTION (NEW IN v2.0)
# ============================================================================

di_documentation:
  include_lifetimes: true              # default: true; document service lifetimes
  include_registration_summary: true   # default: true; summary table in root doc
  scan_startup_files:                  # files to scan for DI registrations
    - "Program.cs"
    - "Startup.cs"
    - "**/ServiceCollectionExtensions.cs"

# ============================================================================
# TEST DOCUMENTATION (NEW IN v2.0)
# ============================================================================

test_documentation:
  enabled: true                    # default: true; document test projects
  simplified_template: true        # default: true; use test-specific template
  include_test_methods: true       # default: true; list test methods
  include_assertions: false        # default: false; too verbose
```

---

## Pattern Behavior

### Focus as Allowlist

When `focus` patterns are specified, they act as an allowlist — only paths matching focus patterns are documented. Paths not matching any focus pattern are excluded from documentation entirely (except for structural parents).

### Pattern Precedence

1. **Focus wins over ignore**: If a path matches both `focus` and `ignore`, the path is documented (focus takes precedence)
2. **Parent paths are always included**: Parent folders of focused paths are generated for navigation context, even if not explicitly focused
3. **Root document is always generated**: `{project-name}.docs.md` is always created regardless of focus patterns

### Empty or Omitted Focus

If `focus` is empty or omitted entirely, the generator documents everything (implicit `**/*`). This is the default behavior for projects without explicit focus configuration.

### Pattern Examples

```yaml
# Example 1: Focused documentation
focus:
  - "src/API/Services/**"
ignore:
  - "**/*.generated.cs"

# Result:
# - src/API/Services/** is documented (except *.generated.cs)
# - src/ and src/API/ get folder docs (navigation context)
# - src/API/Controllers/ is NOT documented (not in focus)
```

```yaml
# Example 2: Focus wins over ignore
focus:
  - "src/API/Services/**"
ignore:
  - "**/AuthClient.cs"

# Result:
# - src/API/Services/AuthClient.cs IS documented (focus wins)
```

```yaml
# Example 3: No focus specified
focus: []  # or omit entirely

# Result:
# - Everything is documented (implicit **/* allowlist)
```

---

## Defaults Reference

| Setting | Default | Notes |
|---------|---------|-------|
| `generator_version` | (auto-updated) | Written after each run |
| `project_name` | Directory name | Required if not inferrable |
| `last_generated` | `null` | Auto-updated |
| `base_commit` | `null` | Auto-updated |
| `pr_number` | `null` | Optional |
| `focus` | `[]` (document all) | Empty = no filtering |
| `ignore` | `[]` | Common ignores recommended |
| `auto_detect_implementations` | `true` | |
| `interface_mappings` | `{}` | |
| `glossary` | `{}` | |
| `architecture` | `[]` | |
| `conventions` | `[]` | |
| `validation.warn_on_missing_sections` | `true` | |
| `validation.warn_on_broken_links` | `true` | |
| `validation.warn_on_stale_references` | `true` | |
| `validation.warn_on_namespace_path_mismatch` | `false` | |
| `validation.warn_on_missing_xml_docs` | `false` | Can be noisy |
| `validation.warn_on_undocumented_generics` | `true` | |
| `validation.warn_on_orphan_extensions` | `true` | |
| `glossary_linking.enabled` | `true` | |
| `glossary_linking.link_in_tables` | `false` | |
| `glossary_linking.max_links_per_doc` | `null` (no limit) | |
| `signature_scope.include_internal` | `false` | |
| `signature_scope.include_protected` | `true` | |
| `partial_class_handling.enabled` | `true` | |
| `partial_class_handling.warn_on_incomplete` | `true` | |
| `partial_class_handling.show_source_file_column` | `true` | |
| `di_documentation.include_lifetimes` | `true` | |
| `di_documentation.include_registration_summary` | `true` | |
| `test_documentation.enabled` | `true` | |
| `test_documentation.simplified_template` | `true` | |
| `test_documentation.include_test_methods` | `true` | |
| `test_documentation.include_assertions` | `false` | |

---

## Recommended Ignore Patterns

For most C# projects, include these ignores:

```yaml
ignore:
  # Build artifacts
  - "**/obj/**"
  - "**/bin/**"
  
  # Generated code
  - "**/*.generated.cs"
  - "**/*.Designer.cs"
  - "**/*.AssemblyInfo.cs"
  
  # Database migrations (usually auto-generated)
  - "**/Migrations/**"
  
  # IDE files
  - "**/.vs/**"
  - "**/.idea/**"
```

---

## Metadata Fields

All metadata fields are for audit purposes only. The generator writes these values but does not read them to make decisions.

| Field | Purpose | Updated When |
|-------|---------|--------------|
| `generator_version` | Records which version created docs | After each run |
| `last_generated` | Records when docs were generated | After each run |
| `base_commit` | Records source commit at generation | After each run |
| `pr_number` | Records associated PR if provided | When provided |

---

## Configuration Validation

The generator validates configuration on startup:

| Check | Behavior on Failure |
|-------|---------------------|
| Config file missing | Warn, use all defaults, continue |
| Config file unparseable | Warn, use all defaults, continue |
| Unknown keys present | Ignore unknown keys, continue |
| Invalid pattern syntax | Warn, skip invalid pattern, continue |
| Empty `project_name` | Infer from directory name |

Configuration errors never block generation. The generator always produces output.

---

## Environment-Specific Configurations

### Library/SDK Projects

For projects that expose internal APIs:

```yaml
signature_scope:
  include_internal: true   # Document internal members
  include_protected: true
```

### Large Monorepos

For focused documentation in large codebases:

```yaml
focus:
  - "src/CoreModule/**"
  - "src/PublicAPI/**"
  
ignore:
  - "**/Tests/**"
  - "**/Benchmarks/**"
  - "**/Samples/**"
```

### Test-Heavy Projects

For projects where test documentation is valuable:

```yaml
test_documentation:
  enabled: true
  simplified_template: true
  include_test_methods: true
  include_assertions: false  # Keep false; assertions are too verbose
```

### Minimal Documentation

For quick documentation with minimal noise:

```yaml
validation:
  warn_on_missing_sections: false
  warn_on_missing_xml_docs: false
  
glossary_linking:
  enabled: false
  
test_documentation:
  enabled: false
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Orchestration flow | `ORCHESTRATOR.md` |
| Validation rules | `VALIDATION.md` |
| Focus pattern examples | `EXAMPLES/focused-generation.md` |
