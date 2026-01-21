# Rules: Partial Class Handling

> **Version:** 2.0.0  
> **Role:** Defines how partial classes are detected, consolidated, and documented as unified types.

---

## Overview

C# partial classes (`partial class Foo`) split a single logical class across multiple files. The generator consolidates these into unified documentation.

**Key principle:** One logical class = one documentation file.

---

## Detection

### Identifying Partial Classes

Scan for `partial` keyword in type declarations:

```csharp
// File: UserService.cs
public partial class UserService { }

// File: UserService.Commands.cs  
public partial class UserService { }

// File: UserService.Queries.cs
public partial class UserService { }
```

**Pattern:** `(public|internal|protected|private)?\s*(static)?\s*partial\s+(class|struct|interface|record)\s+(\w+)`

### Matching Partials

Match partials by fully-qualified name (namespace + type name):

```csharp
// These are the SAME class:
namespace MyProject.Services
{
    public partial class UserService { }  // in UserService.cs
}

namespace MyProject.Services
{
    public partial class UserService { }  // in UserService.Commands.cs
}

// This is a DIFFERENT class:
namespace MyProject.Internal
{
    public partial class UserService { }  // Different namespace!
}
```

### Partial Types Supported

| Type | Supported | Notes |
|------|-----------|-------|
| `partial class` | ✅ Yes | Most common |
| `partial struct` | ✅ Yes | Same rules apply |
| `partial record` | ✅ Yes | Consolidate positional properties |
| `partial interface` | ✅ Yes | Consolidate all members |
| `partial record struct` | ✅ Yes | Same as record |

---

## Documentation Strategy

### Same Folder (Common Case)

When all partials are in the same folder, generate single documentation file:

```
Source:
  src/API/Services/
    UserService.cs
    UserService.Commands.cs
    UserService.Queries.cs

Generated:
  generated-documentation/src/API/Services/
    UserService.docs.md  ← Single consolidated doc
```

### Different Folders (Rare)

When partials exist in multiple folders, document in the folder containing the "primary" partial:

```
Source:
  src/API/Services/UserService.cs        ← Primary (has constructor)
  src/API/Services/Commands/UserService.Commands.cs
  
Generated:
  generated-documentation/src/API/Services/
    UserService.docs.md  ← Primary location
```

---

## Determining Primary File

When partials exist in multiple folders, select primary location by priority:

| Priority | Criterion | Rationale |
|----------|-----------|-----------|
| 1 | File containing constructor(s) | Constructors indicate "main" definition |
| 2 | File with most public methods | Core functionality location |
| 3 | File with class-level XML docs | Documentation intent |
| 4 | Alphabetically first filename | Deterministic tiebreaker |

### Example

```
UserService.cs           → Has constructor, 2 methods
UserService.Commands.cs  → 5 methods
UserService.Queries.cs   → 8 methods

Primary: UserService.cs (has constructor, wins over method count)
```

---

## Frontmatter for Partial Classes

```yaml
---
title: "UserService"
path: "src/API/Services/"
type: file
kind: "class"
partial: true
source_files:
  - path: "UserService.cs"
    contains: "constructors, core methods"
    lines: 120
  - path: "UserService.Commands.cs"
    contains: "command handlers"
    lines: 340
  - path: "UserService.Queries.cs"
    contains: "query methods"
    lines: 387
combined_line_count: 847
namespace: "MyProject.API.Services"
implements: ["IUserService"]
---
```

| Field | Type | Description |
|-------|------|-------------|
| `partial` | boolean | Always `true` for partial classes |
| `source_files` | array | List of all partial files |
| `source_files[].path` | string | Filename |
| `source_files[].contains` | string | What this partial defines |
| `source_files[].lines` | integer | Line count |
| `combined_line_count` | integer | Total lines across all partials |

---

## Document Structure

### Source Files Section

Required for partial classes:

```markdown
## Source Files

This class is defined across multiple partial files:

| File | Contains | Lines |
|------|----------|-------|
| `UserService.cs` | Constructor, core methods, DI setup | 120 |
| `UserService.Commands.cs` | Command handlers (Create, Update, Delete) | 340 |
| `UserService.Queries.cs` | Query methods (Get, List, Search) | 387 |

**Total:** 847 lines
```

### Aggregated Signatures

Combine public signatures from ALL partial files:

```markdown
## Public Signatures

### Constructors

```csharp
// From: UserService.cs
public UserService(ILogger<UserService> logger, IRepository repository)
```

### Methods

| Method | Returns | Source | Description |
|--------|---------|--------|-------------|
| `GetUserAsync(int)` | `Task<UserDto>` | Queries | Retrieves user by ID |
| `ListUsersAsync(Filter)` | `Task<PagedResult>` | Queries | Lists with filtering |
| `CreateUserAsync(Request)` | `Task<UserDto>` | Commands | Creates new user |
| `UpdateUserAsync(int, Request)` | `Task<UserDto>` | Commands | Updates user |
| `DeleteUserAsync(int)` | `Task<bool>` | Commands | Soft-deletes user |
```

### Source Column in Methods Table

When `partial_class_handling.show_source_file_column: true` (default), include Source column indicating which partial file defines each method.

**Source values:** Use short identifier from filename:
- `UserService.Commands.cs` → `Commands`
- `UserService.Queries.cs` → `Queries`
- `UserService.cs` → `Core` or `Main`

---

## XML Documentation Handling

### Consolidation Rules

