# Template: Test File Document

> **Version:** 2.0.0  
> **Output:** `generated-documentation/{path}/{filename}.docs.md`  
> **Purpose:** Document test files with simplified, test-appropriate structure.

---

## Overview

Test files have different documentation needs than production code:
- Focus on what is being tested, not implementation details
- Summarize test coverage rather than documenting each assertion
- Group tests by scenario or feature

---

## Test Project Detection

Identify test projects by any of:
- Project file contains `<IsTestProject>true</IsTestProject>`
- References test frameworks: `xunit`, `nunit`, `mstest`, `Microsoft.NET.Test.Sdk`
- Folder named `Tests`, `Test`, `*.Tests`, `*.Test`, `*Tests`, `*Test`
- File naming: `*Tests.cs`, `*Test.cs`, `*Spec.cs`

---

## Frontmatter Schema

```yaml
---
title: "{filename}"
path: "{relative-path-from-root}"
type: test
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
test_framework: "xunit" | "nunit" | "mstest"
tests_target: "{class-or-feature-being-tested}"
test_count: {count}
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Test class name |
| `type` | string | Yes | Always `"test"` |
| `test_framework` | string | Yes | Testing framework used |
| `tests_target` | string | Yes | What this test class tests |
| `test_count` | integer | Yes | Number of test methods |

---

## Template

```markdown
---
title: "{TestClassName}"
path: "{relative-path-from-root}"
type: test
last_generated: "{ISO-8601-timestamp}"
generator_version: "{version}"
base_commit: "{commit-hash}"
parent: "{parent-folder-doc-path}"
test_framework: "xunit"
tests_target: "UserService"
test_count: 12
---

# {TestClassName}

## Purpose  <!-- REQUIRED -->

{What this test class validates}

## Tests Target  <!-- REQUIRED -->

Tests: [{TargetClass}]({path-to-target-doc})

## Test Coverage  <!-- REQUIRED -->

| Test Method | Scenario | Category |
|-------------|----------|----------|
| `GetUser_ValidId_ReturnsUser` | Happy path retrieval | Unit |
| `GetUser_InvalidId_ReturnsNull` | Missing user handling | Unit |
| `GetUser_NegativeId_ThrowsException` | Input validation | Unit |
| `CreateUser_ValidRequest_CreatesUser` | Happy path creation | Unit |
| `CreateUser_DuplicateEmail_ThrowsException` | Duplicate handling | Unit |

## Test Fixtures  <!-- CONDITIONAL: only if fixtures/setup exists -->

| Fixture | Purpose |
|---------|---------|
| `DatabaseFixture` | In-memory database setup |
| `AuthFixture` | Mock authentication context |

## Test Data  <!-- OPTIONAL: if notable test data setup -->

{Description of test data builders, fixtures, or seed data}

## Related Documentation  <!-- REQUIRED -->

- [Parent: {folder}]({folder-path})
- [Tests: {TargetClass}]({target-path})
```

---

## Section Details

### Purpose (REQUIRED)

Brief description of what this test class validates. Focus on the feature or behavior, not implementation.

**Good:** "Validates UserService business logic including user retrieval, creation, and validation rules."

**Bad:** "Contains test methods for UserService."

### Tests Target (REQUIRED)

Link to the production code being tested. Helps readers navigate between tests and implementation.

### Test Coverage (REQUIRED)

Table summarizing all test methods.

| Column | Description |
|--------|-------------|
| Test Method | Method name (use naming convention format) |
| Scenario | What scenario this test covers |
| Category | `Unit`, `Integration`, `E2E`, `Performance` |

**Test naming conventions recognized:**
- `MethodName_Scenario_ExpectedResult` (recommended)
- `Should_ExpectedBehavior_When_Condition`
- `GivenX_WhenY_ThenZ`

### Test Fixtures (CONDITIONAL)

Include when the test class uses fixtures, base classes, or shared setup.

| Column | Description |
|--------|-------------|
| Fixture | Fixture class name |
| Purpose | What the fixture provides |

### Test Data (OPTIONAL)

Include if the test class has notable test data setup:
- Builder patterns
- Seed data
- Mock factories

---

## Configuration

Control test documentation in `documentation-config.yaml`:

```yaml
test_documentation:
  enabled: true                    # Generate test docs (default: true)
  simplified_template: true        # Use this template (default: true)
  include_test_methods: true       # Include Test Coverage table (default: true)
  include_assertions: false        # Document assertions (default: false, too verbose)
