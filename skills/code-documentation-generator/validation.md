# Code Documentation Generator — Validation Reference

> **Version:** 2.0.0  
> **Role:** Defines all validation checks, warning types, and output formats.

## Core Principle

**Generation always completes.** Validation issues produce warnings but never block output. Partial documentation is always better than no documentation.

---

## Generation Resilience

The generator is designed to always produce output, even when encountering issues:

| Scenario | Behavior |
|----------|----------|
| Config file missing or unparseable | Warn, use defaults, continue |
| No git repository found | Warn, use filesystem discovery, continue |
| Zero files match focus patterns | Warn, generate root/index only, continue |
| Parse failures in source files | Warn, document available metadata, continue |
| Broken internal links | Warn in INDEX.md, continue |
| Stale code references | Warn in INDEX.md, continue |
| Large folder exceeds context | Batch processing, note in INDEX.md, continue |
| Glossary config missing | Skip glossary linking, no glossary doc, continue |
| Limited parent context | Infer purpose from contents, note uncertainty, continue |
| Partial class files outside focus | Document available partials, warn about incomplete view |
| Namespace-path mismatch | Document actual namespace, flag divergence, continue |
| Conflicting XML docs in partials | Use first non-empty, warn in INDEX.md, continue |
| Missing XML documentation | Infer from name/signature, optionally warn, continue |
| Unresolvable `<inheritdoc>` | Warn, leave description blank, continue |
| Generic type without constraint docs | Document as-is, optionally warn, continue |

---

## Validation Checks

### 1. Required Sections Check

Verify each document type has its required sections. Conditional sections are only required when their condition applies.

| Document Type | Required Sections | Conditional Sections |
|---------------|-------------------|----------------------|
| **Index** | Structure, Quick Reference, Validation Warnings | — |
| **Root** | Purpose, Architecture Overview, Solution Structure, Contents, Related Documentation | Patterns (if architecture config), Conventions (if conventions config), Dependencies (if external packages), Getting Started (if setup needed), Service Registration (if DI summary enabled) |
| **Glossary** | Terms | — |
| **Folder** | Purpose, Components & Exports, Contents, Related Documentation | Unimplemented Interfaces (if any exist), Dependencies (if has deps), Usage Notes (if non-obvious patterns) |
| **File** | Purpose, Public Signatures, Related Documentation | Source Files (if partial), Interface (if implements), Constructors/Properties/Methods (if they exist), Dependencies (if has deps), Security (if authorization attributes), Generic Parameters (if generic type) |
| **Non-Code** | Purpose, Related Documentation | Key Settings (if config file) |
| **Test** | Purpose, Test Coverage | Test Fixtures (if fixtures exist) |

**Warning format:**
```
WARN: Missing required section "Purpose" in src/API/Services/Services.docs.md
```

**Note:** 
- Optional sections (marked `<!-- OPTIONAL -->` in templates) never trigger warnings
- Conditional sections (marked `<!-- CONDITIONAL -->`) only trigger warnings when their condition is met but the section is missing

---

### 2. Internal Link Validation

Verify all documentation cross-references resolve to existing files.

**What is checked:**
- All markdown links (`[text](path)`) in generated documentation
- Relative paths resolve correctly from source document location
- Target file exists in `generated-documentation/`

**Warning format:**
```
WARN: Broken link in Controllers.docs.md: [AuthService](../Services/AuthService.docs.md) - file does not exist
```

**Not checked:**
- External URLs (http/https links)
- Anchor links within the same document
- Links to source code files (covered by Code Reference Validation)

---

### 3. Code Reference Validation

Verify mentioned files, classes, and methods still exist in codebase.

#### File Path Validation

Check that referenced source files exist:

```
WARN: Stale reference in UserService.docs.md: file "src/API/Helpers/LegacyHelper.cs" not found
```

#### Symbol Validation

Check that referenced symbols exist in source:

```
WARN: Stale reference in UserService.docs.md: class "LegacyUserManager" not found in source
WARN: Stale reference in AuthClient.docs.md: method "ValidateTokenAsync" not found in IAuthClient
```

**What is checked:**
- Class names mentioned in documentation exist in source
- Method names in signature blocks exist in their declared class
- Interface names in `implements` frontmatter exist
- Base class names in `inherits` frontmatter exist

**Note:** Documents referencing stale symbols should be updated. The generator flags these for review but does not auto-correct.

---

### 4. Namespace-Path Validation

When enabled (`warn_on_namespace_path_mismatch: true`), verify that declared namespaces align with folder structure.

**Warning format:**
```
WARN: Namespace mismatch in UserService.cs: declared "MyProject.API.Services" but path suggests "MyProject.src.API.Services"
```

**Behavior:**
- Documents the actual namespace from source (reality)
- Flags divergence for review
- Does not "correct" to match path

**Default:** Disabled (many projects intentionally diverge)

---

### 5. XML Documentation Validation

When enabled (`warn_on_missing_xml_docs: true`), check for missing XML documentation on public members.

**Warning format:**
```
WARN: Missing XML documentation in UserService.cs: method "GetUserAsync" has no <summary>
```

