---
name: code-documentation-generator-orchestrator
description: Execution flow and subagent coordination for documentation generation.
parent: code-documentation-generator
phase: EXECUTION
---

# Code Documentation Generator — Orchestrator

> **Version:** 2.0.0  
> **Role:** Entry point for documentation generation. Defines orchestration flow, subagent spawning, and module loading.

## Quick Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FOLDER_PATH` | Target folder to document (relative to project root) | `.` (root) |
| `CONFIG_PATH` | Path to `documentation-config.yaml` | `./documentation-config.yaml` |

## Variables

```
#VARIABLES
FOLDER_PATH: string = "."  # Folder to document, relative to project root
CONFIG_PATH: string = "./documentation-config.yaml"  # Configuration file path
```

---

## Module Loading Guide

This specification is modular. Load only the modules required for each phase of generation.

### By Generation Phase

| Phase | Required Modules | Purpose |
|-------|------------------|---------|
| **Initialization** | `ORCHESTRATOR.md`, `CONFIG-REFERENCE.md` | Parse config, build file list |
| **Index Generation** | `TEMPLATES/index.md` | Generate INDEX.md |
| **Root Doc Generation** | `TEMPLATES/root.md`, `RULES/signatures.md` | Generate {project}.docs.md |
| **Glossary Generation** | `TEMPLATES/glossary.md`, `RULES/glossary-linking.md` | Generate {project}.glossary.md |
| **Subagent: Folder** | See Subagent Module Set below | Process folder + files |
| **Validation** | `VALIDATION.md` | Run all validation checks |

### Subagent Module Set

Each folder-processing subagent requires:

```
TEMPLATES/folder.md           # Folder document template
TEMPLATES/file.md             # File document template  
TEMPLATES/non-code.md         # Config/resource template
TEMPLATES/test.md             # Test file template (if test project)
RULES/signatures.md           # What to extract
RULES/csharp-features.md      # Language feature documentation
RULES/interface-handling.md   # Interface detection and placement
RULES/partial-classes.md      # Partial class consolidation
RULES/glossary-linking.md     # Term linking rules
```

**Estimated context:** ~1,500 lines (vs 2,200 for monolithic spec)

---

## Documentation Structure

### Progressive Disclosure Model

Documentation depth increases with folder depth, focusing on public interfaces and signatures throughout:

| Level | Focus | Content Priority |
|-------|-------|------------------|
| Root | Project overview | Purpose, architecture, solution relationships |
| Solution | Solution scope | Project organization, key dependencies |
| Project | Module purpose | Namespace structure, public interfaces |
| Deep folders | Signatures | Class signatures, method signatures, type definitions |

### Output Structure

```
generated-documentation/
├── INDEX.md                        # Navigation index (LLM-optimized)
├── {project-name}.docs.md          # Root-level overview
├── {project-name}.glossary.md      # Domain terminology (if configured)
├── src/
│   ├── src.docs.md                 # src folder overview
│   └── API/
│       ├── API.docs.md             # API solution overview
│       ├── Controllers/
│       │   ├── Controllers.docs.md
│       │   ├── AuthController.docs.md
│       │   └── UserController.docs.md
│       └── Services/
│           ├── Services.docs.md
│           ├── AuthClient.docs.md
│           └── UserService.docs.md
└── tests/
    └── FunctionalTests/
        ├── FunctionalTests.docs.md
        └── ...
```

### File Naming Conventions

| Source Type | Output Name | Example |
|-------------|-------------|---------|
| Folder | `{foldername}.docs.md` | `Services/` → `Services.docs.md` |
| Code file | `{filename}.docs.md` | `UserService.cs` → `UserService.docs.md` |
| Interface | Within implementation file | `IAuthClient.cs` → in `AuthClient.docs.md` |
| Root | `{project-name}.docs.md` | `MyProject.docs.md` |
| Glossary | `{project-name}.glossary.md` | `MyProject.glossary.md` |
| Index | `INDEX.md` | Always at root of generated-documentation/ |

---

## Orchestration Flow

### Complete Execution Sequence

```
1. Read configuration from CONFIG_PATH
2. Run: git ls-files > file_list.txt
3. Run: git rev-parse HEAD > current_commit.txt
4. Apply focus/ignore patterns to file list
5. Auto-detect interface implementations
6. Create generated-documentation/ structure (mirrors focused source paths)
7. Generate INDEX.md (initial, will update after validation)
8. Generate root document: {project-name}.docs.md
9. Generate glossary document: {project-name}.glossary.md (if glossary config exists)
10. Process folders sequentially (depth-first):
    a. Spawn subagent with folder context
    b. Subagent generates folder + file docs (public signatures only)
    c. Subagent returns: status, generated_files, warnings, child_folders
    d. Wait for completion before processing next folder
    e. Queue child_folders for processing
    f. Repeat until no folders remain in queue
11. Run validation:
    a. Check required sections in all generated docs
    b. Validate internal links resolve
    c. Validate code references (files and symbols) exist
12. Update INDEX.md with aggregated validation warnings
13. Update configuration metadata (last_generated, base_commit, generator_version)
14. Report completion summary
```

