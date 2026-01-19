# Full Spec Template: New Projects

**For new projects with medium or complex complexity.**

---

```markdown
# Product Specification: [Product Name]

**Version:** [X.Y]
**Status:** [Draft | In Review | Changes Requested | RC | Approved | Superseded]
**Owner:** [Name]
**Last Updated:** [Date]
**Approvers:** [Names]
**Format:** [Target format]

---

## 1. Problem Statement

### The Problem

[Detailed description: Who has this problem, when they experience it, what triggers it, and why it matters to them.]

### Impact of Not Solving

| Impact Type | Quantified Effect |
|-------------|-------------------|
| Revenue | [$ amount lost/month or year] |
| Time | [Hours wasted per user/week] |
| Churn | [% users lost due to this] |
| Other | [Specific metric] |

### Previous Attempts

| Solution Tried | Why It Failed |
|----------------|---------------|
| [Approach 1] | [Reason] |
| [Approach 2] | [Reason] |

### Success Metrics

| Metric | Target | How Measured | Confidence | Baseline |
|--------|--------|--------------|------------|----------|
| [Metric 1] | [Target] | [Method] | High/Med/Low | [Current] |
| [Metric 2] | [Target] | [Method] | High/Med/Low | [Current] |

---

## 2. Users & Stakeholders

### Stakeholder Map (RACI)

| Role | Person/Team | Responsibility |
|------|-------------|----------------|
| **R**esponsible | [Name] | Does the work |
| **A**ccountable | [Name] | Final decision maker |
| **C**onsulted | [Names] | Input required |
| **I**nformed | [Names] | Keep in the loop |

### User Personas

#### Persona: [Name/Role]

| Attribute | Details |
|-----------|---------|
| **Who** | [Job title, context] |
| **Goals** | [What they're trying to achieve] |
| **Current workflow** | [Step-by-step how they do it today] |
| **Pain points** | [Specific frustrations] |
| **Technical level** | Novice / Intermediate / Expert |
| **Success looks like** | [Observable outcome] |

*[Repeat for each persona]*

---

## 3. Scope

### In Scope (MVP)

| Feature | Priority | Depends On | Confidence |
|---------|----------|------------|------------|
| [Feature 1] | Must | — | High/Med/Low |
| [Feature 2] | Must | Feature 1 | High/Med/Low |
| [Feature 3] | Should | — | High/Med/Low |
| [Feature 4] | Could | Feature 2 | High/Med/Low |

### Out of Scope

- [Explicit exclusion 1]
- [Explicit exclusion 2]

### Non-Goals

Things this will NOT do, even if users request:
- [Non-goal 1]
- [Non-goal 2]

### Future Iterations (Post-MVP)

| Feature | Why Deferred | Prerequisite |
|---------|--------------|--------------|
| [Future 1] | [Reason] | [What must exist first] |

---

## 4. Technical Context

### Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | [Tech] | [Why] |
| Backend | [Tech] | [Why] |
| Database | [Tech] | [Why] |
| Infrastructure | [Tech] | [Why] |

### Integration Points

| System | Type | Owner | Purpose | Notes |
|--------|------|-------|---------|-------|
| [System 1] | API/Event/File | [Team] | [Why needed] | [Constraints] |

### Performance Requirements

| Metric | Target | Confidence | Rationale |
|--------|--------|------------|-----------|
| Latency (p95) | [X ms] | High/Med/Low | [Why this target] |
| Throughput | [X req/s] | High/Med/Low | [Based on] |
| Availability | [X%] | High/Med/Low | [SLA requirement] |
| Concurrent users | [X] | High/Med/Low | [Growth projection] |

### Security & Compliance

- **Authentication:** [Method]
- **Authorization:** [Model]
- **Data encryption:** [At rest / In transit]
- **Compliance:** [Standards — SOC2, GDPR, HIPAA, etc.]
- **Audit requirements:** [What must be logged]

### Constraints

| Constraint | Impact | Workaround |
|------------|--------|------------|
| Budget: [Amount] | [What it limits] | [If any] |
| Timeline: [Deadline] | [What it forces] | [If any] |
| Team: [Size/skills] | [What it limits] | [If any] |

---

## 5. Functional Requirements

### Feature: [Name]

**Priority:** Must / Should / Could
**Depends on:** [Features] or None
**Confidence:** High / Medium / Low
**Estimate:** [T-shirt size or points]

#### Description
[One paragraph explaining what this feature does and why]

#### Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

#### Examples

**Happy path:**
> Given [context], when [user action], then [expected result]

**Edge case:**
> Given [unusual condition], when [action], then [expected handling]

**Error case:**
> Given [failure condition], when [action], then [error behavior]

#### Technical Notes
[Implementation considerations, if any]

---

*[Repeat Feature block for each feature]*

---

## 6. Non-Functional Requirements

### Performance

*[Reference targets from Technical Context]*

- Response time: [Target]
- Throughput: [Target]
- Concurrent capacity: [Target]

### Reliability

| Metric | Target |
|--------|--------|
| Availability | [X% uptime] |
| RTO (Recovery Time) | [Time to recover] |
| RPO (Recovery Point) | [Max data loss tolerance] |
| Degradation behavior | [What happens under failure] |

### Usability

- **Accessibility:** [WCAG level — A, AA, AAA]
- **Internationalization:** [Languages supported]
- **Browser support:** [List]
- **Device support:** [Desktop, mobile, tablet]

### Maintainability

- **Code standards:** [Linting, formatting rules]
- **Documentation:** [What must be documented]
- **Test coverage:** [Target %]
- **On-call:** [Expectations]

---

## 7. Data Specifications

### Data Models

[Entity descriptions or ERD reference]

| Entity | Key Fields | Relationships |
|--------|------------|---------------|
| [Entity 1] | [Fields] | [Relations] |

### Storage

- **Database:** [Type and provider]
- **Projected size:** [Initial and growth]
- **Backup:** [Strategy]

### Data Lifecycle

| Operation | Actor | Retention | Notes |
|-----------|-------|-----------|-------|
| Create | [Who] | — | [Validation rules] |
| Read | [Who] | — | [Access controls] |
| Update | [Who] | — | [Audit requirements] |
| Delete | [Who] | [Policy] | [Soft/hard delete] |
| Archive | [Who] | [Policy] | [Where archived] |

### Privacy & Security

- **PII fields:** [List]
- **Encryption:** [Requirements]
- **Access controls:** [Who sees what]
- **Retention policy:** [How long kept]

---

## 8. Dependencies

### External Services

| Service | Purpose | Criticality | Fallback | Owner |
|---------|---------|-------------|----------|-------|
| [Service] | [Why] | High/Med/Low | [Plan B] | [Team] |

### Third-Party Libraries

| Library | Purpose | License | Risk | Alternative |
|---------|---------|---------|------|-------------|
| [Library] | [Why] | [License] | [Concerns] | [Backup option] |

### Internal Dependencies

| Team/Service | What We Need | Timeline | Status |
|--------------|--------------|----------|--------|
| [Team] | [Deliverable] | [When] | [Status] |

---

## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation | Owner | Confidence |
|------|------------|--------|------------|-------|------------|
| [Risk 1] | H/M/L | H/M/L | [Plan] | [Who] | H/M/L |
| [Risk 2] | H/M/L | H/M/L | [Plan] | [Who] | H/M/L |

### Assumptions

| Assumption | Impact if Wrong | Validation Plan |
|------------|-----------------|-----------------|
| [Assumption 1] | [Consequence] | [How to verify] |

### Anti-Pattern Watch

- [ ] **Scope creep signals:** [Current status]
- [ ] **Metric gaming potential:** [Identified risks]
- [ ] **Single points of failure:** [List]
- [ ] **Optimistic timeline:** [Buffer included?]

---

## 10. Validation Strategy

### Testing Approach

| Type | Scope | Responsibility | Coverage Target |
|------|-------|----------------|-----------------|
| Unit | [What] | Dev | [%] |
| Integration | [What] | Dev/QA | [%] |
| E2E | [Paths] | QA | [Critical paths] |
| Performance | [Scenarios] | [Team] | [Targets] |
| Security | [Scope] | [Team] | [Standards] |

### UAT

- **Who:** [Stakeholders involved]
- **When:** [Timeline]
- **Sign-off process:** [How approval works]

### Rollout Strategy

- [ ] Feature flags: [List]
- [ ] Canary: [% of traffic]
- [ ] Phased rollout: [Stages]
- [ ] Rollback trigger: [Criteria]

### Success Validation

| Check | When | Metric | Target |
|-------|------|--------|--------|
| Launch | Day 1 | [What] | [Target] |
| Week 1 | Day 7 | [What] | [Target] |
| Month 1 | Day 30 | [What] | [Target] |

---

## 11. Timeline

| Milestone | Target Date | Dependencies | Owner | Status |
|-----------|-------------|--------------|-------|--------|
| Spec approved | [Date] | — | [Name] | |
| Design complete | [Date] | Spec | [Name] | |
| Dev complete | [Date] | Design | [Name] | |
| Testing complete | [Date] | Dev | [Name] | |
| Launch | [Date] | Testing | [Name] | |

---

## 12. Open Questions

| # | Question | Owner | Due Date | Status | Resolution |
|---|----------|-------|----------|--------|------------|
| 1 | [Question] | [Who] | [When] | Open/Resolved | [Answer if resolved] |

---

## 13. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [Date] | [Name] | Initial draft |

---

## Appendix

### Glossary

| Term | Definition |
|------|------------|
| [Term] | [Meaning in this context] |

### References

- [Document 1]
- [Document 2]

### Sources

- [List of uploaded/referenced materials]
```

---

## Full New Spec Guidelines

### Section Requirements by Complexity

| Section | Medium | Complex |
|---------|--------|---------|
| 1. Problem Statement | Required | Required + deeper impact analysis |
| 2. Users & Stakeholders | Required | Required + secondary personas |
| 3. Scope | Required | Required + dependency graph |
| 4. Technical Context | Required | Required + detailed capacity planning |
| 5. Functional Requirements | Required | Required + comprehensive edge cases |
| 6. Non-Functional Requirements | Required | Required + SLA details |
| 7. Data Specifications | If applicable | Required if any data |
| 8. Dependencies | Required | Required + risk analysis |
| 9. Risks | Required | Required + anti-pattern analysis |
| 10. Validation Strategy | Required | Required + detailed test plan |
| 11. Timeline | Required | Required + dependency mapping |
| 12. Open Questions | Required | Required |

### Quality Checks

- [ ] Every metric has a specific number
- [ ] Every feature has acceptance criteria
- [ ] Every risk has a mitigation and owner
- [ ] Every dependency has a fallback
- [ ] Every open question has an owner and due date
- [ ] Timeline has realistic buffers
