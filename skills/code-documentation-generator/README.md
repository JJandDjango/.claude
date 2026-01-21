# Code Documentation Generator

> **Version:** 2.0.0  
> **Purpose:** Generate progressive disclosure documentation for C# codebases, optimized for LLM consumption.

---

## Overview

This specification defines a documentation generator that creates structured API documentation mirroring your codebase's folder structure. The output focuses on public interfaces and signatures, enabling LLMs to efficiently understand and work with your code.

### Key Features

- **Progressive disclosure** — Detail increases with folder depth
- **Focus patterns** — Document specific paths, ignore noise
- **Interface detection** — Automatic implementation discovery
- **Partial class consolidation** — Unified docs for split classes
- **Glossary linking** — Automatic domain term linking
- **Full C# support** — Generics, attributes, records, async, and more
- **Validation** — Link checking, section verification, stale reference detection

---

## Quick Start

### Minimal Configuration

Create `documentation-config.yaml`:

```yaml
project_name: "MyProject"
```

Run the generator with:
```
FOLDER_PATH="."
CONFIG_PATH="./documentation-config.yaml"
```

### Focused Documentation

To document only specific paths:

```yaml
project_name: "MyProject"

focus:
  - "src/API/Services/**"
  - "src/API/Controllers/**"

ignore:
  - "**/*.generated.cs"
  - "**/obj/**"
  - "**/bin/**"
```

### With Domain Glossary

```yaml
project_name: "MyProject"

glossary:
  Tenant: "An organization or customer account in the multi-tenant system"
  Claim: "A security assertion about a user's identity or permissions"
```

---

## Specification Structure

This specification is modular. Load only what you need for each task.

```
code-documentation-generator/
├── README.md                 # This file — overview and quick start
├── ORCHESTRATOR.md           # Entry point, generation flow, subagent instructions
├── CONFIG-REFERENCE.md       # Complete configuration schema
├── VALIDATION.md             # Validation rules and warning types
├── TEMPLATES/
│   ├── index.md              # INDEX.md template
│   ├── root.md               # {project}.docs.md template
│   ├── folder.md             # Folder document template
│   ├── file.md               # File/class document template
│   ├── glossary.md           # Glossary document template
│   ├── non-code.md           # Config/resource file template
│   └── test.md               # Test file template
├── RULES/
│   ├── signatures.md         # What to extract, access modifiers
│   ├── csharp-features.md    # Generics, attributes, XML docs, async, etc.
│   ├── interface-handling.md # Detection, placement, multiple implementations
│   ├── partial-classes.md    # Consolidation rules
│   └── glossary-linking.md   # Term matching and linking
└── EXAMPLES/
    ├── focused-generation.md # Walkthrough with focus patterns
    └── large-folder.md       # Batched processing example
```

### Module Loading by Task

| Task | Load These Modules |
|------|-------------------|
| **Understanding the system** | `README.md`, `ORCHESTRATOR.md` |
| **Configuring generation** | `CONFIG-REFERENCE.md` |
| **Processing a folder** | `TEMPLATES/folder.md`, `TEMPLATES/file.md`, `RULES/*` |
| **Understanding validation** | `VALIDATION.md` |
| **Seeing examples** | `EXAMPLES/*` |

### Subagent Module Set

When spawning a subagent for folder processing, provide:

```
TEMPLATES/folder.md
TEMPLATES/file.md
TEMPLATES/non-code.md
TEMPLATES/test.md          # If test project
RULES/signatures.md
RULES/csharp-features.md
RULES/interface-handling.md
RULES/partial-classes.md
RULES/glossary-linking.md
```

---

## Output Structure

Generated documentation mirrors your source structure:

```
generated-documentation/
├── INDEX.md                    # Navigation and validation summary
├── {project}.docs.md           # Project overview
├── {project}.glossary.md       # Domain terms (if configured)
└── src/
    └── API/
        ├── API.docs.md         # Folder documentation
        ├── Controllers/
        │   ├── Controllers.docs.md
        │   └── UserController.docs.md
        └── Services/
            ├── Services.docs.md
            ├── UserService.docs.md
            └── AuthClient.docs.md
```

### File Naming

| Source | Documentation |
|--------|---------------|
| Folder `Services/` | `Services.docs.md` |
| File `UserService.cs` | `UserService.docs.md` |
| Interface `IUserService.cs` | In `UserService.docs.md` (default) |
| Project root | `{project-name}.docs.md` |
| Glossary | `{project-name}.glossary.md` |