### Key Behaviors

- Steps 10a-10f repeat until all folders are processed (no depth limit)
- Subagents execute one at a time (sequential, not parallel)
- Validation warnings never block generation
- All metadata updates happen after successful generation

---

## Generation Process Detail

### Step 1: Initialize Output Structure

```bash
# Get project name from config or directory
PROJECT_NAME=$(grep 'project_name:' "$CONFIG_PATH" | cut -d'"' -f2)
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(basename "$(pwd)")
fi

# Create output directory
mkdir -p generated-documentation

# Mirror folder structure (excluding ignored patterns)
git ls-files | while read -r file; do
  dir=$(dirname "$file")
  mkdir -p "generated-documentation/$dir"
done
```

### Step 2: Gather Context

1. **Read configuration file** at `CONFIG_PATH`
   - See `CONFIG-REFERENCE.md` for complete schema
2. **Get committed files** via `git ls-files`
3. **Get current commit hash** via `git rev-parse HEAD`
4. **Auto-detect interface implementations** (if enabled):
   - Scan for interface definitions (`interface I{Name}`)
   - Find implementing classes (`: I{Name}` in class declaration)
   - Merge with manual `interface_mappings` (manual takes precedence)
   - See `RULES/interface-handling.md` for details

### Step 3: Generate Documentation

All generation runs are full regenerations from root. The `base_commit` tracking is informational only.

```
1. Generate INDEX.md
   → Load: TEMPLATES/index.md
   
2. Generate root document: {project-name}.docs.md
   → Load: TEMPLATES/root.md, RULES/signatures.md
   
3. Generate glossary: {project-name}.glossary.md
   → Load: TEMPLATES/glossary.md
   → Skip if no glossary config
   
4. FOR each folder (depth-first from root):
   a. SPAWN subagent for folder documentation
   b. Subagent READS:
      - All files in current folder (via git ls-files filtering)
      - Configuration file (focus, ignore, glossary, architecture, conventions)
      - Parent folder's generated documentation (for context)
      - Detected interface implementations
   c. Subagent GENERATES:
      - {foldername}.docs.md for the folder
      - {filename}.docs.md for each code file (focusing on public signatures)
      - Non-code file documentation as needed
   d. Subagent WRITES to generated-documentation/{path}/
   e. RECURSE into subfolders
   
5. Run validation checks
   → Load: VALIDATION.md
   
6. Update INDEX.md with validation warnings

7. Update configuration with new timestamps
```

### Step 4: Update Metadata

After generation completes, update `documentation-config.yaml`:

```yaml
generator_version: "2.0.0"  # Current generator version
last_generated: "{current-ISO-8601-timestamp}"
base_commit: "{current-commit-hash}"
pr_number: "{pr-number-if-provided}"
```

---

## Subagent Instructions

### Context to Provide

When spawning a subagent for folder documentation, provide:

