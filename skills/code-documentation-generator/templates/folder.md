# Template: Folder Document (`{foldername}.docs.md`)

> **Version:** 2.0.0  
> **Output:** `generated-documentation/{path}/{foldername}.docs.md`  
> **Purpose:** Document a folder's purpose, contents, and exports.

---

## Frontmatter Schema

```yaml
---
title: "{foldername}"
path: "{relative-path-from-root}"
type: folder
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
namespace: "{C#-namespace-if-applicable}"
navigation_parent: true | false  # true if this is a structural parent only
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Folder name |
| `path` | string | Yes | Relative path from project root |
| `type` | string | Yes | Always `"folder"` |
| `last_generated` | ISO 8601 | Yes | Generation timestamp |
| `generator_version` | string | Yes | Generator version |
| `base_commit` | string | Yes | Source commit hash |
| `parent` | string | Yes | Path to parent folder's doc |
| `namespace` | string | No | Primary C# namespace for this folder |
| `navigation_parent` | boolean | No | `true` if folder is outside focus but has focused children |

---

## Template

```markdown
---
title: "{foldername}"
path: "{relative-path-from-root}"
type: folder
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
namespace: "{C#-namespace-if-applicable}"
---

# {foldername}

## Purpose  <!-- REQUIRED -->

{What this folder contains and why it exists}

## Components & Exports  <!-- REQUIRED -->

| Component | Type | Exported | Description |
|-----------|------|----------|-------------|
| `{ClassName}` | class | yes | {brief description} |
| `{IInterfaceName}` | interface | yes | {brief description} |
| `{InternalHelper}` | class | no | {brief description} |

## Unimplemented Interfaces  <!-- CONDITIONAL: only if unimplemented interfaces exist in folder -->

The following interfaces in this folder have no implementations found in the documented codebase:

| Interface | File | Notes |
|-----------|------|-------|
| `IExternalService` | `IExternalService.cs` | May be implemented by external package |

### IExternalService

```csharp
public interface IExternalService
{
    Task<Result> ProcessAsync(Request request);
}
```

{Contract description if determinable}

## Contents  <!-- REQUIRED -->

### Folders

| Folder | Purpose |
|--------|---------|
| `{subfolder}/` | {description} |

### Files

| File | Key Types |
|------|-----------|
| `{filename}.cs` | `{ClassName}`, `{InterfaceName}` |

## Dependencies  <!-- OPTIONAL: only if folder has dependencies -->

### Internal

| Dependency | Path | Purpose |
|------------|------|---------|
| `{Namespace.ClassName}` | `../Services/` | {why needed} |

### External

| Package | Purpose |
|---------|---------|
| `{PackageName}` | {why needed} |

## Usage Notes  <!-- OPTIONAL: only if non-obvious usage patterns exist -->

{How code in this folder is typically used}

## Related Documentation  <!-- REQUIRED -->

- [Parent: {parent}]({parent-path})
- [Child: {child}]({child-path})
```

---

## Section Details

### Purpose (REQUIRED)

Describe what this folder contains and why it exists as a distinct unit.

**Good example:**
> Business logic services implementing core domain operations. All services in this folder follow the IService pattern and are registered as scoped dependencies.

**Bad example:**
> Contains service files.

### Components & Exports (REQUIRED)

Table of all public types defined in this folder.

| Column | Description |
|--------|-------------|
| Component | Type name (use backticks) |
| Type | `class`, `interface`, `struct`, `enum`, `record`, `delegate` |
| Exported | `yes` if public, `no` if internal |
| Description | One-line description of purpose |

**Ordering:**
1. Interfaces first
2. Classes implementing interfaces
3. Other public classes
4. Internal types (if `include_internal: true`)

### Unimplemented Interfaces (CONDITIONAL)

Include only when interfaces exist in the folder with no implementations found.

**When to include:**
- Interface defined in folder
- No class in documented codebase implements it
- Implementation may be external or not yet written

**Format:**
- Summary table listing all unimplemented interfaces
- Individual sections with full interface signatures
- Notes about likely implementation location

### Contents (REQUIRED)

#### Folders Subsection

List immediate child folders with brief purpose.

| Column | Description |
|--------|-------------|
| Folder | Folder name with trailing `/` |
| Purpose | One-line description |

#### Files Subsection

List files in this folder with their key types.

| Column | Description |
|--------|-------------|
| File | Filename |
| Key Types | Primary public types defined (2-3 max) |

### Dependencies (OPTIONAL)

Include if types in this folder depend on types from other folders or external packages.

**Internal:** Dependencies on other parts of this codebase
**External:** NuGet package dependencies specific to this folder

### Usage Notes (OPTIONAL)

Include if there are non-obvious patterns for using code in this folder.

**Examples:**
- Required initialization order
- Common usage patterns
- Integration points

### Related Documentation (REQUIRED)

Links to:
- Parent folder documentation
- Child folder documentation
- Related folders (e.g., corresponding test folder)

---

## Navigation Parent Variant

When a folder is outside focus patterns but contains focused children, generate a minimal navigation document:

```markdown
---
title: "Services"
path: "src/API/Services/"
type: folder
navigation_parent: true
---

