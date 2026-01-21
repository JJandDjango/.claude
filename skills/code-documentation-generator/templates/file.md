# Template: File Document (`{filename}.docs.md`)

> **Version:** 2.0.0  
> **Output:** `generated-documentation/{path}/{filename}.docs.md`  
> **Purpose:** Document a source file's classes, interfaces, and public signatures.

---

## Frontmatter Schema

```yaml
---
title: "{filename}"
path: "{relative-path-from-root}"
type: file
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
namespace: "{C#-namespace}"
namespace_matches_path: true | false

# Type classification
kind: "class" | "interface" | "struct" | "enum" | "record" | "record struct" | "delegate"
static: true | false
partial: true | false

# Relationships
implements: ["{interface-names}"]
inherits: "{base-class}"
inherits_from_documented: true | false

# Generic parameters (if applicable)
generic_parameters:
  - name: "T"
    constraints: ["IEntity", "new()"]
    description: "Entity type being operated on"

# Partial class info (if applicable)
source_files:
  - path: "{filename}.cs"
    contains: "{description}"

# Extension method info (if applicable)
extension_target: "{extended-type}"
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Filename without extension |
| `path` | string | Yes | Relative path from root |
| `type` | string | Yes | Always `"file"` |
| `kind` | string | Yes | C# type kind |
| `static` | boolean | No | `true` if static class |
| `partial` | boolean | No | `true` if partial class |
| `implements` | array | No | Implemented interfaces |
| `inherits` | string | No | Base class name |
| `inherits_from_documented` | boolean | No | `true` if base is in docs |
| `generic_parameters` | array | No | Generic type parameters |
| `extension_target` | string | No | Type extended (for extension classes) |

---

## Template

```markdown
---
title: "{filename}"
path: "{relative-path-from-root}"
type: file
kind: "class"
namespace: "{C#-namespace}"
implements: ["{interface-names}"]
inherits: "{base-class}"
---

# {filename}

## Purpose  <!-- REQUIRED -->

{What this file/class does and its responsibility}

## Source Files  <!-- CONDITIONAL: only if partial class with multiple files -->

This class is defined across multiple partial files:

| File | Contains | Lines |
|------|----------|-------|
| `{filename}.cs` | Constructor, core methods | {count} |
| `{filename}.Commands.cs` | Command handlers | {count} |

## Generic Parameters  <!-- CONDITIONAL: only if generic type -->

| Parameter | Constraints | Description |
|-----------|-------------|-------------|
| `T` | `IEntity`, `new()` | Entity type being stored |

## Interface  <!-- CONDITIONAL: only if implements interface -->

### {InterfaceName}

{Purpose of the interface - the contract this class fulfills}

#### Methods

```csharp
Task<AuthResult> AuthenticateAsync(Credentials credentials)
Task<bool> ValidateTokenAsync(string token)
```

## Inheritance  <!-- CONDITIONAL: only if inherits from documented base -->

Inherits from [{BaseClass}]({base-class-doc-path}).

### Inherited Members

See [{BaseClass}]({base-class-doc-path}) for:
- `Logger` property
- `DisposeAsync()` method

### Overridden Members

| Member | Description |
|--------|-------------|
| `ValidateAsync(T)` | Custom validation logic |

## Security  <!-- CONDITIONAL: only if authorization attributes present -->

| Endpoint | Policy | Roles |
|----------|--------|-------|
| `CreateUser` | AdminOnly | Admin |
| `GetUser` | Authenticated | - |

## Public Signatures  <!-- REQUIRED -->

### Constructors  <!-- CONDITIONAL: only if has public/protected constructors -->

```csharp
public {ClassName}({Type} {param}, {Type} {param})
```

### Properties  <!-- CONDITIONAL: only if has public/protected properties -->

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `{Name}` | `{Type}` | get | {description} |
| `{Name}` | `{Type}` | get/set | {description} |

### Methods  <!-- CONDITIONAL: only if has public/protected methods -->

| Method | Returns | Status | Description |
|--------|---------|--------|-------------|
| `{MethodName}({params})` | `{ReturnType}` | | {description} |
| `{MethodName}({params})` | `{ReturnType}` | 🔶 Override | {description} |

#### `{MethodName}({parameters})`

```csharp
[HttpPost]
[Authorize(Policy = "AdminOnly")]
public async Task<ActionResult<UserDto>> {MethodName}({Type} {param})
```

**Parameters:**
- `{paramName}` (`{Type}`): {description}

**Returns:** `{ReturnType}` - {description}

**Throws:**  <!-- OPTIONAL: only if method throws exceptions -->
- `{ExceptionType}`: {when thrown}

