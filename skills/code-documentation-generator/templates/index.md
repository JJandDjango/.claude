# Template: Index Document (`INDEX.md`)

> **Version:** 2.0.0  
> **Output:** `generated-documentation/INDEX.md`  
> **Purpose:** Navigation index for all generated documentation, optimized for LLM parsing.

---

## Frontmatter Schema

```yaml
---
type: index
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
root: "{project-root-path}"
total_folders: {count}
total_files: {count}
---
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"index"` |
| `last_generated` | ISO 8601 | Generation timestamp |
| `generator_version` | string | Generator version that created this |
| `root` | string | Project root path |
| `total_folders` | integer | Count of documented folders |
| `total_files` | integer | Count of documented files |

---

## Template

```markdown
---
type: index
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
root: "{project-root-path}"
total_folders: {count}
total_files: {count}
---

# Documentation Index

Generated: {ISO-8601-timestamp}
Generator Version: {version}
Root: {project-root-path}

## Structure  <!-- REQUIRED -->

{project-name}/
  {project-name}.docs.md - {one-line description}
  {project-name}.glossary.md - Domain terminology reference
  src/
    src.docs.md - {one-line description}
    API/
      API.docs.md - {one-line description}
      Controllers/
        Controllers.docs.md - {one-line description}
        AuthController.docs.md
        UserController.docs.md
      Services/
        Services.docs.md - {one-line description}
        AuthClient.docs.md
        UserService.docs.md
  tests/
    tests.docs.md - {one-line description}
    FunctionalTests/
      FunctionalTests.docs.md - {one-line description}

## Quick Reference  <!-- REQUIRED -->

| Path | Purpose | Key Exports |
|------|---------|-------------|
| {project-name}.glossary.md | Domain terminology | - |
| src/ | Application source | - |
| src/API/ | REST API | `Program`, `Startup` |
| src/API/Controllers/ | HTTP endpoints | `AuthController`, `UserController` |
| src/API/Services/ | Business logic | `IAuthClient`, `IUserService` |
| tests/ | Test suites | - |
| tests/FunctionalTests/ | Integration tests | `ApiTestBase` |

## Validation Warnings  <!-- REQUIRED: even if "None" -->

{List any warnings from validation, or "None" if clean}
```

---

## Section Details

### Structure (REQUIRED)

A tree representation of all generated documentation files.

**Format rules:**
- Indent with 2 spaces per level
- Folders end with `/` in the tree but link to `.docs.md`
- Include one-line description after ` - ` for folder docs
- File docs (classes, etc.) listed without description to reduce noise
- Glossary always listed after root doc

**Example:**
```
MyProject/
  MyProject.docs.md - Multi-tenant user management API
  MyProject.glossary.md - Domain terminology reference
  src/
    src.docs.md - Application source code
    API/
      API.docs.md - REST API solution
      Controllers/
        Controllers.docs.md - HTTP endpoint handlers
        UserController.docs.md
        AuthController.docs.md
```

### Quick Reference (REQUIRED)

A table providing fast lookup of key paths and their exports.

**Column definitions:**
- **Path**: Relative path from documentation root
- **Purpose**: Brief description (match folder doc Purpose section)
- **Key Exports**: Primary public types exported (interfaces, main classes)

**Guidelines:**
- Include all folders
- Include glossary
- Skip individual file docs (too granular)
- List 2-4 key exports; use `...` if more exist
- Use `-` for folders with no direct exports

### Validation Warnings (REQUIRED)

Aggregated warnings from all validation checks. This section is always present.

**When warnings exist:**
```markdown
## Validation Warnings

| Type | Location | Issue |
|------|----------|-------|
| Missing Section | src/API/Services/Services.docs.md | Required section "Purpose" not found |
| Broken Link | Controllers.docs.md | Link to ../Services/AuthService.docs.md does not resolve |
| Stale Reference | UserService.docs.md | Class "LegacyUserManager" not found in source |
```

**When no warnings:**
```markdown
## Validation Warnings

None
```

---

## Complete Example

```markdown
---
type: index
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
root: "/"
total_folders: 4
total_files: 3
---

# Documentation Index

Generated: 2024-01-15T10:30:00Z
Generator Version: 2.0.0
Root: /

## Structure

MyProject/
  MyProject.docs.md - Multi-tenant user management API
  MyProject.glossary.md - Domain terminology reference
  src/
    src.docs.md - Application source code
    API/
      API.docs.md - REST API solution
      Controllers/
        Controllers.docs.md - HTTP endpoint handlers
        UserController.docs.md
      Services/
        Services.docs.md - Business logic layer
        UserService.docs.md

## Quick Reference

| Path | Purpose | Key Exports |
|------|---------|-------------|
| MyProject.glossary.md | Domain terminology | - |
| src/API/ | REST API | `Program`, `Startup` |
| src/API/Controllers/ | HTTP endpoints | `UserController` |
| src/API/Services/ | Business logic | `IUserService`, `UserService` |

## Validation Warnings

None
```

---

## Generation Notes

1. **Generated first, updated last**: INDEX.md is created early in the flow with placeholder structure, then updated after validation completes with final warnings
2. **Counts are accurate**: `total_folders` and `total_files` reflect actual generated documentation, not source files
3. **Skipped paths not shown**: Paths outside focus patterns do not appear in Structure

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Validation warning types | `VALIDATION.md` |
| Generation flow | `ORCHESTRATOR.md` |