# Services

## Purpose

Business logic layer. Only `Auth/` is within documentation focus.

## Components & Exports

| Component | Type | Status | Description |
|-----------|------|--------|-------------|
| `Auth/` | folder | ✅ Documented | Authentication services |
| `Users/` | folder | ⏭️ Skipped | Outside focus patterns |

## Contents

### Folders

| Folder | Status | Notes |
|--------|--------|-------|
| `Auth/` | ✅ Documented | Authentication and authorization services |
| `Users/` | ⏭️ Skipped | Outside focus patterns |

## Related Documentation

- [Parent: API](../API.docs.md)
- [Child: Auth](./Auth/Auth.docs.md)
```

**Key differences:**
- `navigation_parent: true` in frontmatter
- Status column indicates documented vs skipped
- No detailed Components & Exports for the folder itself
- Purpose notes the limited scope

---

## Complete Example

```markdown
---
title: "Services"
path: "src/API/Services/"
type: folder
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
base_commit: "abc123def"
parent: "../API.docs.md"
namespace: "MyProject.API.Services"
---

# Services

## Purpose

Business logic layer containing all domain services. Services encapsulate business rules and orchestrate data access through repositories. All services follow the constructor injection pattern and are registered as scoped dependencies.

## Components & Exports

| Component | Type | Exported | Description |
|-----------|------|----------|-------------|
| `IUserService` | interface | yes | User management contract |
| `IAuthClient` | interface | yes | Authentication operations contract |
| `UserService` | class | yes | User management implementation |
| `AuthClient` | class | yes | Authentication implementation |
| `ServiceBase` | class | yes | Base class for all services |
| `ValidationHelper` | class | no | Internal validation utilities |

## Contents

### Folders

| Folder | Purpose |
|--------|---------|
| `Validators/` | FluentValidation validators for requests |
| `Mappers/` | AutoMapper profiles |

### Files

| File | Key Types |
|------|-----------|
| `IUserService.cs` | `IUserService` |
| `UserService.cs` | `UserService` |
| `IAuthClient.cs` | `IAuthClient` |
| `AuthClient.cs` | `AuthClient` |
| `ServiceBase.cs` | `ServiceBase` |

## Dependencies

### Internal

| Dependency | Path | Purpose |
|------------|------|---------|
| `IUserRepository` | `../Repositories/` | Data access |
| `UserDto` | `../Models/` | Data transfer |

### External

| Package | Purpose |
|---------|---------|
| `FluentValidation` | Request validation |
| `AutoMapper` | Object mapping |

## Usage Notes

All services should be resolved through DI, never instantiated directly. Services assume a scoped lifetime and may hold request-specific state.

## Related Documentation

- [Parent: API](../API.docs.md)
- [Child: Validators](./Validators/Validators.docs.md)
- [Child: Mappers](./Mappers/Mappers.docs.md)
- [Related: Models](../Models/Models.docs.md)
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| File documentation | `TEMPLATES/file.md` |
| Interface handling | `RULES/interface-handling.md` |
| Focus patterns | `CONFIG-REFERENCE.md` |