```

When `simplified_template: false`, test files use the standard file template instead.

---

## Complete Example

```markdown
---
title: "UserServiceTests"
path: "tests/API.Tests/Services/UserServiceTests.cs"
type: test
last_generated: "2024-01-15T10:30:00Z"
generator_version: "2.0.0"
base_commit: "abc123def"
parent: "./Services.docs.md"
test_framework: "xunit"
tests_target: "UserService"
test_count: 12
---

# UserServiceTests

## Purpose

Validates UserService business logic including user retrieval, creation, updates, and deletion. Tests cover both happy paths and error handling scenarios.

## Tests Target

Tests: [UserService](../../../src/API/Services/UserService.docs.md)

## Test Coverage

| Test Method | Scenario | Category |
|-------------|----------|----------|
| `GetUserAsync_ValidId_ReturnsUser` | Happy path retrieval | Unit |
| `GetUserAsync_InvalidId_ReturnsNull` | User not found | Unit |
| `GetUserAsync_NegativeId_ThrowsArgumentException` | Input validation | Unit |
| `CreateUserAsync_ValidRequest_CreatesAndReturnsUser` | Happy path creation | Unit |
| `CreateUserAsync_DuplicateEmail_ThrowsDuplicateException` | Duplicate email | Unit |
| `CreateUserAsync_InvalidEmail_ThrowsValidationException` | Email validation | Unit |
| `UpdateUserAsync_ValidRequest_UpdatesUser` | Happy path update | Unit |
| `UpdateUserAsync_NonexistentUser_ThrowsNotFoundException` | User not found | Unit |
| `DeleteUserAsync_ValidId_SoftDeletesUser` | Soft delete | Unit |
| `DeleteUserAsync_AlreadyDeleted_ReturnsFalse` | Idempotent delete | Unit |
| `ListUsersAsync_WithFilter_ReturnsFilteredResults` | Filtering | Integration |
| `ListUsersAsync_WithPaging_ReturnsPagedResults` | Pagination | Integration |

## Test Fixtures

| Fixture | Purpose |
|---------|---------|
| `DatabaseFixture` | In-memory SQLite database with seeded data |
| `ServiceFixture` | Pre-configured UserService with mocked dependencies |

## Test Data

Uses `UserBuilder` for test data construction:
```csharp
var user = new UserBuilder()
    .WithEmail("test@example.com")
    .WithName("Test User")
    .Build();
```

## Related Documentation

- [Parent: Services Tests](./Services.docs.md)
- [Tests: UserService](../../../src/API/Services/UserService.docs.md)
- [Fixture: DatabaseFixture](../Fixtures/DatabaseFixture.docs.md)
```

---

## Test Folder Documentation

Test folders use the standard folder template but with test-specific content:

```markdown
---
title: "Services"
path: "tests/API.Tests/Services/"
type: folder
---

# Services Tests

## Purpose

Unit and integration tests for all service classes in the API project.

## Components & Exports

| Component | Type | Tests | Description |
|-----------|------|-------|-------------|
| `UserServiceTests` | test | UserService | User management tests |
| `AuthClientTests` | test | AuthClient | Authentication tests |
| `TenantServiceTests` | test | TenantService | Multi-tenancy tests |

## Test Summary

| Test Class | Test Count | Categories |
|------------|------------|------------|
| `UserServiceTests` | 12 | Unit, Integration |
| `AuthClientTests` | 8 | Unit |
| `TenantServiceTests` | 15 | Unit, Integration |

## Related Documentation

- [Parent: API.Tests](../API.Tests.docs.md)
- [Production: Services](../../../src/API/Services/Services.docs.md)
```

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Configuration | `CONFIG-REFERENCE.md` |
| File template | `TEMPLATES/file.md` |
| Folder template | `TEMPLATES/folder.md` |