### Events  <!-- CONDITIONAL: only if has public/protected events -->

| Event | Type | Description |
|-------|------|-------------|
| `UserCreated` | `EventHandler<UserEventArgs>` | Raised after user creation |

### Indexers  <!-- CONDITIONAL: only if has indexers -->

```csharp
public UserDto this[int index] { get; }
public UserDto this[string name] { get; set; }
```

## Dependencies  <!-- OPTIONAL: only if has dependencies -->

### Internal

| Dependency | Path | Lifetime | Purpose |
|------------|------|----------|---------|
| `IUserRepository` | `../Repositories/` | Scoped | Data access |
| `ILogger<UserService>` | - | Singleton | Logging |

### External

| Package | Purpose |
|---------|---------|
| `{PackageName}` | {why needed} |

## Related Documentation  <!-- REQUIRED -->

- [Parent: {folder}]({folder-path})
- [Interface: {interface}]({interface-path})  <!-- if implements -->
- [Base: {base}]({base-path})  <!-- if inherits -->
```

---

## Section Details

### Purpose (REQUIRED)

Describe what this class/type does and its single responsibility.

**Source:** Extract from XML `<summary>` if present; otherwise infer from name and code.

### Source Files (CONDITIONAL)

Include only for partial classes spanning multiple files.

| Column | Description |
|--------|-------------|
| File | Source filename |
| Contains | What this partial defines (constructors, commands, etc.) |
| Lines | Line count for this partial |

### Generic Parameters (CONDITIONAL)

Include only for generic types. Document all type parameters.

| Column | Description |
|--------|-------------|
| Parameter | Type parameter name (e.g., `T`, `TResult`) |
| Constraints | List of constraints (`class`, `struct`, interface names, `new()`) |
| Description | What this parameter represents |

### Interface (CONDITIONAL)

Include when this class implements an interface. Document the full interface contract here so the file is self-contained.

**Format:**
- Interface name as H3
- Purpose of the interface
- All interface method signatures in code block

### Inheritance (CONDITIONAL)

Include when class inherits from a documented base class.

**Inherited Members:** List members from base (don't re-document)
**Overridden Members:** Document members this class overrides

### Security (CONDITIONAL)

Include when authorization attributes are present on methods.

| Column | Description |
|--------|-------------|
| Endpoint | Method name |
| Policy | Authorization policy name |
| Roles | Required roles (or `-` if policy-based) |

### Public Signatures (REQUIRED)

The core of the file documentation. Document all public and protected members.

#### Method Status Markers

| Marker | Meaning |
|--------|---------|
| (none) | Normal method |
| 🔷 Virtual | Can be overridden |
| 🔶 Override | Overrides base implementation |
| 🔒 Sealed | Cannot be further overridden |

#### Method Detail Format

For significant methods, include expanded documentation:

```markdown
#### `GetUserAsync(int id, CancellationToken ct)`

```csharp
public async Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
```

**Parameters:**
- `id` (`int`): User's database identifier
- `ct` (`CancellationToken`): Cancellation token (optional)

**Returns:** `Task<UserDto?>` - User data, or null if not found

**Throws:**
- `ArgumentOutOfRangeException`: When id is negative
```

### Dependencies (OPTIONAL)

Document constructor dependencies with their DI lifetime.

| Column | Description |
|--------|-------------|
| Dependency | Interface or type injected |
| Path | Location in codebase (or `-` for framework types) |
| Lifetime | `Singleton`, `Scoped`, `Transient`, or `-` |
| Purpose | Why this dependency is needed |

---

## Variant: Static Class

For static classes, adjust the template:

```yaml
---
kind: "class"
static: true
instantiable: false
---
```

- Skip Constructors section
- Use "Static Methods" as header instead of "Methods"
- Skip Dependencies section (static classes shouldn't have DI)

---

## Variant: Extension Methods Class

For classes containing extension methods:

```yaml
---
kind: "class"
static: true
extension_target: "System.String"
---
```

**Methods table includes Extends column:**

| Method | Extends | Returns | Description |
|--------|---------|---------|-------------|
| `ToSlug(this string)` | `string` | `string` | URL-friendly version |
| `Truncate(this string, int)` | `string` | `string` | Truncates to length |

**Signature format includes `this` modifier:**

```csharp
public static string ToSlug(this string input)
```

---

## Variant: Record Type

For records and record structs:

```yaml
---
kind: "record"  # or "record struct"
---
```

**Include Record Definition section:**

```markdown
## Record Definition

```csharp
public record UserDto(int Id, string Name, string Email);
```

### Positional Properties