**What is checked:**
- Public classes have `<summary>`
- Public methods have `<summary>`
- Public properties have `<summary>`
- Method parameters have `<param>` tags
- Non-void methods have `<returns>` tags

**Default:** Disabled (can be very noisy on legacy codebases)

---

### 6. Generic Type Validation

When enabled (`warn_on_undocumented_generics: true`), check that generic constraints are documented.

**Warning format:**
```
WARN: Undocumented generic constraint in Repository.cs: type parameter "T" has constraint "IEntity" but no description
```

**Default:** Enabled

---

### 7. Extension Method Validation

When enabled (`warn_on_orphan_extensions: true`), check that extension methods extend documented types.

**Warning format:**
```
WARN: Orphan extension in StringExtensions.cs: extends "System.String" which is not documented in this codebase
```

**Note:** This is informational only. Extensions of external types (like `System.String`) are valid but the warning helps identify when extended types should perhaps be documented.

**Default:** Enabled

---

## Warning Types Reference

Complete registry of warning types that may appear in validation output:

| Type | Source | Description |
|------|--------|-------------|
| `missing_section` | Section Check | Required section not found in document |
| `broken_link` | Link Validation | Internal documentation link doesn't resolve |
| `stale_file_reference` | Code Reference | Referenced source file doesn't exist |
| `stale_symbol_reference` | Code Reference | Referenced class/method doesn't exist |
| `namespace_mismatch` | Namespace Check | Namespace doesn't match folder path |
| `missing_xml_docs` | XML Check | Public member lacks XML documentation |
| `undocumented_generic` | Generic Check | Generic constraint lacks description |
| `orphan_extension` | Extension Check | Extension method extends undocumented type |
| `parse_failure` | Subagent | Could not parse source file |
| `truncated` | Subagent | Large file, only signatures extracted |
| `missing_interface` | Subagent | Interface referenced but not found |
| `batched_processing` | Subagent | Folder processed in batches |
| `limited_context` | Subagent | Purpose inferred without full context |
| `partial_incomplete` | Subagent | Partial class has files outside focus |
| `conflicting_docs` | Subagent | Conflicting XML docs across partials |
| `unresolved_inheritdoc` | Subagent | `<inheritdoc>` chain not resolvable |

---

## Validation Output

### Aggregation in INDEX.md

All validation warnings are aggregated in **INDEX.md only** under the "Validation Warnings" section. Warnings do not appear inline in individual documents.

**Rationale:**
- Keeps generated docs clean
- Provides single location for reviewing issues
- Enables batch review during code review process

### INDEX.md Format

```markdown
## Validation Warnings

| Type | Location | Issue |
|------|----------|-------|
| Missing Section | src/API/Services/Services.docs.md | Required section "Purpose" not found |
| Broken Link | Controllers.docs.md | Link to ../Services/AuthService.docs.md does not resolve |
| Stale Reference | UserService.docs.md | Class "LegacyUserManager" not found in source |
| Parse Failure | src/API/Legacy/OldHelper.cs | Could not parse - syntax error at line 47 |
| Batched Processing | src/API/Services/ | Processed in 4 batches (50 files) |
```

### Clean Validation

When no warnings exist:

```markdown
## Validation Warnings

None
```

---

## Validation Configuration

Control validation behavior in `documentation-config.yaml`:

```yaml
validation:
  # Section completeness
  warn_on_missing_sections: true      # Check required sections exist
  
  # Reference integrity  
  warn_on_broken_links: true          # Check internal links resolve
  warn_on_stale_references: true      # Check code references exist
  
  # Code quality indicators
  warn_on_namespace_path_mismatch: false  # Flag namespace/path divergence
  warn_on_missing_xml_docs: false         # Flag missing XML docs (noisy)
  warn_on_undocumented_generics: true     # Flag undocumented constraints
  warn_on_orphan_extensions: true         # Flag extensions of external types
```

---

## Validation Timing

Validation runs **after** all documentation is generated:

```
1. Generate all documentation
2. Run validation checks
3. Aggregate warnings
4. Update INDEX.md with warnings
5. Report summary
```

This ensures:
- All cross-references can be validated
- Validation never blocks generation
- Complete warning picture in final output

---

## Handling Validation Results

### In Code Review

1. Review `INDEX.md` Validation Warnings section
2. Assess severity of each warning
3. Decide whether to address before merge

### Common Resolutions

| Warning Type | Typical Resolution |
|--------------|-------------------|
| Missing Section | Add section to template or source |
| Broken Link | Fix path or remove stale reference |
| Stale Reference | Update documentation or remove reference |
| Parse Failure | Fix syntax error in source code |
| Missing XML Docs | Add XML documentation to source |
| Namespace Mismatch | Intentional: ignore. Unintentional: fix namespace |

### Suppressing Warnings

To reduce noise, disable specific checks:

```yaml
validation:
  warn_on_missing_xml_docs: false    # Disable if legacy codebase
  warn_on_namespace_path_mismatch: false  # Disable if intentional divergence
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Orchestration flow | `ORCHESTRATOR.md` |
| Configuration options | `CONFIG-REFERENCE.md` |
| Warning types from subagents | `ORCHESTRATOR.md` → Subagent Output Contract |
| Required sections by template | `TEMPLATES/*.md` |
