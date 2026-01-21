# Template: Non-Code File Document

> **Version:** 2.0.0  
> **Output:** `generated-documentation/{path}/{filename}.docs.md`  
> **Purpose:** Document configuration files, resource files, and project files.

---

## Overview

Non-code files include:
- Configuration files (`.json`, `.yaml`, `.xml`, `.config`)
- Resource files (`.resx`, embedded resources)
- Project files (`.csproj`, `.sln`)
- Data files (`.sql`, seed data)

---

## Frontmatter Schema

```yaml
---
title: "{filename}"
path: "{relative-path-from-root}"
type: config | data | resource | project
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"

# For project files
target_frameworks: ["net8.0"]
package_count: {count}
project_references: ["{project-names}"]
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Filename |
| `path` | string | Yes | Relative path |
| `type` | string | Yes | `config`, `data`, `resource`, or `project` |
| `target_frameworks` | array | No | For .csproj files |
| `package_count` | integer | No | For .csproj files |
| `project_references` | array | No | For .csproj files |

---

## Template: Configuration File

```markdown
---
title: "{filename}"
path: "{relative-path-from-root}"
type: config
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
---

# {filename}

## Purpose  <!-- REQUIRED -->

{What this file configures or contains}

## Key Settings  <!-- CONDITIONAL: only for config files with notable settings -->

| Setting | Value | Purpose |
|---------|-------|---------|
| `{key}` | `{value}` | {description} |
| `{section.key}` | `{value}` | {description} |

## Environment Overrides  <!-- OPTIONAL: if environment-specific variants exist -->

| Environment | File | Notes |
|-------------|------|-------|
| Development | `appsettings.Development.json` | Debug logging enabled |
| Production | `appsettings.Production.json` | Stricter security settings |

## Related Documentation  <!-- REQUIRED -->

- [Parent: {folder}]({folder-path})
```

---

## Template: Project File (`.csproj`)

```markdown
---
title: "{ProjectName}.csproj"
path: "{relative-path-from-root}"
type: project
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
target_frameworks: ["net8.0"]
package_count: 12
project_references: ["MyProject.Core", "MyProject.Data"]
---

# {ProjectName}.csproj

## Purpose  <!-- REQUIRED -->

{What this project builds and its role in the solution}

## Build Configuration  <!-- REQUIRED -->

| Property | Value |
|----------|-------|
| Target Framework | `net8.0` |
| Output Type | `Library` / `Exe` |
| Nullable | `enable` |
| ImplicitUsings | `enable` |

## Package References  <!-- CONDITIONAL: only if packages exist -->

| Package | Version | Purpose |
|---------|---------|---------|
| `Microsoft.AspNetCore.Authentication.JwtBearer` | `8.0.0` | JWT authentication |
| `Serilog.AspNetCore` | `7.0.0` | Structured logging |
| `FluentValidation.AspNetCore` | `11.3.0` | Request validation |

## Project References  <!-- CONDITIONAL: only if project references exist -->

| Project | Purpose |
|---------|---------|
| `MyProject.Core` | Domain models and interfaces |
| `MyProject.Data` | Data access layer |

## Key MSBuild Properties  <!-- OPTIONAL: only if notable custom properties -->

| Property | Value | Purpose |
|----------|-------|---------|
| `GenerateDocumentationFile` | `true` | Produces XML docs |
| `TreatWarningsAsErrors` | `true` | Strict compilation |

## Related Documentation  <!-- REQUIRED -->

- [Parent: {folder}]({folder-path})
- [Referenced: MyProject.Core](../Core/Core.docs.md)
```

---

## Template: Solution File (`.sln`)

```markdown
---
title: "{SolutionName}.sln"
path: "{relative-path-from-root}"
type: project
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
project_count: {count}
---

# {SolutionName}.sln

## Purpose  <!-- REQUIRED -->

{What this solution contains and how projects relate}

## Projects  <!-- REQUIRED -->

| Project | Path | Type |
|---------|------|------|
| `MyProject.API` | `src/API/MyProject.API.csproj` | Web API |
| `MyProject.Core` | `src/Core/MyProject.Core.csproj` | Class Library |
| `MyProject.Tests` | `tests/MyProject.Tests.csproj` | Test Project |

## Solution Folders  <!-- OPTIONAL: if solution folders exist -->

