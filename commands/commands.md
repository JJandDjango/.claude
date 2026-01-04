---
name: Document
allowed-tools: Glob, Task, Write(generated-documentation/**), Edit(generated-documentation/**)
description: Generate documentation for code
argument-hint: [filepath]
---

# Document

Generate documenation for `FILEPATH` by examining the codebase and writing comprehensive documentation.

## Variables

FILEPATH: $1 (e.g., "src/Api/Clients/Auth/IAuthClient.cs" or "IAuthClient.cs")

## Workflow

1. Verify `FILEPATH` is provided (stop if missing)
2. Find the source file using Glob (search if only filename given, use as-is if path provided)
3. Launch the doc-explorer agent to handle the entire documentation process

## Task Agent Instructions

Launch a Task agent with the following prompt:

```markdown
Generate comprehensive documentation for: {FILEPATH}

**Process:**
1. Read source file at {FILEPATH}
2. Output to: generated-documentation/{source_path}/{filename}.md
3. Explore codebase (very thorough) for: usages, DI registration, tests, config, dependencies, real examples
4. Read template: docs/AI/DocumentationExample.md
5. Check/read output file if it exists (Write tool requirement)
6. Follow template format:
  - class/interface overview
  - constructor
  - methods
    - signature
    - purpose
    - parameters
    - behavior
    - compatible examples
    - returns
    - throws
    - line-numbered references
  - configuration
  - related models
  - testing
7. Write to output file

**Requirements:**
- Self-contained (no source reading needed)
- Accurate line numbers in all references
- Compilable C# examples with contextual descriptions
- Complete public API coverage

**Return:** "Documentation for {filename} written to {output_path}
```

## Report

After the agent completes, confirm: "Documentation for `FILENAME` complete"
