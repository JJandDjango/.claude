# Example: Focused Documentation Generation

> **Version:** 2.0.0  
> **Purpose:** Detailed walkthrough of generating documentation with focus patterns.

---

## Scenario

Document only the authentication services in a larger codebase, while maintaining navigation context.

---

## Configuration

```yaml
# documentation-config.yaml

project_name: "MyProject"
generator_version: "2.0.0"

focus:
  - "src/API/Services/Auth/**"

ignore:
  - "**/*.generated.cs"
  - "**/obj/**"
  - "**/bin/**"

auto_detect_implementations: true

glossary:
  Tenant: "An organization or customer account in the multi-tenant system"
  Claim: "A security assertion about a user's identity or permissions"
  Token: "A JWT bearer token used for authentication"

validation:
  warn_on_missing_sections: true
  warn_on_broken_links: true
```

---

## Source Tree

```
MyProject/
├── documentation-config.yaml
├── MyProject.sln
├── src/
│   └── API/
│       ├── API.csproj
│       ├── Program.cs
│       ├── Controllers/
│       │   ├── AuthController.cs
│       │   └── UserController.cs
│       ├── Services/
│       │   ├── Auth/
│       │   │   ├── IAuthService.cs
│       │   │   ├── AuthService.cs
│       │   │   ├── TokenValidator.cs
│       │   │   └── TokenGenerator.cs
│       │   └── Users/
│       │       ├── IUserService.cs
│       │       └── UserService.cs
│       └── Models/
│           ├── UserDto.cs
│           └── AuthResult.cs
└── tests/
    └── API.Tests/
        └── AuthServiceTests.cs
```

---

## Generated Documentation Structure

```
generated-documentation/
├── INDEX.md                              # ✅ Always generated
├── MyProject.docs.md                     # ✅ Always generated (root)
├── MyProject.glossary.md                 # ✅ Always generated (glossary exists)
└── src/
    └── src.docs.md                       # ✅ Navigation parent
        └── API/
            └── API.docs.md               # ✅ Navigation parent
                └── Services/
                    └── Services.docs.md  # ✅ Navigation parent
                        └── Auth/
                            ├── Auth.docs.md           # ✅ FULL documentation
                            ├── IAuthService.docs.md   # ✅ FULL (or in AuthService)
                            ├── AuthService.docs.md    # ✅ FULL documentation
                            ├── TokenValidator.docs.md # ✅ FULL documentation
                            └── TokenGenerator.docs.md # ✅ FULL documentation
```

### What's NOT Generated

```
❌ src/API/Controllers/           # Outside focus
❌ src/API/Services/Users/        # Outside focus
❌ src/API/Models/                # Outside focus
❌ tests/                         # Outside focus
```

---

## Generation Walkthrough

### Step 1: Initialization

```bash
# Parse config
PROJECT_NAME="MyProject"
FOCUS_PATTERNS=["src/API/Services/Auth/**"]

# Get file list
git ls-files > all_files.txt

# Filter to focus
# Matches: src/API/Services/Auth/*
# Result: 4 files (IAuthService.cs, AuthService.cs, TokenValidator.cs, TokenGenerator.cs)
```

### Step 2: Determine Navigation Parents

Focus path: `src/API/Services/Auth/`

Required navigation parents:
1. `src/` — parent of focused path
2. `src/API/` — parent of focused path
3. `src/API/Services/` — parent of focused path

These get minimal "navigation parent" documentation.

### Step 3: Generate Root Documents

**INDEX.md** — Initial structure (validation warnings added later)

**MyProject.docs.md** — Full root document with:
- Architecture from config
- Conventions from config
- Note that focus is limited to Auth services

**MyProject.glossary.md** — Terms: Tenant, Claim, Token

### Step 4: Process Navigation Parents

#### src.docs.md (Navigation Parent)