| Folder | Contents |
|--------|----------|
| `src` | Production code projects |
| `tests` | Test projects |

## Related Documentation  <!-- REQUIRED -->

- [API Project](./src/API/API.docs.md)
- [Core Project](./src/Core/Core.docs.md)
```

---

## Template: Resource File (`.resx`)

```markdown
---
title: "{filename}.resx"
path: "{relative-path-from-root}"
type: resource
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
resource_count: {count}
culture: "{culture-code}"  # e.g., "en-US", or null for default
---

# {filename}.resx

## Purpose  <!-- REQUIRED -->

{What resources this file contains}

## Resource Summary  <!-- REQUIRED -->

| Category | Count | Examples |
|----------|-------|----------|
| Strings | 45 | Error messages, labels |
| Images | 3 | Icons, logos |

## Key Resources  <!-- OPTIONAL: highlight important resources -->

| Name | Type | Description |
|------|------|-------------|
| `Error_InvalidEmail` | String | Email validation error message |
| `Error_UserNotFound` | String | User lookup failure message |

## Localization  <!-- CONDITIONAL: if localized variants exist -->

| Culture | File | Status |
|---------|------|--------|
| Default | `Resources.resx` | Complete |
| Spanish | `Resources.es.resx` | Complete |
| French | `Resources.fr.resx` | Partial (32/45) |

## Related Documentation  <!-- REQUIRED -->

- [Parent: {folder}]({folder-path})
```

---

## Example: appsettings.json

```markdown
---
title: "appsettings.json"
path: "src/API/appsettings.json"
type: config
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
base_commit: "abc123def"
parent: "./API.docs.md"
---

# appsettings.json

## Purpose

Primary configuration file for the API application. Contains connection strings, logging configuration, and feature flags.

## Key Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `ConnectionStrings.DefaultConnection` | `Server=...` | Primary database connection |
| `Logging.LogLevel.Default` | `Information` | Default log verbosity |
| `Jwt.Issuer` | `https://api.example.com` | Token issuer for validation |
| `Jwt.Audience` | `https://app.example.com` | Expected token audience |
| `Features.EnableCaching` | `true` | Response caching toggle |

## Environment Overrides

| Environment | File | Notes |
|-------------|------|-------|
| Development | `appsettings.Development.json` | Local database, debug logging |
| Production | `appsettings.Production.json` | Production DB, warning-level logging |

## Related Documentation

- [Parent: API](./API.docs.md)
```

---

## Example: Project File

```markdown
---
title: "MyProject.API.csproj"
path: "src/API/MyProject.API.csproj"
type: project
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
base_commit: "abc123def"
parent: "./API.docs.md"
target_frameworks: ["net8.0"]
package_count: 8
project_references: ["MyProject.Core"]
---

# MyProject.API.csproj

## Purpose

ASP.NET Core Web API project serving as the main application entry point. Handles HTTP requests, authentication, and routes to business logic services.

## Build Configuration

| Property | Value |
|----------|-------|
| Target Framework | `net8.0` |
| Output Type | `Exe` |
| Nullable | `enable` |
| ImplicitUsings | `enable` |

## Package References

| Package | Version | Purpose |
|---------|---------|---------|
| `Microsoft.AspNetCore.Authentication.JwtBearer` | `8.0.0` | JWT token validation |
| `Serilog.AspNetCore` | `7.0.0` | Structured logging |
| `FluentValidation.AspNetCore` | `11.3.0` | Request validation |
| `Swashbuckle.AspNetCore` | `6.5.0` | OpenAPI documentation |
| `AutoMapper.Extensions.Microsoft.DependencyInjection` | `12.0.0` | Object mapping |

## Project References

| Project | Purpose |
|---------|---------|
| `MyProject.Core` | Domain models, interfaces, DTOs |

## Key MSBuild Properties

| Property | Value | Purpose |
|----------|-------|---------|
| `GenerateDocumentationFile` | `true` | XML docs for Swagger |
| `NoWarn` | `1591` | Suppress missing XML doc warnings |

## Related Documentation

- [Parent: API](./API.docs.md)
- [Referenced: Core](../Core/Core.docs.md)
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Folder documentation | `TEMPLATES/folder.md` |
| Generation flow | `ORCHESTRATOR.md` |
