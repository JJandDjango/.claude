# Rules: Glossary Linking

> **Version:** 2.0.0  
> **Role:** Defines how glossary terms are automatically linked in generated documentation.

---

## Overview

When generating documentation, the generator automatically links glossary terms according to these rules. This creates consistent terminology linking without manual effort.

---

## Matching Behavior

| Rule | Behavior | Example |
|------|----------|---------|
| Case-insensitive | Matches regardless of case | "tenant" matches glossary term "Tenant" |
| Whole words only | Prevents partial matches | "Tenant" matches; "TenantId" does NOT |
| First occurrence only | Links once per document | First "Tenant" linked; subsequent plain text |
| Plural/stem matching | Common variations match | "Tenants" matches "Tenant" |

### Plural Matching Rules

| Glossary Term | Also Matches |
|---------------|--------------|
| `Tenant` | `Tenants` |
| `Claim` | `Claims` |
| `Policy` | `Policies` |
| `Entity` | `Entities` |
| `Status` | `Statuses` |

**Stemming is conservative:** Only standard English plural forms are matched. Complex variations require explicit glossary entries.

---

## Exclusion Zones

Terms are NOT linked when they appear in:

### 1. Code Blocks (Inline or Fenced)

```csharp
private readonly ITenantService _tenantService;  // "Tenant" NOT linked
```

**Rationale:** Code should remain unmodified; readers expect exact syntax.

### 2. Headings (Any Level)

```markdown
## TenantService  <!-- "Tenant" NOT linked -->
### Tenant Management  <!-- "Tenant" NOT linked -->
```

**Rationale:** Headings are navigation anchors; links create visual confusion.

### 3. Table Cells

| Type | Name |
|------|------|
| class | TenantService |  <!-- NOT linked -->

**Rationale:** Tables are dense; links clutter formatting.

**Exception:** When `glossary_linking.link_in_tables: true`, terms in table cells ARE linked.

### 4. YAML Frontmatter

```yaml
namespace: "MyProject.Tenant.Services"  # NOT linked
```

### 5. Already-Linked Text

```markdown
See [TenantService](./TenantService.docs.md)  // "Tenant" NOT linked again
```

**Rationale:** Avoid nested or adjacent links.

### 6. File/Folder Names in Paths

```markdown
Located in `src/API/Tenant/`  // "Tenant" NOT linked
```

---

## Link Format

Links use relative paths from the document location to the glossary at the documentation root.

### Path Calculation

```markdown
// Glossary location: generated-documentation/MyProject.glossary.md

// From: generated-documentation/MyProject.docs.md
[Tenant](./MyProject.glossary.md#tenant)

// From: generated-documentation/src/API/Services/UserService.docs.md
[Tenant](../../../MyProject.glossary.md#tenant)
```

### Anchor Format

- Lowercase the term
- Replace spaces with hyphens
- Remove special characters

| Glossary Term | Anchor |
|---------------|--------|
| `Tenant` | `#tenant` |
| `Tenant Claim` | `#tenant-claim` |
| `OAuth 2.0` | `#oauth-20` |
| `API Key` | `#api-key` |

---

## Implementation Algorithm

```
FUNCTION link_glossary_terms(document_text, glossary_terms, doc_path):
    IF glossary_linking.enabled == false:
        RETURN document_text  // Skip linking entirely
    
    linked_terms = empty set
    glossary_path = calculate_relative_path(doc_path, glossary_location)
    link_count = 0
    max_links = glossary_linking.max_links_per_doc OR infinity
    
    FOR EACH section IN document_text:
        // Skip exclusion zones
        IF section.type IN [code_block, heading, frontmatter]:
            CONTINUE
        
        IF section.type == table AND NOT glossary_linking.link_in_tables:
            CONTINUE
        
        FOR EACH term IN glossary_terms:
            IF term IN linked_terms:
                CONTINUE  // Already linked this term
            
            IF link_count >= max_links:
                RETURN document_text  // Hit link limit
            
            // Build pattern with word boundaries and plural variants
            pattern = word_boundary + case_insensitive(term + plural_variants) + word_boundary
            
            match = first_match(section.text, pattern)
            
            IF match EXISTS AND NOT inside_existing_link(match):
                anchor = lowercase(term).replace(" ", "-").remove_special_chars()
                link = "[{match.text}]({glossary_path}#{anchor})"
                section.text = replace_first(section.text, match, link)
                linked_terms.add(term)
                link_count += 1
    
    RETURN document_text
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Term appears only in code blocks | No link created |
| Term in heading, then in prose | Link created in prose only |
| Overlapping terms | Link longer term first |
| Term at start of sentence | Link created; capitalization preserved |
| Glossary is empty or missing | Skip linking entirely; no warnings |
| Term is part of compound word | Link anyway if word boundary matches |

### Overlapping Terms

When glossary contains overlapping terms like "Tenant" and "Tenant Claim":

1. Sort terms by length (longest first)
2. Match longer terms before shorter
3. Once "Tenant Claim" is linked, "Tenant" won't match that occurrence

**Example:**
```markdown
// Glossary: "Tenant", "Tenant Claim"
// Input: "The Tenant Claim is validated for the Tenant"