---

## Progressive Disclosure

Documentation depth increases with folder depth:

| Level | Focus | Content |
|-------|-------|---------|
| Root | Project overview | Architecture, conventions, solutions |
| Solution | Organization | Project relationships, dependencies |
| Project | Module purpose | Namespaces, key interfaces |
| Deep folders | Signatures | Classes, methods, properties |

---

## Design Decisions

Key architectural choices in this specification:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Focus model** | Allowlist | Large codebases need noise reduction |
| **Focus vs ignore** | Focus wins | Explicit focus = definitely document |
| **Interface docs** | In implementation file | Self-contained docs per class |
| **Multiple implementations** | Duplicate interface | Each doc is standalone |
| **Unimplemented interfaces** | In folder doc | Surfaces orphaned contracts |
| **Processing model** | Sequential subagents | Correctness over performance |
| **Recursion depth** | Unlimited | Complete documentation of focused tree |
| **Parent context** | Immediate only | Prevents context bloat |
| **Large folders** | Batched by priority | Interfaces first for reference integrity |
| **Validation failures** | Warnings only | Always produce output |
| **Warning location** | INDEX.md only | Clean individual docs |
| **Regeneration** | Full always | Simple mental model, no stale fragments |
| **Metadata fields** | Audit only | Generator is authoritative |
| **Signature scope** | Public + protected | Documents inheritance contracts |
| **Partial classes** | Consolidate | One class = one doc |
| **Namespace extraction** | From source | Documents reality |
| **Glossary linking** | First occurrence | Reduces clutter |

---

## Version History

### v2.0.0 (Current)

**Breaking:** Modular specification structure (was single file)

**New features:**
- Generic type documentation with constraints
- Attribute documentation (routing, authorization, validation)
- XML documentation extraction and mapping
- Async pattern documentation
- Inheritance documentation with virtual/override markers
- Dependency injection documentation with lifetimes
- Record and primary constructor support
- Extension method documentation
- Enum value tables
- Static class handling
- Event and indexer documentation
- Test project simplified template
- Project file (.csproj, .sln) documentation

**Improvements:**
- Modular file structure for LLM efficiency
- Enhanced validation with new warning types
- Better cross-referencing between modules

### v1.1.0

- Focus patterns as allowlist
- Interface auto-detection
- Partial class consolidation
- Glossary linking
- Batched processing for large folders

### v1.0.0

- Initial specification
- Basic folder/file documentation
- Progressive disclosure model

---

## Best Practices

### Writing Quality Documentation

1. **Purpose statements** — Answer "what" and "why", not just "what"
2. **Focus on signatures** — Code provides implementation details
3. **Document contracts** — What callers can expect
4. **Link liberally** — Connect related documentation
5. **Use glossary terms** — Link on first occurrence per document

### For LLM Consumption

1. **Consistent structure** — Same sections in same order
2. **Front-load key info** — Purpose and signatures first
3. **Use tables** — Structured data over prose
4. **Include code blocks** — Exact signatures over descriptions
5. **Relative paths** — Enable navigation without absolute paths
6. **Centralized warnings** — All issues in INDEX.md

### Maintenance

1. **Regenerate on PR** — Keep docs current
2. **Review INDEX.md warnings** — Part of code review
3. **Update glossary** — As terminology evolves
4. **Trust the generator** — Metadata auto-updates

---

## Cross-Reference Index

| Topic | Module |
|-------|--------|
| Generation flow | `ORCHESTRATOR.md` |
| Configuration options | `CONFIG-REFERENCE.md` |
| Validation rules | `VALIDATION.md` |
| Index template | `TEMPLATES/index.md` |
| Root template | `TEMPLATES/root.md` |
| Folder template | `TEMPLATES/folder.md` |
| File template | `TEMPLATES/file.md` |
| Glossary template | `TEMPLATES/glossary.md` |
| Non-code template | `TEMPLATES/non-code.md` |
| Test template | `TEMPLATES/test.md` |
| Signature extraction | `RULES/signatures.md` |
| C# features | `RULES/csharp-features.md` |
| Interface handling | `RULES/interface-handling.md` |
| Partial classes | `RULES/partial-classes.md` |
| Glossary linking | `RULES/glossary-linking.md` |
| Focus example | `EXAMPLES/focused-generation.md` |
| Batching example | `EXAMPLES/large-folder.md` |
