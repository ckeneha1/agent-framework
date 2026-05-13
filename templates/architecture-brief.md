# Architecture Brief — [project name]

## Scope
In scope: [what will be built]
Out of scope: [what will not be touched]

## Analytical question
[One sentence. If this cannot be written, the project is not ready to start.]

Expected finding: [One sentence: "I expect X because Y."]

## Git workflow
Branch: [branch name]
Merge target: [e.g., main, or another feature branch]
Current branch state: [clean / conflicts present / behind remote]
Prerequisite git operations: [any operations needed before analyst starts, or "none"]

## Build contract
Build command: [e.g., `uv run python analyze.py`]

Expected output artifacts (must be repo paths, not temp directories):
- [file 1 — full path from repo root]
- [file 2 — full path from repo root]

## Toolkit assessment
Existing tools being used: [list]
Gaps requiring new build: [list, or "none"]
New libraries needed: [list, or "none"]

## Parallelism plan
Sequential (must be in order):
1. [step]
2. [step]

Parallel (can run concurrently):
- [step A] alongside [step B]

## Risk flags
- [known landmine or tricky dependency]
- [or "none identified"]

---
*Confirm this brief before analyst begins work.*