| Property | Type | Description |
|----------|------|-------------|
| `Id` | `int` | User identifier (positional) |
| `Name` | `string` | Display name (positional) |
```

---

## Variant: Enum

For enums:

```yaml
---
kind: "enum"
---
```

**Use Values section instead of Public Signatures:**

```markdown
## Values

| Value | Int | Description |
|-------|-----|-------------|
| `Pending` | 0 | Order created, awaiting payment |
| `Paid` | 1 | Payment received |
| `Shipped` | 2 | Order dispatched |
| `Cancelled` | -1 | Order cancelled |
```

---

## Complete Example

```markdown
---
title: "UserService"
path: "src/API/Services/UserService.cs"
type: file
kind: "class"
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
base_commit: "abc123def"
parent: "./Services.docs.md"
namespace: "MyProject.API.Services"
namespace_matches_path: true
implements: ["IUserService"]
inherits: "ServiceBase"
inherits_from_documented: true
---

# UserService

## Purpose

Manages user lifecycle operations including creation, retrieval, updates, and soft deletion. Enforces business rules for user management and coordinates with the repository layer for persistence.

## Interface

### IUserService

Contract for user management operations. All user-related business logic flows through this interface.

#### Methods

```csharp
Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
Task<PagedResult<UserDto>> ListUsersAsync(UserFilter filter, CancellationToken ct = default)
Task<UserDto> CreateUserAsync(CreateUserRequest request, CancellationToken ct = default)
Task<UserDto> UpdateUserAsync(int id, UpdateUserRequest request, CancellationToken ct = default)
Task<bool> DeleteUserAsync(int id, CancellationToken ct = default)
```

## Inheritance

Inherits from [ServiceBase](./ServiceBase.docs.md).

### Inherited Members

See [ServiceBase](./ServiceBase.docs.md) for:
- `Logger` property
- `ValidateAsync<T>(T)` method
- `DisposeAsync()` method

## Public Signatures

### Constructors

```csharp
public UserService(ILogger<UserService> logger, IUserRepository repository, IValidator<CreateUserRequest> validator)
```

### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `Logger` | `ILogger<UserService>` | get | Inherited from ServiceBase |

### Methods

| Method | Returns | Status | Description |
|--------|---------|--------|-------------|
| `GetUserAsync(int, CancellationToken)` | `Task<UserDto?>` | | Retrieves user by ID |
| `ListUsersAsync(UserFilter, CancellationToken)` | `Task<PagedResult<UserDto>>` | | Lists users with filtering |
| `CreateUserAsync(CreateUserRequest, CancellationToken)` | `Task<UserDto>` | | Creates new user |
| `UpdateUserAsync(int, UpdateUserRequest, CancellationToken)` | `Task<UserDto>` | | Updates existing user |
| `DeleteUserAsync(int, CancellationToken)` | `Task<bool>` | | Soft-deletes user |

#### `GetUserAsync(int id, CancellationToken ct)`

```csharp
public async Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
```

**Parameters:**
- `id` (`int`): User's database identifier
- `ct` (`CancellationToken`): Cancellation token (optional)

**Returns:** `Task<UserDto?>` - User data, or null if not found

**Throws:**
- `ArgumentOutOfRangeException`: When id is negative

#### `CreateUserAsync(CreateUserRequest request, CancellationToken ct)`

```csharp
public async Task<UserDto> CreateUserAsync(CreateUserRequest request, CancellationToken ct = default)
```

**Parameters:**
- `request` (`CreateUserRequest`): User creation data
- `ct` (`CancellationToken`): Cancellation token (optional)

**Returns:** `Task<UserDto>` - Created user with assigned ID

**Throws:**
- `ValidationException`: When request fails validation
- `DuplicateEmailException`: When email already exists

## Dependencies

### Internal

| Dependency | Path | Lifetime | Purpose |
|------------|------|----------|---------|
| `IUserRepository` | `../Repositories/` | Scoped | Data access |
| `IValidator<CreateUserRequest>` | `./Validators/` | Scoped | Request validation |

### External

| Package | Purpose |
|---------|---------|
| `FluentValidation` | Validation framework |

## Related Documentation

- [Parent: Services](./Services.docs.md)
- [Interface: IUserService](./IUserService.docs.md)
- [Base: ServiceBase](./ServiceBase.docs.md)
- [Related: UserRepository](../Repositories/UserRepository.docs.md)
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Signature extraction rules | `RULES/signatures.md` |
| C# feature documentation | `RULES/csharp-features.md` |
| Interface handling | `RULES/interface-handling.md` |
| Partial classes | `RULES/partial-classes.md` |
