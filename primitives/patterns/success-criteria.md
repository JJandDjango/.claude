---
name: success-criteria
description: Reusable verification checklists for common thread types. Reference for agent self-evaluation and handoff reports.
reference: true
---

# Success Criteria Templates

<purpose>
Provide reusable verification checklists for common thread types. Agents should reference these when self-evaluating or preparing handoff reports.
</purpose>

<context>
These checklists are templates. Copy the relevant section into your `criteria` tag or handoff report.
</context>

<examples>
## Implementation Thread Criteria

Before marking implementation complete:

- [ ] All new code compiles/transpiles without errors
- [ ] Linter passes with zero warnings
- [ ] Unit tests exist for all new public functions
- [ ] All tests pass locally
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Changes are atomic and focused on a single concern
- [ ] Code follows existing project conventions

## Documentation Thread Criteria

Before marking documentation complete:

- [ ] All public APIs have JSDoc/docstrings
- [ ] Parameter types and return types are documented
- [ ] Examples provided for non-obvious usage
- [ ] No broken internal links
- [ ] README updated if public interface changed

## Refactor Thread Criteria

Before marking refactor complete:

- [ ] Existing tests still pass (no regressions)
- [ ] No functional changes unless explicitly intended
- [ ] Performance characteristics unchanged or improved
- [ ] All callers of modified code still work
- [ ] Git history is clean (squashed if appropriate)

## Verifier Audit Criteria

Before issuing a PASS verdict:

- [ ] Tests re-run independently (not trusting Developer logs)
- [ ] Build completes in clean environment
- [ ] Code review completed for all modified files
- [ ] No "shallow" tests that don't exercise actual logic
- [ ] Security implications considered for input/output changes
- [ ] Handoff report matches actual changes
</examples>
