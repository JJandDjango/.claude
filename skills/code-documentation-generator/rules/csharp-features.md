# Rules: C# Language Features

> **Version:** 2.0.0  
> **Role:** Documentation rules for C# language features including generics, attributes, XML docs, async patterns, inheritance, records, and more.

---

## Table of Contents

1. [Generic Types](#generic-types)
2. [Attributes](#attributes)
3. [XML Documentation Extraction](#xml-documentation-extraction)
4. [Async Patterns](#async-patterns)
5. [Inheritance](#inheritance)
6. [Dependency Injection](#dependency-injection)
7. [Records and Primary Constructors](#records-and-primary-constructors)
8. [Extension Methods](#extension-methods)
9. [Enums](#enums)
10. [Static Classes](#static-classes)
11. [Events](#events)
12. [Indexers](#indexers)

---

## Generic Types

### Class-Level Generics

Document generic type parameters in frontmatter and signatures.

**Frontmatter:**
```yaml
---
title: "Repository<T>"
kind: "class"
generic_parameters:
  - name: "T"
    constraints: ["IEntity"]
    variance: null
    description: "Entity type being stored"
---
```

**Signature format:**
```csharp
public class Repository<T> where T : IEntity
public class CacheManager<TKey, TValue> where TKey : notnull where TValue : class
```

### Generic Method Signatures

Include full constraint clauses:

```csharp
public async Task<T> GetByIdAsync<T>(int id) where T : class, IEntity
public TResult Transform<TSource, TResult>(TSource input) where TResult : new()
```

### Constraints Table

When a type has generic parameters, include a Generic Parameters section:

```markdown
## Generic Parameters

| Parameter | Constraints | Variance | Description |
|-----------|-------------|----------|-------------|
| `T` | `IEntity` | — | Entity type being stored |
| `TKey` | `notnull` | — | Cache key type |
| `TValue` | `class` | — | Cached value type |
```

### Variance Annotations

For interfaces, document variance:

| Annotation | Meaning | Example |
|------------|---------|---------|
| `out T` | Covariant | `IEnumerable<out T>` |
| `in T` | Contravariant | `IComparer<in T>` |
| (none) | Invariant | `IList<T>` |

**Frontmatter for variant interface:**
```yaml
generic_parameters:
  - name: "T"
    constraints: []
    variance: "out"
    description: "Covariant result type"
```

### Constraint Types

Document all constraint types:

| Constraint | Meaning |
|------------|---------|
| `class` | Must be reference type |
| `struct` | Must be value type |
| `notnull` | Must be non-nullable |
| `new()` | Must have parameterless constructor |
| `unmanaged` | Must be unmanaged type |
| `IFoo` | Must implement interface |
| `BaseClass` | Must inherit from class |
| `T : U` | Type parameter constraint |

---

## Attributes

### Documentation Scope

| Attribute Category | Document? | Location |
|--------------------|-----------|----------|
| Routing (`[HttpGet]`, `[Route]`) | ✅ Yes | In method signature block |
| Authorization (`[Authorize]`, `[AllowAnonymous]`) | ✅ Yes | Security section |
| Validation (`[Required]`, `[MaxLength]`) | ✅ Yes | Properties table, Validation column |
| Serialization (`[JsonProperty]`, `[XmlElement]`) | ⚠️ Conditional | Only if affects public contract |
| Obsolete (`[Obsolete]`) | ✅ Yes | Note in description |
| Debugging (`[DebuggerDisplay]`) | ❌ No | Internal tooling |
| Test (`[Fact]`, `[Theory]`) | ❌ No | Tests use simplified template |
| Compiler (`[CallerMemberName]`) | ⚠️ Conditional | If affects method signature |

### Signature Block Format

Include routing and key behavioral attributes inline with signatures:

```csharp
[HttpPost("users")]
[Authorize(Policy = "AdminOnly")]
[ProducesResponseType(typeof(UserDto), 201)]
[ProducesResponseType(400)]
public async Task<ActionResult<UserDto>> CreateUser([FromBody] CreateUserRequest request)
```

### Security Section

When authorization attributes exist, add a Security section to file documentation:

```markdown
## Security

| Endpoint | Attribute | Policy/Roles | Notes |
|----------|-----------|--------------|-------|
| `CreateUser` | `[Authorize]` | AdminOnly | Admin policy required |
| `GetUser` | `[Authorize]` | — | Any authenticated user |
| `GetPublicProfile` | `[AllowAnonymous]` | — | Public endpoint |
```

### Validation Attributes on Properties

Add a Validation column to properties tables when validation attributes exist:

```markdown
### Properties

| Property | Type | Access | Validation | Description |
|----------|------|--------|------------|-------------|
| `Email` | `string` | get/set | `[Required]`, `[EmailAddress]` | User email |
| `Name` | `string` | get/set | `[Required]`, `[MaxLength(100)]` | Display name |
| `Age` | `int?` | get/set | `[Range(0, 150)]` | Optional age |
```

### Obsolete Members

Mark obsolete members clearly:

```markdown
| Method | Returns | Status | Description |
|--------|---------|--------|-------------|
| `GetUser(int)` | `User` | ⚠️ Obsolete | Use `GetUserAsync` instead |
```

In method detail:
```markdown
#### `GetUser(int id)` ⚠️ OBSOLETE

> **Deprecated:** Use `GetUserAsync(int id)` instead. Will be removed in v3.0.

```csharp
[Obsolete("Use GetUserAsync instead. Will be removed in v3.0.")]
public User GetUser(int id)
```
```

---

## XML Documentation Extraction

### Mapping Rules

| XML Tag | Maps To | Behavior |
|---------|---------|----------|
| `<summary>` | Purpose section (types), Description column (members) | Use verbatim, trim whitespace |
| `<param name="x">` | Parameter description in method detail | Merge with type information |
| `<returns>` | Returns line in method detail | Use verbatim |
| `<exception cref="T">` | Throws section | Include if present |
| `<remarks>` | Usage Notes section | Append if substantial |
| `<example>` | ❌ Skip | Too verbose for LLM docs |
| `<see cref="">` | Convert to relative doc links | Link if target documented |
| `<seealso cref="">` | Related Documentation section | Add as related link |
| `<inheritdoc>` | Resolve and inline | Follow chain to find content |
| `<value>` | Property description | Use for property Purpose |
| `<typeparam>` | Generic Parameters table | Map to description column |

### Extraction Example

**Source:**
```csharp
/// <summary>
/// Retrieves a user by their unique identifier.
/// </summary>
/// <param name="id">The user's database ID.</param>
/// <param name="ct">Cancellation token for async operation.</param>
/// <returns>The user DTO, or null if not found.</returns>
/// <exception cref="ArgumentOutOfRangeException">Thrown when id is negative.</exception>
/// <remarks>
/// This method uses caching for improved performance on repeated calls.
/// </remarks>
public async Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
```

**Generated:**
```markdown
#### `GetUserAsync(int id, CancellationToken ct)`

Retrieves a user by their unique identifier.

```csharp
public async Task<UserDto?> GetUserAsync(int id, CancellationToken ct = default)
```

**Parameters:**
- `id` (`int`): The user's database ID.
- `ct` (`CancellationToken`): Cancellation token for async operation.

**Returns:** `Task<UserDto?>` - The user DTO, or null if not found.

**Throws:**
- `ArgumentOutOfRangeException`: Thrown when id is negative.

> **Note:** This method uses caching for improved performance on repeated calls.
```

### Missing Documentation Handling

| Scenario | Behavior |
|----------|----------|
| No XML docs on public member | Infer from name/signature; optionally warn |
| Empty `<summary>` | Treat as missing |
| XML docs on private members | Ignore (private not documented) |
| `<inheritdoc>` chain unresolvable | Warn, leave description as "See base class" |
| `<inheritdoc cref="..."/>` | Resolve specific reference |
| Malformed XML | Skip tag, continue with others |

### `<inheritdoc>` Resolution

Follow the inheritance chain to find documentation:

```csharp
public interface IUserService
{
    /// <summary>Gets user by ID.</summary>
    Task<UserDto> GetUserAsync(int id);
}

public class UserService : IUserService
{
    /// <inheritdoc/>
    public Task<UserDto> GetUserAsync(int id) { }
}
```

Resolution:
1. Check `<inheritdoc cref="..."/>` for explicit target
2. Check implemented interfaces for matching member
3. Check base class for matching member
4. If unresolved, document as "See base implementation"

### `<see cref="">` Conversion

Convert XML references to markdown links:

| XML Reference | Markdown Output |
|---------------|-----------------|
| `<see cref="UserService"/>` | `[UserService](./UserService.docs.md)` |
| `<see cref="UserService.GetUserAsync"/>` | `[GetUserAsync](./UserService.docs.md#getuserasync)` |
| `<see cref="System.String"/>` | `String` (no link, external type) |

---

## Async Patterns

### Signature Format

Always include `async` keyword when present in source:

```csharp
public async Task<UserDto> GetUserAsync(int id, CancellationToken ct = default)
public async ValueTask<int> ComputeAsync()
public async IAsyncEnumerable<User> StreamUsersAsync([EnumeratorCancellation] CancellationToken ct)
```

### Return Type Documentation

| Actual Return | Document As | Description Format |
|---------------|-------------|-------------------|
| `Task` | `Task` | "Completes when {operation} finishes" |
| `Task<T>` | `Task<T>` | "Returns {T description}" |
| `ValueTask` | `ValueTask` | Same as Task; note if perf-critical |
| `ValueTask<T>` | `ValueTask<T>` | Same as Task<T> |
| `IAsyncEnumerable<T>` | `IAsyncEnumerable<T>` | "Yields {T} items as available" |

### CancellationToken Convention

| Scenario | Documentation |
|----------|---------------|
| `CancellationToken ct = default` | Note "Supports cancellation" in description |
| `CancellationToken ct` (required) | Document as required parameter |
| No cancellation token | No special note needed |
| Multiple tokens | Document purpose of each |

### Methods Table Format

```markdown
| Method | Returns | Description |
|--------|---------|-------------|
| `GetUserAsync(int, CancellationToken)` | `Task<UserDto>` | Retrieves user; supports cancellation |
| `StreamUsersAsync(CancellationToken)` | `IAsyncEnumerable<User>` | Yields users as available |
| `ComputeAsync()` | `ValueTask<int>` | High-perf compute operation |
```

---

## Inheritance

### Frontmatter Fields

```yaml
---
inherits: "ServiceBase"
inherits_from_documented: true  # false if base is external/outside focus
---
```

### Virtual/Override/Sealed Markers

| Member Status | Table Marker | Signature Block |
|---------------|--------------|-----------------|
| Normal | (none) | No modifier |
| `virtual` | 🔷 Virtual | Include `virtual` |
| `override` | 🔶 Override | Include `override` |
| `sealed override` | 🔒 Sealed | Include both |
| Inherited (not overridden) | ↗️ Inherited | Don't re-document |

### Methods Table with Inheritance

```markdown
| Method | Returns | Status | Description |
|--------|---------|--------|-------------|
| `GetUserAsync(int)` | `Task<UserDto>` | | Normal method |
| `ValidateAsync(T)` | `Task<bool>` | 🔶 Override | Custom validation |
| `OnInitialized()` | `void` | 🔷 Virtual | Extension point |
| `Dispose()` | `void` | 🔒 Sealed | Cleanup; cannot override |
| `LogAsync(string)` | `Task` | ↗️ Inherited | See ServiceBase |
```

### Inherited Members Section

Don't re-document members that are purely inherited. Instead, link to base:

```markdown
## Inheritance

Inherits from [ServiceBase](./ServiceBase.docs.md).

### Inherited Members

See [ServiceBase](./ServiceBase.docs.md) for:
- `Logger` property
- `DisposeAsync()` method
- `OnInitialized()` protected method

### Overridden Members

| Member | Type | Description |
|--------|------|-------------|
| `ValidateAsync(T)` | method | Custom validation with tenant check |
```

### Abstract Members

For abstract classes, mark abstract members:

```markdown
| Method | Returns | Status | Description |
|--------|---------|--------|-------------|
| `ProcessAsync()` | `Task` | 📋 Abstract | Must be implemented by subclass |
```

---

## Dependency Injection

### Constructor Dependencies Table

Document injected dependencies with lifetime information:

```markdown
## Dependencies

### Constructor Injected

| Dependency | Type | Lifetime | Optional | Purpose |
|------------|------|----------|----------|---------|
| `logger` | `ILogger<UserService>` | Singleton | No | Logging |
| `repository` | `IUserRepository` | Scoped | No | Data access |
| `cache` | `IMemoryCache` | Singleton | No | Response caching |
| `emailService` | `IEmailService` | Scoped | Yes | Notifications |
```

**Determining lifetime:**
- Check DI registration in startup files
- Common patterns: `ILogger<T>` → Singleton, `DbContext` → Scoped
- If unknown, omit or mark as "—"

**Detecting optional:**
- Parameter has default value (`= null`)
- Parameter is nullable (`IEmailService?`)
- Uses `[FromServices]` with nullable

### Service Registration Extraction

Scan configured startup files for registrations:

```csharp
// Patterns to extract:
services.AddScoped<IUserService, UserService>();
services.AddSingleton<IAuthClient, AuthClient>();
services.AddTransient<IEmailService, EmailService>();
services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

// Also recognize:
services.AddHttpClient<IExternalApi, ExternalApiClient>();
services.AddDbContext<AppDbContext>();
```

---

## Records and Primary Constructors

### Record Types

**Frontmatter:**
```yaml
---
title: "UserDto"
kind: "record"  # or "record struct"
---
```

**Record Definition section:**

```markdown
## Record Definition

```csharp
public record UserDto(int Id, string Name, string Email);
```

### Positional Properties

| Property | Type | Positional | Description |
|----------|------|------------|-------------|
| `Id` | `int` | Yes | User identifier |
| `Name` | `string` | Yes | Display name |
| `Email` | `string` | Yes | Contact email |

### Additional Members

| Member | Type | Description |
|--------|------|-------------|
| `IsActive` | `bool` | Computed from status |
| `FullName` | `string` | Computed property |
```

### Record Struct

Same format with `kind: "record struct"`:

```csharp
public readonly record struct Point(int X, int Y);
```

### Primary Constructors (C# 12)

For classes with primary constructors:

```csharp
public class UserService(ILogger<UserService> logger, IUserRepository repo) : IUserService
```

**Document as:**

```markdown
## Constructor (Primary)

```csharp
public UserService(ILogger<UserService> logger, IUserRepository repo)
```

**Captured Parameters:**

| Parameter | Type | Purpose |
|-----------|------|---------|
| `logger` | `ILogger<UserService>` | Logging instance |
| `repo` | `IUserRepository` | Data access |

Note: Primary constructor parameters are captured as private fields.
```

---

## Extension Methods

### File-Level Metadata

```yaml
---
title: "StringExtensions"
kind: "class"
static: true
extension_target: "System.String"
---
```

### Methods Table with Extends Column

```markdown
## Static Methods

| Method | Extends | Returns | Description |
|--------|---------|---------|-------------|
| `ToSlug(this string)` | `string` | `string` | URL-friendly version |
| `Truncate(this string, int)` | `string` | `string` | Truncates to max length |
| `IsValidEmail(this string)` | `string` | `bool` | Email format check |
```

### Signature Format

Always include the `this` modifier:

```csharp
public static string ToSlug(this string input)
public static string Truncate(this string input, int maxLength, string suffix = "...")
public static bool IsValidEmail(this string input)
```

### Cross-Reference to Extended Type

If the extended type is documented in this codebase:

```markdown
## Extends

This class extends [User](../Models/User.docs.md) with additional methods.

## Extended By

These extension classes add methods to this type:
- [UserExtensions](../Extensions/UserExtensions.docs.md): `ToDto`, `Validate`
```

### Orphan Extension Warning

When extension target is not documented:

```
WARN: Extension in StringExtensions.cs extends "System.String" which is not documented
```

This is informational—extensions of framework types are valid.

---

## Enums

### Frontmatter

```yaml
---
title: "OrderStatus"
kind: "enum"
---
```

### Values Table

Replace Public Signatures section with Values section:

```markdown
## Values

| Value | Integer | Description |
|-------|---------|-------------|
| `Pending` | 0 | Order created, awaiting payment |
| `Paid` | 1 | Payment received |
| `Processing` | 2 | Order being prepared |
| `Shipped` | 3 | Order dispatched |
| `Delivered` | 4 | Order received by customer |
| `Cancelled` | -1 | Order cancelled |
| `Refunded` | -2 | Payment refunded |
```

### Flags Enums

For `[Flags]` enums, note the attribute and show combined values:

```markdown
## Values

> **Note:** This is a flags enum. Values can be combined.

| Value | Integer | Description |
|-------|---------|-------------|
| `None` | 0 | No permissions |
| `Read` | 1 | Can read resources |
| `Write` | 2 | Can modify resources |
| `Delete` | 4 | Can delete resources |
| `Admin` | 7 | All permissions (Read + Write + Delete) |
```

### Enum from XML Docs

Extract descriptions from XML documentation on enum members:

```csharp
public enum OrderStatus
{
    /// <summary>Order created, awaiting payment.</summary>
    Pending = 0,
    
    /// <summary>Payment received.</summary>
    Paid = 1
}
```

---

## Static Classes

### Frontmatter

```yaml
---
title: "MathHelpers"
kind: "class"
static: true
instantiable: false
---
```

### Template Adjustments

1. **Skip Constructors section** — static classes have none
2. **Use "Static Methods" header** instead of "Methods"
3. **Skip Dependencies section** — static classes shouldn't use DI

```markdown
## Public Signatures

### Static Properties

| Property | Type | Description |
|----------|------|-------------|
| `Pi` | `double` | Mathematical constant π |
| `E` | `double` | Euler's number |

### Static Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `Clamp(int, int, int)` | `int` | Constrains value to range |
| `Lerp(float, float, float)` | `float` | Linear interpolation |
```

---

## Events

### Events Table

```markdown
### Events

| Event | Type | Description |
|-------|------|-------------|
| `UserCreated` | `EventHandler<UserEventArgs>` | Raised after user creation |
| `UserDeleted` | `EventHandler<UserEventArgs>` | Raised before user deletion |
| `PropertyChanged` | `PropertyChangedEventHandler` | Standard INPC event |
| `MessageReceived` | `Action<string>` | Simple delegate event |
```

### Event Args Documentation

If custom EventArgs are defined, document them:

```markdown
### UserEventArgs

```csharp
public class UserEventArgs : EventArgs
{
    public int UserId { get; init; }
    public string Action { get; init; }
    public DateTime Timestamp { get; init; }
}
```

| Property | Type | Description |
|----------|------|-------------|
| `UserId` | `int` | Affected user ID |
| `Action` | `string` | Action performed |
| `Timestamp` | `DateTime` | When event occurred |
```

---

## Indexers

### Indexers Section

```markdown
### Indexers

```csharp
public UserDto this[int index] { get; }
public UserDto this[string name] { get; set; }
```

| Indexer | Type | Access | Description |
|---------|------|--------|-------------|
| `this[int]` | `UserDto` | get | Access user by position |
| `this[string]` | `UserDto` | get/set | Access user by name |
```

### Multiple Indexers

Document each overload:

```csharp
public T this[int index] { get; set; }
public T this[string key] { get; set; }
public T this[int row, int col] { get; set; }
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Signature extraction | `RULES/signatures.md` |
| File template | `TEMPLATES/file.md` |
| Configuration | `CONFIG-REFERENCE.md` |
| Validation | `VALIDATION.md` |
