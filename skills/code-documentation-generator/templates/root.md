# Template: Root Document (`{project-name}.docs.md`)

> **Version:** 2.0.0  
> **Output:** `generated-documentation/{project-name}.docs.md`  
> **Purpose:** Project-level overview, architecture, and navigation entry point.

---

## Frontmatter Schema

```yaml
---
title: "{project-name}"
path: "/"
type: root
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
pr_number: "{pr-number}"  # if applicable
solutions:
  - name: "{solution-name}"
    path: "{solution-path}"
    role: "primary" | "secondary"
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Project name |
| `path` | string | Yes | Always `"/"` for root |
| `type` | string | Yes | Always `"root"` |
| `last_generated` | ISO 8601 | Yes | Generation timestamp |
| `generator_version` | string | Yes | Generator version |
| `base_commit` | string | Yes | Source commit hash |
| `pr_number` | string | No | Associated PR if applicable |
| `solutions` | array | No | List of solutions in project |

---

## Template

```markdown
---
title: "{project-name}"
path: "/"
type: root
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
pr_number: "{pr-number}"
solutions:
  - name: "API"
    path: "src/API"
    role: "primary"
  - name: "FunctionalTests"
    path: "tests/FunctionalTests"
    role: "secondary"
---

# {project-name}

## Purpose  <!-- REQUIRED -->

{High-level description of what this project does and why it exists}

## Architecture Overview  <!-- REQUIRED -->

{Describe the overall architecture, key patterns, and design decisions.
 Populated from the `architecture` config section if present.}

### Patterns  <!-- OPTIONAL: only if architecture config exists -->

- {Pattern from architecture config}
- {Pattern from architecture config}

### Conventions  <!-- OPTIONAL: only if conventions config exists -->

{Populated from the `conventions` config section.}

- {Convention from conventions config}
- {Convention from conventions config}

## Solution Structure  <!-- REQUIRED -->

### API (Primary)

