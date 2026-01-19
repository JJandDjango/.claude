# Lite Spec Template

**For simple projects. One page maximum.**

---

```markdown
# [Product Name] — Lite Spec

**Version:** [X.Y] | **Status:** [Status] | **Owner:** [Name] | **Date:** [Date]

---

## Problem

[2-3 sentences: Who has this problem, what the problem is, why solving it matters. Include impact — time, money, or pain.]

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| [Primary metric] | [Specific number] | [Measurement method] |
| [Secondary metric] | [Specific number] | [Measurement method] |

## Primary User

**[Role/Persona name]**
- Context: [When/where they encounter this problem]
- Technical level: [Novice / Intermediate / Expert]
- Success looks like: [Observable outcome for this user]

## Must-Have Features

### [Feature 1 Name]

**What:** [One sentence description]

**Done when:**
- [ ] [Testable acceptance criterion]
- [ ] [Testable acceptance criterion]

---

### [Feature 2 Name]

**What:** [One sentence description]

**Done when:**
- [ ] [Testable acceptance criterion]
- [ ] [Testable acceptance criterion]

---

### [Feature 3 Name] *(if applicable)*

**What:** [One sentence description]

**Done when:**
- [ ] [Testable acceptance criterion]

---

## Out of Scope

- [What this explicitly won't do]
- [Feature that might seem related but isn't included]
- [Future consideration not in v1]

## Technical Notes

- **Stack:** [Languages, frameworks, key libraries]
- **Constraints:** [Key limitations — budget, timeline, infrastructure]
- **Integrations:** [External systems this connects to]
- **Environment:** [Where this runs — cloud, on-prem, local]

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Primary risk] | H/M/L | H/M/L | [Fallback plan] |
| [Secondary risk] | H/M/L | H/M/L | [Fallback plan] |

## Open Questions

| Question | Owner | Due Date |
|----------|-------|----------|
| [Unresolved question] | [Who answers] | [When needed] |

## Timeline

| Milestone | Target |
|-----------|--------|
| Spec approved | [Date] |
| Development complete | [Date] |
| Launch | [Date] |

---

*Simple spec for simple project. Expand to full spec if scope grows.*
```

---

## Lite Spec Guidelines

### When to Use
- Project classified as "simple"
- ≤4 must-have features
- ≤2 integration points
- Solo developer or small team
- Clear, well-understood problem

### Structure Rules
- **One page** — if it's longer, project isn't simple
- **3 features maximum** — more than that, escalate to medium
- **Single user persona** — if multiple distinct users, escalate
- **One risk table** — keep it focused

### Quality Checks Before Output
- [ ] Problem statement is specific (who + what + why)
- [ ] Metrics have numbers (not "improve" or "better")
- [ ] Each feature has testable acceptance criteria
- [ ] Out of scope is explicit (prevents scope creep)
- [ ] At least one risk identified with mitigation

### Common Lite Spec Mistakes
- **Vague features:** "User authentication" → "Email/password login with password reset flow"
- **Missing acceptance criteria:** Every feature needs "done when"
- **No out of scope:** Always define boundaries
- **Generic risks:** "Something might go wrong" → "Third-party API rate limits could block imports"