// Output: "The [Tenant Claim](...#tenant-claim) is validated for the [Tenant](...#tenant)"
```

### Compound Words

| Term | Text | Matches? |
|------|------|----------|
| `Tenant` | `TenantService` | ❌ No (no word boundary) |
| `Tenant` | `tenant-service` | ❌ No (hyphenated compound) |
| `Tenant` | `the tenant's data` | ✅ Yes (possessive OK) |
| `Tenant` | `multi-tenant` | ❌ No (part of compound) |

---

## Configuration

```yaml
# documentation-config.yaml

glossary_linking:
  enabled: true           # default: true; set false to disable all linking
  link_in_tables: false   # default: false; set true to link in table cells
  max_links_per_doc: null # default: null (no limit); set integer to cap
```

### When to Disable

- **Very short documents:** Linking may feel excessive
- **Technical reference docs:** Pure API docs may not need conceptual links
- **Generated code docs:** Auto-generated content may conflict

### When to Limit

Set `max_links_per_doc` when:
- Documents are very long
- Many glossary terms create visual noise
- Prefer fewer, higher-impact links

---

## Glossary Term Best Practices

### Good Terms

| Term | Definition |
|------|------------|
| `Tenant` | Clear domain concept |
| `Claim` | Security-specific meaning |
| `Idempotent` | Technical term needing definition |

### Avoid as Terms

| Term | Why |
|------|-----|
| `User` | Too common; would over-link |
| `Data` | Too generic |
| `Service` | Technical but ubiquitous |
| `API` | Well-known; no added value |

### Term Definition Guidelines

1. **Project-specific meaning:** Only add terms with meanings specific to this codebase
2. **Not obvious:** Don't define industry-standard terms unless used differently
3. **Consistent naming:** Use the canonical form (singular, title case)

---

## Example

**Glossary config:**
```yaml
glossary:
  Tenant: "An organization or customer account in the multi-tenant system"
  Claim: "A security assertion about a user's identity or permissions"
  Scope: "A permission boundary defining what actions a token can perform"
```

**Input document:**
```markdown
## Purpose

Manages tenant provisioning and lifecycle. Each tenant has claims
that define their scope of access. The TenantService validates
tenant claims before granting access.

### Configuration

```yaml
tenant:
  defaultClaims: ["read", "write"]
```

| Property | Description |
|----------|-------------|
| TenantId | Unique tenant identifier |
```

**Output document:**
```markdown
## Purpose

Manages [Tenant](../MyProject.glossary.md#tenant) provisioning and lifecycle. Each tenant has [claims](../MyProject.glossary.md#claim)
that define their [scope](../MyProject.glossary.md#scope) of access. The TenantService validates
tenant claims before granting access.

### Configuration

```yaml
tenant:
  defaultClaims: ["read", "write"]
```

| Property | Description |
|----------|-------------|
| TenantId | Unique tenant identifier |
```

**What was linked:**
- "Tenant" (first occurrence in prose) ✅
- "claims" (first occurrence, plural matched) ✅
- "scope" (first occurrence) ✅
- "tenant" in code block ❌ (exclusion zone)
- "tenant" in table ❌ (exclusion zone)
- Second "tenant" in prose ❌ (already linked)
- "claims" second occurrence ❌ (already linked)

---

## Cross-Reference

| Topic | Module |
|-------|--------|
| Glossary template | `TEMPLATES/glossary.md` |
| Configuration | `CONFIG-REFERENCE.md` |