{Brief description of the API solution's role and responsibilities}

**Key Areas:**
- `Controllers/` - {purpose}
- `Services/` - {purpose}
- `Models/` - {purpose}

### Functional Tests (Secondary)

{Brief description of the test solution's role}

## Service Registration  <!-- CONDITIONAL: only if di_documentation.include_registration_summary is true -->

{Summary of dependency injection registrations extracted from startup files}

| Service | Implementation | Lifetime |
|---------|----------------|----------|
| `IUserService` | `UserService` | Scoped |
| `IAuthClient` | `AuthClient` | Singleton |
| `IEmailService` | `EmailService` | Transient |

## Dependencies  <!-- OPTIONAL: only if external packages used -->

### Internal

{Cross-solution dependencies}

### External

| Package | Version | Purpose |
|---------|---------|---------|
| `{PackageName}` | `{version}` | {why needed} |

## Getting Started  <!-- OPTIONAL: omit if no special setup needed -->

{Brief orientation for new developers}

## Contents  <!-- REQUIRED -->

### Folders

| Folder | Purpose |
|--------|---------|
| `src/` | {description} |
| `tests/` | {description} |

### Key Files

| File | Purpose |
|------|---------|
| `{file}` | {description} |

## Related Documentation  <!-- REQUIRED -->

- [Glossary](./{project-name}.glossary.md)
- [API Solution](./src/API/API.docs.md)
- [Functional Tests](./tests/FunctionalTests/FunctionalTests.docs.md)
```

---

## Section Details

### Purpose (REQUIRED)

High-level description answering:
- What does this project do?
- Why does it exist?
- Who is the target user/consumer?

**Length:** 2-4 sentences. Front-load the most important information.

### Architecture Overview (REQUIRED)

Describe the system's architecture. If `architecture` config is provided, incorporate those patterns.

**Include:**
- Overall architectural style (monolith, microservices, etc.)
- Key design patterns in use
- Layer organization

### Patterns (OPTIONAL)

Only include if `architecture` config section exists. List patterns verbatim from config.

### Conventions (OPTIONAL)

Only include if `conventions` config section exists. List conventions verbatim from config.

### Solution Structure (REQUIRED)

Document each solution (.sln) in the project:
- Name and role (primary/secondary)
- Brief description
- Key areas within the solution

**Primary vs Secondary:**
- Primary: Main application code
- Secondary: Tests, tools, samples

### Service Registration (CONDITIONAL)

Include only when `di_documentation.include_registration_summary: true`.

**Extraction sources** (configured in `di_documentation.scan_startup_files`):
- `Program.cs`
- `Startup.cs`
- `**/ServiceCollectionExtensions.cs`

**Table columns:**
- **Service**: Interface or abstract type
- **Implementation**: Concrete implementation
- **Lifetime**: `Singleton`, `Scoped`, or `Transient`

**Example extraction:**
```csharp
// From Program.cs
services.AddScoped<IUserService, UserService>();
services.AddSingleton<IAuthClient, AuthClient>();
services.AddTransient<IEmailService, EmailService>();
```

Generates:
| Service | Implementation | Lifetime |
|---------|----------------|----------|
| `IUserService` | `UserService` | Scoped |
| `IAuthClient` | `AuthClient` | Singleton |
| `IEmailService` | `EmailService` | Transient |

### Dependencies (OPTIONAL)

Include only if the project has notable dependencies.

**Internal:** Cross-project references within the solution
**External:** NuGet packages with version and purpose

### Getting Started (OPTIONAL)

Brief orientation for developers new to the codebase. Omit if project is straightforward.

### Contents (REQUIRED)

List top-level folders and key files at project root.

### Related Documentation (REQUIRED)

Links to:
- Glossary (if exists)
- Primary solution documentation
- Other important entry points

---

## Complete Example

```markdown
---
title: "MyProject"
path: "/"
type: root
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
base_commit: "abc123def"
solutions:
  - name: "API"
    path: "src/API"
    role: "primary"
  - name: "FunctionalTests"
    path: "tests/FunctionalTests"
    role: "secondary"
---

# MyProject

## Purpose

MyProject is a multi-tenant user management API that provides authentication, authorization, and user lifecycle management for enterprise applications. It serves as the identity backbone for the company's product suite.

## Architecture Overview

The system follows a clean architecture pattern with clear separation between HTTP concerns (Controllers), business logic (Services), and data access (Repositories). All cross-cutting concerns are handled via middleware.

### Patterns

- CQRS pattern used for command/query separation in Services layer
- Repository pattern with Unit of Work for data access
- All services inherit from BaseService for common functionality

### Conventions

- Controllers handle HTTP concerns only; business logic lives in Services
- DTOs suffixed with 'Dto', domain models have no suffix
- Async methods suffixed with 'Async'

## Solution Structure

### API (Primary)

The main REST API providing all user management endpoints. Handles authentication, user CRUD, and tenant management.

**Key Areas:**
- `Controllers/` - HTTP endpoint handlers
- `Services/` - Business logic and domain operations
- `Models/` - DTOs and domain entities

### Functional Tests (Secondary)

Integration and end-to-end tests that verify API behavior against a test database.

## Service Registration

| Service | Implementation | Lifetime |
|---------|----------------|----------|
| `IUserService` | `UserService` | Scoped |
| `IAuthClient` | `AuthClient` | Singleton |
| `ITenantService` | `TenantService` | Scoped |
| `IEmailService` | `EmailService` | Transient |

## Dependencies

### External

| Package | Version | Purpose |
|---------|---------|---------|
| `Microsoft.AspNetCore.Authentication.JwtBearer` | `8.0.0` | JWT token validation |
| `Serilog.AspNetCore` | `7.0.0` | Structured logging |
| `FluentValidation` | `11.8.0` | Request validation |

## Contents

### Folders

| Folder | Purpose |
|--------|---------|
| `src/` | Application source code |
| `tests/` | Test projects |
| `docs/` | Additional documentation |

### Key Files

| File | Purpose |
|------|---------|
| `MyProject.sln` | Solution file |
| `README.md` | Project readme |
| `documentation-config.yaml` | Documentation generator config |

## Related Documentation

- [Glossary](./MyProject.glossary.md)
- [API Solution](./src/API/API.docs.md)
- [Functional Tests](./tests/FunctionalTests/FunctionalTests.docs.md)
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| DI documentation config | `CONFIG-REFERENCE.md` |
| Glossary template | `TEMPLATES/glossary.md` |
| Generation flow | `ORCHESTRATOR.md` |
