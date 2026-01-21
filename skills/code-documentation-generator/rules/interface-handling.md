# Rules: Interface Handling

> **Version:** 2.0.0  
> **Role:** Defines how interfaces are detected, where they're documented, and how multiple implementations are handled.

---

## Overview

Interfaces can be documented in three ways:
1. **Within implementation file** (default) — Interface contract embedded in implementing class doc
2. **Standalone file** — Separate `IFoo.docs.md` via manual mapping
3. **In folder doc** — For unimplemented interfaces

---

## Auto-Detection

When `auto_detect_implementations: true` (default):

### Step 1: Scan for Interfaces

Find all interface declarations:
```csharp
public interface IUserService { }
internal interface ICache { }  // Only if include_internal: true
```

Pattern: `(public|internal)?\s+interface\s+I\w+`

### Step 2: Find Implementations

Search for classes implementing each interface:
```csharp
public class UserService : IUserService { }
public class CachedUserService : ServiceBase, IUserService, IDisposable { }
```

Pattern: `class\s+\w+\s*.*:\s*.*I{InterfaceName}`

### Step 3: Build Mapping

Create interface → implementations map:
```yaml
IUserService:
  - UserService
  - CachedUserService
IAuthClient:
  - AuthClient
  - MockAuthClient
IExternalService: []  # No implementations found
```

### Step 4: Merge with Manual Mappings

Manual `interface_mappings` in config override auto-detected:
```yaml
interface_mappings:
  "IAuthClient.cs": "IAuthClient.docs.md"  # Forces standalone doc
```

---

## Default Behavior: Interface in Implementation File

When an interface has one or more implementations, document the interface within each implementation file.

### Single Implementation

```
Source:
  IUserService.cs
  UserService.cs (implements IUserService)

Generated:
  UserService.docs.md ← Contains IUserService contract
```

The implementation doc includes an Interface section:

```markdown
## Interface

### IUserService

Contract for user management operations. Defines the public API for user CRUD operations.

#### Methods

```csharp
Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
Task<UserDto> CreateUserAsync(CreateUserRequest request, CancellationToken ct = default)
Task<bool> DeleteUserAsync(int id, CancellationToken ct = default)
```

#### Properties

```csharp
ILogger Logger { get; }
```

## Public Signatures

### UserService : IUserService

{Implementation signatures follow...}
```

### Multiple Implementations

When an interface has multiple implementations, the interface contract is documented in **each** implementation file:

```
Source:
  IAuthClient.cs
  AuthClient.cs (implements IAuthClient)
  MockAuthClient.cs (implements IAuthClient)

Generated:
  AuthClient.docs.md ← Contains IAuthClient contract
  MockAuthClient.docs.md ← Contains IAuthClient contract (duplicated)
```

**Rationale:** Each implementation doc should be self-contained. A reader viewing `MockAuthClient.docs.md` shouldn't need to navigate elsewhere to understand the contract.

### Interface Section Format

```markdown
## Interface

### IAuthClient

Authentication client contract for validating credentials and tokens.

#### Methods

```csharp
Task<AuthResult> AuthenticateAsync(Credentials credentials)
Task<bool> ValidateTokenAsync(string token)
Task RevokeTokenAsync(string token)
```

**Notes:**
- Implementations must handle token expiration gracefully
- `AuthenticateAsync` should never throw; return failure result instead
```

---

## Unimplemented Interfaces

When an interface has no implementations found in the documented codebase, document it in the **folder document**.

### Detection

Interface is "unimplemented" when:
- No class in focus patterns implements it
- Implementation exists but is outside focus patterns
- Implementation is in external package

### Folder Document Format

```markdown
## Unimplemented Interfaces

The following interfaces in this folder have no implementations found in the documented codebase:

| Interface | File | Likely Reason |
|-----------|------|---------------|
| `IExternalService` | `IExternalService.cs` | Implemented by external package |
| `IFutureFeature` | `IFutureFeature.cs` | Not yet implemented |
| `ITenantResolver` | `ITenantResolver.cs` | Implementation outside focus |

### IExternalService

```csharp
public interface IExternalService
{
    Task<Response> ProcessAsync(Request request);
    Task<HealthStatus> CheckHealthAsync();
}
```

Contract for external service integration. Implementation expected to be provided by consumer package or dependency injection.

---

### IFutureFeature

```csharp
public interface IFutureFeature
{
    Task EnableAsync(FeatureConfig config);
}
```

Placeholder for upcoming feature. No implementation exists yet.
```

---

## Custom Mappings

Override default behavior via `interface_mappings` in config.