```markdown
---
title: "src"
path: "src/"
type: folder
navigation_parent: true
---

# src

## Purpose

Application source code. Only `API/Services/Auth/` is within documentation focus.

## Contents

| Folder | Status | Notes |
|--------|--------|-------|
| `API/` | 🔍 Partial | Contains focused Auth services |

## Related Documentation

- [Parent: MyProject](../MyProject.docs.md)
- [Child: API](./API/API.docs.md)
```

#### API.docs.md (Navigation Parent)

```markdown
---
title: "API"
path: "src/API/"
type: folder
navigation_parent: true
---

# API

## Purpose

REST API solution. Only `Services/Auth/` is within documentation focus.

## Contents

| Folder | Status | Notes |
|--------|--------|-------|
| `Controllers/` | ⏭️ Skipped | Outside focus |
| `Services/` | 🔍 Partial | Contains focused Auth services |
| `Models/` | ⏭️ Skipped | Outside focus |

## Related Documentation

- [Parent: src](../src.docs.md)
- [Child: Services](./Services/Services.docs.md)
```

#### Services.docs.md (Navigation Parent)

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

## Contents

| Folder | Status | Notes |
|--------|--------|-------|
| `Auth/` | ✅ Documented | Authentication services |
| `Users/` | ⏭️ Skipped | Outside focus |

## Related Documentation

- [Parent: API](../API.docs.md)
- [Child: Auth](./Auth/Auth.docs.md)
```

### Step 5: Spawn Subagent for Auth Folder

**Subagent Context:**

```yaml
folder_path: "src/API/Services/Auth/"
depth: 4
parent_doc: |
  # Services
  Business logic layer. Only Auth/ is within documentation focus.
  ...
files:
  - IAuthService.cs
  - AuthService.cs
  - TokenValidator.cs
  - TokenGenerator.cs
detected_implementations:
  IAuthService:
    - AuthService
```

**Subagent Modules Loaded:**
- `TEMPLATES/folder.md`
- `TEMPLATES/file.md`
- `RULES/signatures.md`
- `RULES/csharp-features.md`
- `RULES/interface-handling.md`
- `RULES/glossary-linking.md`

### Step 6: Subagent Generates Auth Documentation

#### Auth.docs.md (Full Folder Doc)

```markdown
---
title: "Auth"
path: "src/API/Services/Auth/"
type: folder
namespace: "MyProject.API.Services.Auth"
---

# Auth

## Purpose

