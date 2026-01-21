# Example: Large Folder Batched Processing

> **Version:** 2.0.0  
> **Purpose:** Demonstrates how folders with many files are processed in batches.

---

## Scenario

A Services folder contains 50 files, exceeding what can be processed in a single context window.

---

## Source Structure

```
src/API/Services/
├── IUserService.cs
├── IAuthService.cs
├── IOrderService.cs
├── IProductService.cs
├── IInventoryService.cs
├── INotificationService.cs
├── IReportService.cs
├── ICacheService.cs
├── UserService.cs
├── AuthService.cs
├── OrderService.cs
├── ProductService.cs
├── InventoryService.cs
├── NotificationService.cs
├── ReportService.cs
├── CacheService.cs
├── ValidationHelper.cs
├── MappingExtensions.cs
├── ServiceBase.cs
├── ... (31 more files)
└── appsettings.Services.json
```

**Total:** 50 files (47 .cs files, 3 config files)

---

## Batching Detection

```
Estimated context needed:
- 47 .cs files × ~200 lines average = ~9,400 lines
- Available context: ~8,000 lines (after system prompt, templates, etc.)
- Threshold: 80% = 6,400 lines

9,400 > 6,400 → Trigger batched processing
```

---

## Batch Organization

### Priority Sorting

Files sorted by documentation priority:

| Priority | Category | Files | Rationale |
|----------|----------|-------|-----------|
| 1 | Interfaces | 8 | Define contracts; needed for implementation docs |
| 2 | Implementations | 8 | Core API surface |
| 3 | Base classes | 1 | Foundation for other classes |
| 4 | Helpers/Extensions | 15 | Supporting utilities |
| 5 | Remaining classes | 15 | Other code |
| 6 | Config files | 3 | Non-code documentation |

### Batch Assignment

```
Batch 1 (Interfaces) - 8 files, ~15% context
  IUserService.cs
  IAuthService.cs
  IOrderService.cs
  IProductService.cs
  IInventoryService.cs
  INotificationService.cs
  IReportService.cs
  ICacheService.cs

Batch 2 (Implementations) - 8 files, ~40% context
  UserService.cs
  AuthService.cs
  OrderService.cs
  ProductService.cs
  InventoryService.cs
  NotificationService.cs
  ReportService.cs
  CacheService.cs

Batch 3 (Base + Helpers) - 16 files, ~30% context
  ServiceBase.cs
  ValidationHelper.cs
  MappingExtensions.cs
  ... (13 more helpers)

Batch 4 (Remaining) - 18 files
  ... remaining classes and configs
```

---

## Processing Flow

### Batch 1: Interfaces

**Input:**
```yaml
batch: 1
files:
  - IUserService.cs
  - IAuthService.cs
  - ... (6 more)
prior_batch_exports: null  # First batch
```

**Output:**
```yaml
generated_files:
  - IUserService.docs.md
  - IAuthService.docs.md
  - ... (6 more)
  
exports:
  - name: "IUserService"
    type: "interface"
    doc_path: "IUserService.docs.md"
    methods: ["GetByIdAsync", "CreateAsync", "UpdateAsync", "DeleteAsync"]
  - name: "IAuthService"
    type: "interface"
    doc_path: "IAuthService.docs.md"
    methods: ["AuthenticateAsync", "ValidateTokenAsync"]
  # ... more exports
```

### Batch 2: Implementations

**Input:**
```yaml
batch: 2
files:
  - UserService.cs
  - AuthService.cs
  - ... (6 more)
  
prior_batch_exports:
  - name: "IUserService"
    type: "interface"
    doc_path: "IUserService.docs.md"
    methods: ["GetByIdAsync", "CreateAsync", "UpdateAsync", "DeleteAsync"]
  - name: "IAuthService"
    type: "interface"
    doc_path: "IAuthService.docs.md"
    methods: ["AuthenticateAsync", "ValidateTokenAsync"]
  # ... all Batch 1 exports
```

**Processing Notes:**
- `UserService.docs.md` can correctly link to `IUserService.docs.md`
- Interface implementations table populated accurately
- No need to re-read Batch 1 files

**Output:**
```yaml
generated_files:
  - UserService.docs.md
  - AuthService.docs.md
  - ... (6 more)

exports:
  - name: "UserService"
    type: "class"
    implements: ["IUserService"]
    doc_path: "UserService.docs.md"
  # ... more exports
```

### Batch 3: Base + Helpers

**Input:**
```yaml
batch: 3
files:
  - ServiceBase.cs
  - ValidationHelper.cs
  - MappingExtensions.cs
  - ... (13 more)

prior_batch_exports:
  # All exports from Batches 1-2
```

**Processing Notes:**
- `ServiceBase.docs.md` can be linked from implementation docs
- Helper classes can reference service interfaces
- Extension methods can document which types they extend

### Batch 4: Remaining

**Input:**
```yaml
batch: 4
files:
  - ... (15 remaining .cs files)
  - appsettings.Services.json
  - ... (2 more config files)

prior_batch_exports:
  # All exports from Batches 1-3
```

---

## Cross-Batch Reference Manifest

The manifest accumulates across batches:

