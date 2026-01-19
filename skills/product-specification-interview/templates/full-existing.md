# Full Spec Template: Existing Projects

**For existing projects with medium or complex complexity. Includes current state analysis, tribal knowledge capture, and migration planning.**

---

```markdown
# Product Specification: [Product Name] — Revision

**Version:** [X.Y]
**Status:** [Draft | In Review | Changes Requested | RC | Approved | Superseded]
**Owner:** [Name]
**Last Updated:** [Date]
**Approvers:** [Names]
**Format:** [Target format]
**Previous Version:** [Link or reference]

---

## 1. Problem Statement

### Original Problem

[What this system was originally built to solve]

### What Actually Happened

| Expected | Actual |
|----------|--------|
| [Original assumption] | [Reality] |
| [Original metric target] | [Actual result] |

### Current Problem

[What needs to change now — the reason for this revision]

### Success Metrics

| Metric | Current | Target | Gap | Confidence |
|--------|---------|--------|-----|------------|
| [Metric 1] | [Now] | [Goal] | [Delta] | H/M/L |
| [Metric 2] | [Now] | [Goal] | [Delta] | H/M/L |

---

## 2. Users & Stakeholders

### Expected vs Actual Users

| Expected | Actual | Surprise Factor |
|----------|--------|-----------------|
| [Who we built for] | [Who actually uses it] | [What we learned] |

### User Feedback Themes

| Theme | Frequency | Severity | Source |
|-------|-----------|----------|--------|
| [Complaint/request] | [How often] | H/M/L | [Feedback channel] |

### Workarounds Discovered

| Workaround | Why Users Do This | Implication |
|------------|-------------------|-------------|
| [Behavior] | [Root cause] | [What we should fix] |

### Stakeholder Map (RACI)

| Role | Person/Team | Responsibility |
|------|-------------|----------------|
| **R**esponsible | [Name] | Does the work |
| **A**ccountable | [Name] | Final decision maker |
| **C**onsulted | [Names] | Input required |
| **I**nformed | [Names] | Keep in the loop |

---

## 3. Current State Analysis

### What Works Well

| Component | Why It Works | Preserve? |
|-----------|--------------|-----------|
| [Feature/system] | [Reason for success] | Yes/No |

### Pain Points

| Issue | Severity | Impact | Frequency | Root Cause |
|-------|----------|--------|-----------|------------|
| [Problem] | H/M/L | [Effect] | [How often] | [Why it happens] |

### Technical Debt

| Item | Risk if Ignored | Effort to Fix | Priority | Notes |
|------|-----------------|---------------|----------|-------|
| [Debt item] | [Consequence] | S/M/L/XL | Must/Should/Could | [Context] |

### Tribal Knowledge

**Critical undocumented knowledge that must be captured:**

| Knowledge | Why It Matters | Risk if Lost |
|-----------|----------------|--------------|
| [Non-obvious behavior] | [Impact] | [Consequence] |
| [Historical decision] | [Why it was made] | [If forgotten] |
| [Gotcha for new devs] | [What breaks] | [Recovery difficulty] |

#### "If It Breaks" Procedures

| Symptom | Likely Cause | Fix | Who Knows |
|---------|--------------|-----|-----------|
| [What you see] | [Root cause] | [Steps] | [Person] |

### Operational Burden

| Metric | Current | Acceptable? |
|--------|---------|-------------|
| Maintenance hours/week | [Hours] | Yes/No |
| On-call incidents/month | [Count] | Yes/No |
| Deploy frequency | [Cadence] | Yes/No |
| Deploy pain level | [1-10] | Yes/No |
| Time to onboard new dev | [Days] | Yes/No |

---

## 4. Scope

### Keep (Working Well)

| Feature | Why Keep | Any Changes? |
|---------|----------|--------------|
| [Feature] | [Reason] | None / Minor tweak |

### Modify (Needs Improvement)

| Feature | Current Issue | Proposed Change | Priority | Breaking? |
|---------|---------------|-----------------|----------|-----------|
| [Feature] | [Problem] | [Solution] | Must/Should/Could | Yes/No |

### Add (Missing)

| Feature | Why Needed | Priority | Depends On |
|---------|------------|----------|------------|
| [Feature] | [Gap it fills] | Must/Should/Could | [Prerequisites] |

### Remove (Deprecate)

| Feature | Why Remove | Migration Path | User Impact |
|---------|------------|----------------|-------------|
| [Feature] | [Reason] | [Transition plan] | [Who affected] |

### Out of Scope This Revision

- [What we're explicitly not changing]
- [Deferred improvements]

---

## 5. Technical Context

### Current Architecture

[Description or diagram of existing system]

| Component | Technology | Health | Notes |
|-----------|------------|--------|-------|
| [Component] | [Tech] | Good/Degraded/Poor | [Issues] |

### Proposed Changes

| Component | Current | Proposed | Rationale | Risk |
|-----------|---------|----------|-----------|------|
| [Component] | [Now] | [After] | [Why change] | H/M/L |

### Integration Points

| System | Type | Status | Changes Needed |
|--------|------|--------|----------------|
| [System] | API/Event/File | Working/Problematic | [Modifications] |

### Performance: Current vs Target

| Metric | Current | Target | Gap | How to Close |
|--------|---------|--------|-----|--------------|
| Latency (p95) | [X ms] | [Y ms] | [Delta] | [Approach] |
| Throughput | [X/s] | [Y/s] | [Delta] | [Approach] |
| Availability | [X%] | [Y%] | [Delta] | [Approach] |

### Technical Constraints

| Constraint | Impact | Negotiable? |
|------------|--------|-------------|
| [Constraint] | [Effect on project] | Yes/No |

---

## 6. Functional Requirements

### Modified Features

#### Feature: [Name] — MODIFICATION

**Current behavior:** [What it does now]
**Problem:** [Why it needs to change]
**Proposed behavior:** [What it should do]
**Priority:** Must / Should / Could
**Breaking change:** Yes / No

#### Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

#### Migration Notes
- How existing users transition: [Plan]
- Data migration required: [Yes/No — details]
- Rollback plan: [How to revert]

---

### New Features

#### Feature: [Name] — NEW

**Priority:** Must / Should / Could
**Depends on:** [Features] or None

#### Description
[What this feature does and why it's needed]

#### Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

#### Examples

**Happy path:**
> Given [context], when [action], then [result]

**Edge case:**
> Given [unusual], when [action], then [handling]

---

*[Repeat for each feature]*

---

## 7. Non-Functional Requirements

### Current vs Target

| Category | Metric | Current | Target | Priority |
|----------|--------|---------|--------|----------|
| Performance | Latency | [Now] | [Goal] | Must/Should |
| Reliability | Uptime | [Now] | [Goal] | Must/Should |
| Usability | [Metric] | [Now] | [Goal] | Must/Should |

### What Must Change

| Requirement | Current Gap | Proposed Solution | Effort |
|-------------|-------------|-------------------|--------|
| [NFR] | [Problem] | [Fix] | S/M/L |

---

## 8. Data Specifications

### Schema Changes

| Entity | Change Type | Details | Migration |
|--------|-------------|---------|-----------|
| [Entity] | Add/Modify/Remove | [What] | [How] |

### Data Migration Plan

| Step | Description | Rollback | Duration | Risk |
|------|-------------|----------|----------|------|
| 1 | [Action] | [Revert plan] | [Time] | H/M/L |

### Backward Compatibility

| Data Type | Compatibility Requirement | How Achieved |
|-----------|---------------------------|--------------|
| [Type] | [Requirement] | [Approach] |

---

## 9. API & Contract Changes

| API/Endpoint | Change | Breaking? | Version Strategy | Consumer Impact |
|--------------|--------|-----------|------------------|-----------------|
| [Endpoint] | [What changes] | Yes/No | [v1 → v2] | [Who affected] |

### Deprecation Timeline

| API | Deprecation Date | Removal Date | Migration Guide |
|-----|------------------|--------------|-----------------|
| [API] | [When] | [When] | [Link/details] |

### Consumer Communication Plan

| Audience | Message | Channel | Timing |
|----------|---------|---------|--------|
| [Who] | [What to tell them] | [How] | [When] |

---

## 10. Migration Considerations

### Backward Compatibility Requirements

| Requirement | Duration | How Maintained |
|-------------|----------|----------------|
| [What must keep working] | [How long] | [Approach] |

### Migration Steps

| Phase | Description | Success Criteria | Rollback |
|-------|-------------|------------------|----------|
| 1 | [Action] | [How we know it worked] | [Revert steps] |
| 2 | [Action] | [How we know it worked] | [Revert steps] |

### User Communication

| Audience | Timing | Message | Channel |
|----------|--------|---------|---------|
| [Users] | [When] | [What to communicate] | [How] |

### Rollback Plan

**Trigger criteria:** [When to rollback]
**Steps:**
1. [Step 1]
2. [Step 2]
**Recovery time:** [Expected duration]
**Data implications:** [What happens to data created after deployment]

---

## 11. Dependencies

### Problematic Current Dependencies

| Dependency | Problem | Action | Priority |
|------------|---------|--------|----------|
| [Dep] | [Issue] | Keep/Update/Remove/Replace | Must/Should |

### New Dependencies

| Dependency | Purpose | Risk | Alternative |
|------------|---------|------|-------------|
| [Dep] | [Why needed] | [Concerns] | [Backup] |

---

## 12. Risks & Mitigations

### Historical Issues

| Past Incident | Root Cause | Lesson | Applied Here? |
|---------------|------------|--------|---------------|
| [What broke] | [Why] | [Learning] | Yes/No |

### Current Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| [Risk] | H/M/L | H/M/L | [Plan] | [Who] |

### Revision-Specific Risks

| Risk | Why This Revision | Mitigation |
|------|-------------------|------------|
| Migration failure | [Why likely] | [Plan] |
| User disruption | [Why likely] | [Plan] |
| Regression | [Why likely] | [Plan] |

---

## 13. Validation Strategy

### Regression Testing

| Area | Test Approach | Coverage | Owner |
|------|---------------|----------|-------|
| [Feature area] | [How tested] | [Scope] | [Who] |

### New Functionality Testing

| Feature | Test Type | Acceptance Criteria |
|---------|-----------|---------------------|
| [Feature] | [Unit/Integration/E2E] | [Pass criteria] |

### Rollout Strategy

- [ ] Feature flags: [List]
- [ ] Canary deployment: [% traffic]
- [ ] Phased rollout: [Stages]
- [ ] Rollback trigger: [Criteria]
- [ ] Monitoring: [What to watch]

### Success Validation

| Check | Timing | Metric | Current | Target |
|-------|--------|--------|---------|--------|
| Pre-launch | Before | [Baseline] | [Value] | — |
| Launch | Day 1 | [Metric] | — | [Target] |
| Week 1 | Day 7 | [Metric] | — | [Target] |

---

## 14. Timeline

| Milestone | Target | Dependencies | Owner | Status |
|-----------|--------|--------------|-------|--------|
| Spec approved | [Date] | — | [Name] | |
| Migration tested | [Date] | Spec | [Name] | |
| Staged rollout | [Date] | Migration | [Name] | |
| Full launch | [Date] | Staged | [Name] | |
| Old version sunset | [Date] | Launch | [Name] | |

---

## 15. Open Questions

| # | Question | Owner | Due | Status |
|---|----------|-------|-----|--------|
| 1 | [Question] | [Who] | [When] | Open |

---

## 16. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| [X.Y] | [Date] | [Name] | [Summary] |

---

## Appendix

### Tribal Knowledge Archive

[Detailed capture of undocumented knowledge from Section 3]

### Historical Decisions

| Decision | Date | Rationale | Still Valid? |
|----------|------|-----------|--------------|
| [What was decided] | [When] | [Why] | Yes/No/Revisit |
```

---

## Full Existing Spec Guidelines

### Key Differences from New Projects

| Aspect | New Project | Existing Project |
|--------|-------------|------------------|
| Problem framing | Future state | Current vs desired state |
| Scope | Build list | Keep/Modify/Add/Remove |
| Users | Personas | Expected vs actual |
| Technical | Greenfield | Current architecture + changes |
| Risks | Hypothetical | Historical + new |
| Validation | Test plan | Regression + new |

### Required Sections

| Section | Medium | Complex |
|---------|--------|---------|
| 3. Current State Analysis | Required | Required + deep tribal knowledge |
| 10. Migration Considerations | Required | Required + detailed rollback |
| Historical risks | Required | Required + incident analysis |

### Quality Checks

- [ ] Current state accurately captured (validated with team)
- [ ] Tribal knowledge documented and attributed
- [ ] Every modification has migration path
- [ ] Breaking changes identified with communication plan
- [ ] Rollback plan is concrete and tested
- [ ] Historical lessons explicitly applied