### Standalone Interface Documentation

Force an interface to have its own documentation file:

```yaml
interface_mappings:
  "IAuthClient.cs": "IAuthClient.docs.md"
```

**Result:**
- `IAuthClient.docs.md` created as standalone file
- Implementation files (`AuthClient.docs.md`) reference but don't duplicate

**Implementation file format when interface is standalone:**

```markdown
## Interface

Implements [IAuthClient](./IAuthClient.docs.md).

## Public Signatures

### AuthClient : IAuthClient

{Only implementation-specific signatures here}
```

### Grouped Interface Documentation

Group multiple related interfaces into one doc:

```yaml
interface_mappings:
  "IUserRepository.cs": "Repositories.docs.md"
  "IProductRepository.cs": "Repositories.docs.md"
  "IOrderRepository.cs": "Repositories.docs.md"
```

**Result:**
- Single `Repositories.docs.md` contains all three interface contracts
- Useful for related interfaces following same pattern

### When to Use Custom Mappings

| Scenario | Recommended Approach |
|----------|---------------------|
| Single implementation | Default (interface in impl file) |
| Multiple implementations | Default (duplicate interface) |
| Interface-only package | Custom → standalone files |
| Repository pattern family | Custom → grouped file |
| Complex interface hierarchy | Custom → standalone files |

---

## Interface Documentation Content

### Required Elements

1. **Interface name** as H3 heading
2. **Purpose description** (from XML docs or inferred)
3. **Full method signatures** in code block
4. **Property signatures** if any

### Optional Elements

1. **Notes** on implementation requirements
2. **Constraints** or expected behavior
3. **Related interfaces** links

### Example Complete Interface Documentation

```markdown
### IUserService

Contract for user management operations. Implementations handle user lifecycle including creation, retrieval, updates, and soft deletion.

#### Methods

```csharp
Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
Task<PagedResult<UserDto>> ListUsersAsync(UserFilter filter, CancellationToken ct = default)
Task<UserDto> CreateUserAsync(CreateUserRequest request, CancellationToken ct = default)
Task<UserDto> UpdateUserAsync(int id, UpdateUserRequest request, CancellationToken ct = default)
Task<bool> DeleteUserAsync(int id, CancellationToken ct = default)
```

#### Properties

```csharp
ILogger Logger { get; }
```

#### Events

```csharp
event EventHandler<UserEventArgs> UserCreated;
event EventHandler<UserEventArgs> UserDeleted;
```

**Implementation Notes:**
- `DeleteUserAsync` performs soft delete; user record retained with `IsDeleted` flag
- All methods should respect tenant context from current request
- Implementations must be thread-safe for scoped DI lifetime
```

---

## Generic Interfaces

For generic interfaces, include type parameters:

```markdown
### IRepository<T> where T : IEntity

Generic repository contract for entity persistence.

#### Methods

```csharp
Task<T?> GetByIdAsync(int id, CancellationToken ct = default)
Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default)
Task<T> AddAsync(T entity, CancellationToken ct = default)
Task UpdateAsync(T entity, CancellationToken ct = default)
Task DeleteAsync(int id, CancellationToken ct = default)
```

#### Type Parameters

| Parameter | Constraints | Description |
|-----------|-------------|-------------|
| `T` | `IEntity` | Entity type being persisted |
```

---

## Interface Inheritance

When interfaces inherit from other interfaces:

```csharp
public interface IUserService : IService, IDisposable
{
    Task<UserDto> GetUserAsync(int id);
}
```

**Document as:**

```markdown
### IUserService

Extends: `IService`, `IDisposable`

User management contract building on base service infrastructure.

#### Own Methods

```csharp
Task<UserDto> GetUserAsync(int id)
```

#### Inherited from IService

See [IService](./IService.docs.md) for:
- `InitializeAsync()`
- `Logger` property

#### Inherited from IDisposable

- `Dispose()` — Standard disposal pattern
```

---

## Configuration Reference

```yaml
# documentation-config.yaml

# Enable/disable auto-detection
auto_detect_implementations: true  # default: true

# Manual overrides
interface_mappings:
  # Standalone documentation
  "IAuthClient.cs": "IAuthClient.docs.md"
  
  # Grouped documentation  
  "IUserRepository.cs": "Repositories.docs.md"
  "IProductRepository.cs": "Repositories.docs.md"
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| File template | `TEMPLATES/file.md` |
| Folder template | `TEMPLATES/folder.md` |
| Signature rules | `RULES/signatures.md` |
| C# features | `RULES/csharp-features.md` |
