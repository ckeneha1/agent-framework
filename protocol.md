# Handoff Protocol

## Flow

```
User initiates project
        ↓
  [ARCHITECT]  →  Architecture Brief  (confirmed by user)
        ↓
   [ANALYST]   →  Review Package
        ↓
  [QA/CRITIC]  →  QA Report
     ↙     ↘
 Issues     Sign-off
   ↓            ↓
[ANALYST]   [ARCHIVIST]  →  Close Report
(fix &          ↓
resubmit)  [ARCHITECT]  →  Post-project retro
```

Loops from QA back to Analyst are expected and healthy. Maximum two loops before escalating to the user.

---

## Handoff 1: User → Architect

**Trigger**: User states a new project is starting.

**Architect's first action**: Do not begin work. Deliver the Architecture Brief first.

**Acceptance check (Architect asks before drafting the brief)**:
- [ ] Do I understand the scope well enough to state what is out of scope?
- [ ] Is there an analytical question, or is this still a vague direction?
- [ ] Do I know the current git state (branch, any in-flight conflicts)?

If any check fails, ask the user to clarify before proceeding.

---

## Handoff 2: Architect → Analyst

**Trigger**: Architecture Brief is complete and user has confirmed it.

**Template**: `templates/architecture-brief.md`

**Analyst acceptance check** (before starting work):
- [ ] Is the analytical question stated in one sentence?
- [ ] Is the expected finding stated?
- [ ] Do I know what branch to work on?
- [ ] Do I know what the build command is?
- [ ] Are there any risk flags I need to handle before starting?

If any check fails, return the brief to Architect with a specific question.

---

## Handoff 3: Analyst → QA/Critic

**Trigger**: Analyst declares analysis complete.

**Template**: `templates/review-package.md`

**QA acceptance check** (before starting review):
- [ ] Is the Review Package complete? (all sections present)
- [ ] Do the files in the manifest actually exist?
- [ ] Does the build succeed from scratch before review begins?

If build fails, return to Analyst immediately — do not review a broken build.

---

## Handoff 4a: QA/Critic → Analyst (issues found)

**Trigger**: QA finds one or more issues.

**Template**: `templates/qa-report.md` (ISSUES FOUND variant)

**Analyst on receiving issues**:
- Fix each issue and note what was changed
- Resubmit a new Review Package
- Maximum two loops. If a third loop is needed, escalate to user.

---

## Handoff 4b: QA/Critic → Archivist (sign-off)

**Trigger**: QA finds no issues (or all issues from a prior loop have been resolved).

**Template**: `templates/qa-report.md` (SIGNED OFF variant)

**Archivist acceptance check** (before starting archival):
- [ ] QA sign-off is present and explicit
- [ ] No outstanding issues from any prior QA loop
- [ ] Full file manifest from the Analyst Review Package is available

---

## Handoff 5: Archivist → Project closed

**Trigger**: Archivist has completed all archival tasks.

**Template**: `templates/close-report.md`

After Close Report is delivered, Architect runs the post-project retro (see `roles/01-architect.md`).

---

## Escalation rule

Any role may escalate to the user when:
- A required input is missing and cannot be inferred
- The same error has occurred twice in the same role
- A QA loop has cycled more than twice
- A risk flag from the Architecture Brief has materialized

Escalation format: state the role, state the blocker, state what you need from the user to proceed. Do not attempt to work around a blocker without flagging it.
