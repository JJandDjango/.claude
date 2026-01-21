# Rules: Signature Extraction

> **Version:** 2.0.0  
> **Role:** Defines what to extract from source code and how to determine public API surface.

---

## Overview

The "public signatures" referenced throughout this specification follow specific rules for what gets documented based on C# access modifiers and member types.

---

## Access Modifier Rules

| Modifier | Document? | Rationale |
|----------|-----------|-----------|
| `public` | ✅ Always | Part of public API surface |
| `protected` | ✅ Always | Part of inheritance contract; subclasses need this |
| `protected internal` | ✅ Always | Accessible to inheritors across assemblies |
| `internal` | ⚠️ Conditional | Only if `include_internal: true` in config |
| `private protected` | ❌ Never | Too narrow; effectively implementation detail |
| `private` | ❌ Never | Implementation detail |

### Configuration Override

```yaml
# documentation-config.yaml
signature_scope:
  include_internal: false  # default: false; set true for SDK/library projects
  include_protected: true  # default: true; set false to document only public
```

**When to enable `include_internal`:**
- Public SDK or library projects
- Packages consumed by other teams
- Projects where internal API stability matters

---

## Member Type Rules

| Member Type | Document If... |
|-------------|----------------|
| Classes | Public or protected nested classes |
| Interfaces | All members (implicitly public) |
| Structs | Public or protected |
| Enums | Public or protected (include all values) |
| Records | Public or protected (include positional properties) |
| Delegates | Public or protected |
| Methods | Access modifier qualifies per table above |
| Properties | Access modifier qualifies; document get/set accessibility |
| Fields | Public or protected only (rare in well-designed APIs) |
| Events | Public or protected |
| Constructors | Public or protected |
| Finalizers | ❌ Never (implementation detail) |
| Operators | Public (operators are always public or not defined) |
| Indexers | Public or protected |

---

## Special Member Handling

### Static Members

Follow the same access rules. Document `public static` methods, properties, and fields.

```csharp
// ✅ Document
public static UserService Instance { get; }
public static async Task<User> GetDefaultUserAsync() { }

// ❌ Skip
private static readonly object _lock = new();
```

### Nested Types

Document public/protected nested types. Private nested types are implementation details.

```csharp
public class UserService
{
    // ✅ Document - public nested type
    public class UserNotFoundException : Exception { }
    
    // ✅ Document - protected nested type  
    protected class CacheEntry { }
    
    // ❌ Skip - private nested type
    private class InternalState { }
}
```

### Explicit Interface Implementations

Document these in the "Interface" section of the implementing class, as they represent the contract being fulfilled.

```csharp
public class UserService : IUserService, IDisposable
{
    // ✅ Document in Interface section
    void IDisposable.Dispose() { }
    
    // ✅ Document in Interface section
    Task<User> IUserService.GetUserAsync(int id) { }
}
```

### Property Accessors

Document the accessibility of both get and set:

| Property Definition | Document As |
|--------------------|-------------|
| `public string Name { get; set; }` | get/set |
| `public string Name { get; }` | get |
| `public string Name { get; private set; }` | get |
| `public string Name { get; protected set; }` | get/set (note protected set) |
| `public string Name { get; init; }` | get/init |

---

## Extraction Examples

### Full Class Example

```csharp
public class UserService : IUserService
{
    // ✅ Documented - public constructor
    public UserService(ILogger logger, IRepository repo) { }
    
    // ✅ Documented - public method
    public async Task<UserDto> GetUserAsync(int id) { }
    
    // ✅ Documented - protected virtual (inheritance contract)
    protected virtual void OnUserLoaded(User user) { }
    
    // ✅ Documented - public property
    public ILogger Logger { get; }
    
    // ✅ Documented - public event
    public event EventHandler<UserEventArgs> UserCreated;
    
    // ❌ Skipped - internal (unless include_internal: true)
    internal void RefreshCache() { }
    
    // ❌ Skipped - private
    private bool ValidateId(int id) { }
    
    // ❌ Skipped - private field
    private readonly IRepository _repo;
}
```

### Interface Example

All interface members are implicitly public and always documented:

```csharp
public interface IUserService
{
    // ✅ All documented
    Task<UserDto> GetUserAsync(int id);
    Task<UserDto> CreateUserAsync(CreateUserRequest request);
    Task<bool> DeleteUserAsync(int id);
    
    // ✅ Properties documented
    ILogger Logger { get; }
    
    // ✅ Events documented
    event EventHandler<UserEventArgs> UserCreated;
}
```

### Static Class Example

```csharp
public static class StringExtensions
{
    // ✅ Documented - public static method
    public static string ToSlug(this string input) { }
    
    // ✅ Documented - public static method
    public static string Truncate(this string input, int maxLength) { }
    
    // ❌ Skipped - private static
    private static readonly Regex SlugRegex = new(@"\s+");
}
```

---

## Signature Format Standards

### Method Signatures

Include full signature with:
- Access modifier
- Static/async/virtual/override modifiers
- Return type (including Task wrapping)
- Method name
- Generic parameters with constraints
- Parameters with types and names
- Default values for optional parameters

```csharp
public async Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
protected virtual void OnUserLoaded(User user)
public static string ToSlug(this string input)
```

### Property Signatures

Include:
- Access modifier
- Static modifier if applicable
- Type
- Name
- Accessor list

```csharp
public string Name { get; set; }
public static UserService Instance { get; }
public IReadOnlyList<User> Users { get; }
```

### Constructor Signatures

Include:
- Access modifier
- Class name
- Parameters

```csharp
public UserService(ILogger<UserService> logger, IUserRepository repository)
protected UserService()  // Protected for inheritance
```

### Event Signatures

Include:
- Access modifier
- Event keyword
- Delegate type
- Name

```csharp
public event EventHandler<UserEventArgs> UserCreated
public event Action<string> MessageReceived
```

---

## Extraction Priority

When context is limited (large files), extract in this priority order:

1. **Public class/interface declarations** — Type exists and its purpose
2. **Public interface implementations** — Contract fulfillment
3. **Public constructors** — How to instantiate
4. **Public method signatures** — What operations are available
5. **Public property signatures** — What data is exposed
6. **Public events** — What notifications are available
7. **Protected members** — Inheritance contract
8. **Internal members** — Only if configured

---

## Documentation Output

### Methods Table Format

| Method | Returns | Status | Description |
|--------|---------|--------|-------------|
| `GetUserAsync(int, CancellationToken)` | `Task<UserDto?>` | | Retrieves user by ID |
| `OnUserLoaded(User)` | `void` | 🔷 Virtual | Called after user loads |

### Properties Table Format

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `Logger` | `ILogger<UserService>` | get | Logging instance |
| `Name` | `string` | get/set | User display name |
| `Id` | `int` | get/init | Immutable identifier |

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| C# language features | `RULES/csharp-features.md` |
| File template | `TEMPLATES/file.md` |
| Configuration | `CONFIG-REFERENCE.md` |