Authentication and authorization services. Handles user authentication, 
[token](../../MyProject.glossary.md#token) generation, and validation.

## Components & Exports

| Component | Type | Exported | Description |
|-----------|------|----------|-------------|
| `IAuthService` | interface | yes | Authentication contract |
| `AuthService` | class | yes | Authentication implementation |
| `TokenValidator` | class | yes | JWT token validation |
| `TokenGenerator` | class | yes | JWT token generation |

## Contents

### Files

| File | Key Types |
|------|-----------|
| `IAuthService.cs` | `IAuthService` |
| `AuthService.cs` | `AuthService` |
| `TokenValidator.cs` | `TokenValidator` |
| `TokenGenerator.cs` | `TokenGenerator` |

## Dependencies

### Internal

| Dependency | Path | Purpose |
|------------|------|---------|
| `UserDto` | `../../Models/` | User data transfer |

### External

| Package | Purpose |
|---------|---------|
| `Microsoft.IdentityModel.Tokens` | JWT handling |

## Related Documentation

- [Parent: Services](../Services.docs.md)
```

#### AuthService.docs.md (Full File Doc)

```markdown
---
title: "AuthService"
path: "src/API/Services/Auth/AuthService.cs"
type: file
kind: "class"
namespace: "MyProject.API.Services.Auth"
implements: ["IAuthService"]
---

# AuthService

## Purpose

Implements authentication operations including credential validation, 
[token](../../../MyProject.glossary.md#token) issuance, and session management.

## Interface

### IAuthService

Contract for authentication operations.

#### Methods

```csharp
Task<AuthResult> AuthenticateAsync(string username, string password, CancellationToken ct = default)
Task<bool> ValidateTokenAsync(string token, CancellationToken ct = default)
Task RevokeTokenAsync(string token, CancellationToken ct = default)
```

## Public Signatures

### Constructors

```csharp
public AuthService(ILogger<AuthService> logger, TokenValidator validator, TokenGenerator generator)
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `AuthenticateAsync(string, string, CancellationToken)` | `Task<AuthResult>` | Validates credentials, issues token |
| `ValidateTokenAsync(string, CancellationToken)` | `Task<bool>` | Validates JWT token |
| `RevokeTokenAsync(string, CancellationToken)` | `Task` | Revokes/blacklists token |

#### `AuthenticateAsync(string username, string password, CancellationToken ct)`

```csharp
public async Task<AuthResult> AuthenticateAsync(string username, string password, CancellationToken ct = default)
```

**Parameters:**
- `username` (`string`): User's login name
- `password` (`string`): User's password
- `ct` (`CancellationToken`): Cancellation token (optional)

**Returns:** `Task<AuthResult>` - Authentication result with token or failure reason

## Dependencies

### Constructor Injected

| Dependency | Type | Lifetime | Purpose |
|------------|------|----------|---------|
| `logger` | `ILogger<AuthService>` | Singleton | Logging |
| `validator` | `TokenValidator` | Scoped | Token validation |
| `generator` | `TokenGenerator` | Scoped | Token generation |

## Related Documentation

- [Parent: Auth](./Auth.docs.md)
- [TokenValidator](./TokenValidator.docs.md)
- [TokenGenerator](./TokenGenerator.docs.md)
```

### Step 7: Subagent Returns

```yaml
status: "success"
generated_files:
  - path: "generated-documentation/src/API/Services/Auth/Auth.docs.md"
    type: "folder"
  - path: "generated-documentation/src/API/Services/Auth/AuthService.docs.md"
    type: "file"
  - path: "generated-documentation/src/API/Services/Auth/TokenValidator.docs.md"
    type: "file"
  - path: "generated-documentation/src/API/Services/Auth/TokenGenerator.docs.md"
    type: "file"
warnings: []
child_folders: []  # No subfolders
```

### Step 8: Validation

Run validation checks:
- ✅ All required sections present
- ✅ All internal links resolve
- ✅ All code references exist

### Step 9: Finalize INDEX.md

```markdown
---
type: index
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
root: "/"
total_folders: 4
total_files: 4
---

# Documentation Index

Generated: 2024-01-15T10:30:00Z
Generator Version: 2.0.0
Root: /

## Structure

MyProject/
  MyProject.docs.md - Multi-tenant authentication API
  MyProject.glossary.md - Domain terminology reference
  src/
    src.docs.md - Application source (partial)
    API/
      API.docs.md - REST API (partial)
      Services/
        Services.docs.md - Business logic (partial)
        Auth/
          Auth.docs.md - Authentication services
          AuthService.docs.md
          TokenValidator.docs.md
          TokenGenerator.docs.md

## Quick Reference

| Path | Purpose | Key Exports |
|------|---------|-------------|
| MyProject.glossary.md | Domain terminology | - |
| src/API/Services/Auth/ | Authentication | `IAuthService`, `AuthService` |

## Validation Warnings

None
```

---

## Key Behaviors Demonstrated

1. **Root always generated** — `MyProject.docs.md` exists regardless of focus
2. **Glossary always generated** — When glossary config exists
3. **Navigation parents created** — `src/`, `API/`, `Services/` get minimal docs
4. **Full documentation for focused paths** — `Auth/` gets complete treatment
5. **Siblings skipped entirely** — `Users/`, `Controllers/`, `Models/` not documented
6. **Glossary terms linked** — "Token" linked on first occurrence
7. **Clean INDEX.md** — Shows partial structure with clear indicators

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Configuration | `CONFIG-REFERENCE.md` |
| Orchestration | `ORCHESTRATOR.md` |
| Folder template | `TEMPLATES/folder.md` |
| File template | `TEMPLATES/file.md` |