```yaml
# After all batches complete
prior_batch_exports:
  # Interfaces (Batch 1)
  - name: "IUserService"
    type: "interface"
    doc_path: "IUserService.docs.md"
    methods: ["GetByIdAsync", "CreateAsync", "UpdateAsync", "DeleteAsync"]
    
  - name: "IAuthService"
    type: "interface"
    doc_path: "IAuthService.docs.md"
    methods: ["AuthenticateAsync", "ValidateTokenAsync"]
    
  # ... (6 more interfaces)
  
  # Implementations (Batch 2)
  - name: "UserService"
    type: "class"
    implements: ["IUserService"]
    inherits: "ServiceBase"
    doc_path: "UserService.docs.md"
    
  - name: "AuthService"
    type: "class"
    implements: ["IAuthService"]
    inherits: "ServiceBase"
    doc_path: "AuthService.docs.md"
    
  # ... (6 more implementations)
  
  # Base + Helpers (Batch 3)
  - name: "ServiceBase"
    type: "class"
    doc_path: "ServiceBase.docs.md"
    
  - name: "ValidationHelper"
    type: "class"
    static: true
    doc_path: "ValidationHelper.docs.md"
    
  # ... more exports
```

---

## Folder Document Generation

After ALL batches complete, generate `Services.docs.md`:

```markdown
---
title: "Services"
path: "src/API/Services/"
type: folder
processing:
  batched: true
  batch_count: 4
  total_files: 50
namespace: "MyProject.API.Services"
---

# Services

## Purpose

Business logic layer containing all domain services, helpers, and utilities.
Processed in 4 batches due to size.

## Components & Exports

| Component | Type | Exported | Description |
|-----------|------|----------|-------------|
| `IUserService` | interface | yes | User management contract |
| `IAuthService` | interface | yes | Authentication contract |
| `IOrderService` | interface | yes | Order processing contract |
| `IProductService` | interface | yes | Product catalog contract |
| `IInventoryService` | interface | yes | Inventory management contract |
| `INotificationService` | interface | yes | Notification delivery contract |
| `IReportService` | interface | yes | Report generation contract |
| `ICacheService` | interface | yes | Caching operations contract |
| `UserService` | class | yes | User management implementation |
| `AuthService` | class | yes | Authentication implementation |
| `OrderService` | class | yes | Order processing implementation |
| ... | ... | ... | ... |
| `ServiceBase` | class | yes | Base class for all services |
| `ValidationHelper` | class | yes | Validation utilities |
| `MappingExtensions` | class | yes | Object mapping extensions |

## Contents

### Files

| File | Key Types | Batch |
|------|-----------|-------|
| `IUserService.cs` | `IUserService` | 1 |
| `IAuthService.cs` | `IAuthService` | 1 |
| `UserService.cs` | `UserService` | 2 |
| `AuthService.cs` | `AuthService` | 2 |
| `ServiceBase.cs` | `ServiceBase` | 3 |
| `ValidationHelper.cs` | `ValidationHelper` | 3 |
| ... | ... | ... |
| `appsettings.Services.json` | - | 4 |

## Dependencies

### External

| Package | Purpose |
|---------|---------|
| `FluentValidation` | Request validation |
| `AutoMapper` | Object mapping |
| `Microsoft.Extensions.Caching.Memory` | In-memory caching |

## Related Documentation

- [Parent: API](../API.docs.md)
```

---

## Subagent Return Contract

```yaml
status: "success"
processing:
  batched: true
  batch_count: 4
  total_files: 50
  
generated_files:
  - path: "generated-documentation/src/API/Services/Services.docs.md"
    type: "folder"
  - path: "generated-documentation/src/API/Services/IUserService.docs.md"
    type: "file"
  - path: "generated-documentation/src/API/Services/UserService.docs.md"
    type: "file"
  # ... (47 more file docs)
  
warnings:
  - type: "batched_processing"
    folder: "src/API/Services/"
    message: "Processed in 4 batches (50 files) due to context limits"

child_folders: []
```

---

## INDEX.md Entry

```markdown
## Validation Warnings

| Type | Location | Issue |
|------|----------|-------|
| Batched Processing | src/API/Services/ | Processed in 4 batches (50 files) |
```

**Note:** Batched processing warnings are informational, not errors. They indicate the folder was large but processed successfully.

---

## Key Behaviors

1. **Priority ordering** — Interfaces processed first to enable accurate implementation docs
2. **Manifest accumulation** — Each batch receives all prior exports
3. **No re-reading** — Batch N doesn't re-read Batch N-1 files; uses manifest
4. **Folder doc last** — Generated only after all batches complete
5. **Complete output** — All 50 files get documentation despite batching
6. **Transparent metadata** — Frontmatter records batched processing

---

## Performance Characteristics

| Metric | Single Pass | Batched (4) |
|--------|-------------|-------------|
| Context per pass | 9,400 lines | ~2,500 lines |
| Total context used | N/A (exceeds) | ~10,000 lines |
| Subagent calls | 1 (would fail) | 4 |
| Quality | N/A | Full |

Batching trades additional subagent calls for reliable processing of large folders.

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Orchestration | `ORCHESTRATOR.md` |
| Subagent contract | `ORCHESTRATOR.md` → Subagent Output Contract |
| Validation | `VALIDATION.md` |