1. **Folder path** being documented
2. **Configuration** from `documentation-config.yaml`
3. **Parent documentation** content (the parent folder's `.docs.md`)
4. **File list** for the folder (from `git ls-files`)
5. **Depth level** (for calibrating detail level)
6. **Detected implementations** (interface → implementing classes map)
7. **Required modules** (see Subagent Module Set above)

### Parent Context Rules

Subagents receive **immediate parent documentation only** to prevent context bloat in deep hierarchies:

| Subagent Processing | Parent Context Received |
|---------------------|-------------------------|
| `src/` | Root doc (`{project-name}.docs.md`) |
| `src/API/` | `src.docs.md` only |
| `src/API/Services/` | `API.docs.md` only |
| `src/API/Services/Validators/` | `Services.docs.md` only |

**Rationale:**
- Root architecture/conventions are embedded in the root document at generation time
- Immediate parent provides namespace context and awareness of sibling folders
- Each document should be understandable with only its immediate parent as context
- Prevents exponential context growth in deep folder structures

**What is NOT included:**
- Grandparent or ancestor documentation (beyond immediate parent)
- Sibling folder documentation
- Root document (except when processing direct children of root)

### Exception Handling

If a subagent cannot determine folder purpose from immediate parent context alone:

1. Make a reasonable inference based on folder name and file contents
2. Flag uncertainty in the generated documentation:
   ```markdown
   ## Purpose
   
   {Best inference based on available context}
   
   > ℹ️ **Context Note**: Purpose inferred from folder contents; parent context was limited.
   ```
3. Include in return contract for orchestrator awareness:
   ```yaml
   warnings:
     - type: "limited_context"
       folder: "src/API/Services/Validators/"
       message: "Purpose inferred without full ancestor context"
   ```

### Subagent Task Prompt

```
You are documenting the folder: {folder_path}
Depth level: {depth} (0 = root, higher = more detail)

Configuration:
{config_yaml_content}

Parent documentation:
{parent_docs_content}

Files to document:
{file_list}

Detected interface implementations:
{implementations_map}

Instructions:
1. Read each file in the folder
2. For .cs files:
   - Extract PUBLIC signatures only (classes, interfaces, methods, properties)
   - Check interface_mappings in config (manual mappings override auto-detection)
   - If interface, document within implementation file unless mapped separately
   - Generate {filename}.docs.md using the File Document Template
3. Generate {foldername}.docs.md using the Folder Document Template
4. For non-code files (configs, etc.):
   - Generate documentation using Non-Code File Template
5. Write all documentation to generated-documentation/{folder_path}/

Focus: Document PUBLIC SIGNATURES for LLM consumption. Implementation details are available in source code.

Error handling:
- Unparseable code: Include with warning, document available metadata
- Large files: Extract public signatures only, add truncation notice

Required specification modules:
- TEMPLATES/folder.md
- TEMPLATES/file.md
- TEMPLATES/non-code.md
- RULES/signatures.md
- RULES/csharp-features.md
- RULES/interface-handling.md
- RULES/partial-classes.md
- RULES/glossary-linking.md
```

---

## Subagent Output Contract

Each subagent must return a structured response upon completion.

### Return Schema

```yaml
status: "success" | "partial" | "failed"
  # success: All files processed without issues
  # partial: Completed with warnings (parse failures, large files truncated)
  # failed: Could not complete (still produces whatever output was possible)

generated_files:
  - path: "generated-documentation/{folder_path}/{filename}.docs.md"
    type: "folder" | "file" | "config" | "test"
  # List of all documentation files created by this subagent

warnings:
  - type: "{warning_type}"
    file: "{source-file-path}"
    message: "{description of issue}"
  # All warnings encountered during processing

child_folders:
  - path: "{relative-folder-path}"
    file_count: {number}
  # Subfolders requiring their own subagent processing
```

### Warning Types

| Type | Description |
|------|-------------|
| `parse_failure` | Could not parse source file |
| `truncated` | Large file, only public signatures extracted |
| `missing_interface` | Interface referenced but not found |
| `batched_processing` | Folder processed in multiple batches due to size |
| `limited_context` | Purpose inferred without full ancestor context |
| `partial_incomplete` | Partial class has files outside focus patterns |
| `namespace_mismatch` | Namespace doesn't match folder path |
| `conflicting_docs` | Conflicting XML docs across partial files |
| `missing_xml_docs` | No XML documentation found for public member |
| `unresolved_inheritdoc` | `<inheritdoc>` chain could not be resolved |
| `other` | Catch-all for unexpected issues |

### Example Response

```yaml
status: "partial"
generated_files:
  - path: "generated-documentation/src/API/Services/Services.docs.md"
    type: "folder"
  - path: "generated-documentation/src/API/Services/UserService.docs.md"
    type: "file"
  - path: "generated-documentation/src/API/Services/AuthClient.docs.md"
    type: "file"
warnings:
  - type: "parse_failure"
    file: "src/API/Services/LegacyHelper.cs"
    message: "Could not parse file - syntax error at line 47"
child_folders:
  - path: "src/API/Services/Validators"
    file_count: 3
```

---

## Processing Model

### Sequential Execution

- Subagents process one at a time to ensure thoroughness
- Performance is not a priority; correctness is
- Parent folder documentation must complete before child subagents spawn

### Unlimited Recursion

- Subagents recurse into all discovered child folders
- Processing continues until no subfolders remain
- There is no depth limit, timeout, or early termination mechanism

### Recursion Termination

| Condition | Behavior |
|-----------|----------|
| No child folders exist | Return with empty `child_folders` array |
| All child folders contain only ignored files | Skip those folders, return empty `child_folders` |
| Child folders exist but are outside focus patterns | Skip those folders (not in allowlist) |
| Maximum depth reached | N/A — no maximum depth limit exists |

---

## Large Folder Handling

When a folder contains more files than can be processed in a single context window, batched processing is used.

**Detection:** Trigger batching when estimated total source content exceeds 80% of available context window.

**Processing:** See `EXAMPLES/large-folder.md` for detailed batching strategy.

**Key points:**
- Files sorted by documentation priority (interfaces first)
- Each batch generates complete docs before next batch starts
- Cross-batch reference manifest maintains linking accuracy
- Folder doc generated only after ALL batches complete

---

## Completion Output

```
Documentation generation complete.

Generated:
- 1 index document
- 1 root document
- 1 glossary document
- 24 folder documents  
- 87 file documents
- 12 config/resource documents

Validation:
- 0 missing section warnings
- 0 broken link warnings
- 2 stale reference warnings (see INDEX.md)

Output: generated-documentation/
```

---

## Cross-Reference Index

| Topic | Module |
|-------|--------|
| Configuration options | `CONFIG-REFERENCE.md` |
| Document templates | `TEMPLATES/*.md` |
| Signature extraction rules | `RULES/signatures.md` |
| C# language features | `RULES/csharp-features.md` |
| Interface handling | `RULES/interface-handling.md` |
| Partial class handling | `RULES/partial-classes.md` |
| Glossary linking | `RULES/glossary-linking.md` |
| Validation rules | `VALIDATION.md` |
| Worked examples | `EXAMPLES/*.md` |