| Scenario | Behavior |
|----------|----------|
| Class-level `<summary>` in one file | Use it |
| Class-level `<summary>` in multiple files | Use first non-empty; warn about conflict |
| Same member in multiple partials | Impossible in C# (compiler error) |
| `<inheritdoc/>` on partial | Resolve normally |

### Conflict Warning

When multiple partials have conflicting class-level XML docs:

```
WARN: Partial class "UserService" has conflicting XML documentation:
      - UserService.cs: "Manages user lifecycle operations"
      - UserService.Commands.cs: "Handles user commands"
      Using first: "Manages user lifecycle operations"
```

---

## Edge Cases

### Partial with Only Private Members

Include in `source_files` list even if no public members:

```yaml
source_files:
  - path: "UserService.cs"
    contains: "constructors, public API"
    lines: 150
  - path: "UserService.Internal.cs"
    contains: "internal implementation helpers"
    lines: 80
```

Note in Contains column that it's internal.

### Partial Outside Focus Patterns

When some partials are outside focus:

1. Document only focused partials
2. Add warning about incomplete view
3. Note missing partials in Source Files table

```markdown
## Source Files

| File | Contains | Status |
|------|----------|--------|
| `UserService.cs` | Constructor, core methods | ✅ Documented |
| `UserService.Commands.cs` | Command handlers | ✅ Documented |
| `UserService.Internal.cs` | Internal helpers | ⚠️ Outside focus |

> **Note:** This documentation may be incomplete. `UserService.Internal.cs` is outside focus patterns.
```

**Validation warning:**
```
WARN: Partial class "UserService" has files outside focus patterns:
      - src/API/Services/UserService.cs (documented)
      - src/API/Services/UserService.Commands.cs (documented)
      - src/API/Internal/UserService.Internal.cs (NOT documented - outside focus)
```

### Partial Interface

Same rules apply—consolidate all partial interface files:

```csharp
// IUserService.cs
public partial interface IUserService
{
    Task<UserDto> GetUserAsync(int id);
}

// IUserService.Commands.cs
public partial interface IUserService
{
    Task<UserDto> CreateUserAsync(CreateUserRequest request);
}
```

Document all members in single `IUserService.docs.md`.

### Partial Record

Consolidate positional properties from primary declaration with additional members from partials:

```csharp
// UserRecord.cs
public partial record UserRecord(int Id, string Name);

// UserRecord.Computed.cs
public partial record UserRecord
{
    public string DisplayName => $"{Name} (#{Id})";
}
```

---

## Configuration

```yaml
# documentation-config.yaml

partial_class_handling:
  enabled: true                    # default: true; consolidate partials
  warn_on_incomplete: true         # default: true; warn if partials outside focus
  show_source_file_column: true    # default: true; show source in method tables
```

When `enabled: false`:
- Each partial file gets its own documentation
- No consolidation attempted
- May result in confusing duplicate type documentation

---

## Complete Example

```markdown
---
title: "UserService"
path: "src/API/Services/"
type: file
kind: "class"
partial: true
source_files:
  - path: "UserService.cs"
    contains: "Constructor, DI setup, core methods"
    lines: 120
  - path: "UserService.Commands.cs"
    contains: "Command handlers"
    lines: 340
  - path: "UserService.Queries.cs"
    contains: "Query methods"
    lines: 387
combined_line_count: 847
namespace: "MyProject.API.Services"
implements: ["IUserService"]
inherits: "ServiceBase"
---

# UserService

## Purpose

Manages user lifecycle operations including creation, retrieval, updates, and soft deletion. Split across multiple files for organization.

## Source Files

This class is defined across multiple partial files:

| File | Contains | Lines |
|------|----------|-------|
| `UserService.cs` | Constructor, DI setup, core methods | 120 |
| `UserService.Commands.cs` | Command handlers (Create, Update, Delete) | 340 |
| `UserService.Queries.cs` | Query methods (Get, List, Search) | 387 |

**Total:** 847 lines

## Interface

### IUserService

{Interface contract...}

## Public Signatures

### Constructors

```csharp
// From: UserService.cs
public UserService(ILogger<UserService> logger, IUserRepository repository)
```

### Properties

| Property | Type | Access | Source | Description |
|----------|------|--------|--------|-------------|
| `Logger` | `ILogger` | get | Core | Logging instance |

### Methods

| Method | Returns | Source | Description |
|--------|---------|--------|-------------|
| `GetUserAsync(int)` | `Task<UserDto?>` | Queries | Retrieves user by ID |
| `ListUsersAsync(UserFilter)` | `Task<PagedResult<UserDto>>` | Queries | Lists with filtering |
| `SearchUsersAsync(string)` | `Task<IReadOnlyList<UserDto>>` | Queries | Full-text search |
| `CreateUserAsync(CreateUserRequest)` | `Task<UserDto>` | Commands | Creates new user |
| `UpdateUserAsync(int, UpdateUserRequest)` | `Task<UserDto>` | Commands | Updates user |
| `DeleteUserAsync(int)` | `Task<bool>` | Commands | Soft-deletes user |

## Related Documentation

- [Parent: Services](./Services.docs.md)
- [Interface: IUserService](./IUserService.docs.md)
- [Base: ServiceBase](./ServiceBase.docs.md)
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| File template | `TEMPLATES/file.md` |
| Signature rules | `RULES/signatures.md` |
| Validation | `VALIDATION.md` |
| Configuration | `CONFIG-REFERENCE.md` |
