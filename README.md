# agent-framework

A four-role orchestration framework for blog analysis projects, designed to run inside Claude Code via CLAUDE.md conventions.

## The idea

Each project runs through four roles in sequence. No role signs off on its own work. Every handoff requires a hard artifact before the next role begins.

```
User → [ARCHITECT] → Architecture Brief
      → [ANALYST]  → Review Package
      → [QA]       → QA Report
      → [ARCHIVIST]→ Close Report → [ARCHITECT] retro
```

## Repository layout

```
roles/              Role definitions
  01-architect.md   Pre-project brief, mid-project monitoring, post-project retro
  02-analyst.md     Question formulation, charts, claims, prose standards
  03-qa.md          Direction, magnitude, formula, silent failure, claims, chart checks
  04-archivist.md   Reproducibility, decisions log, memory update

templates/          Fill-in-the-blank handoff artifacts
  architecture-brief.md
  review-package.md
  qa-report.md
  close-report.md

specs/              Spec-driven CI: required sections for every framework document
protocol.md         Full handoff flow with acceptance checklists
CLAUDE.md           Instructions for Claude Code — how to activate and run the framework
scripts/
  activate.sh       Initialize a project to use this framework
  validate.py       Spec validator (run by CI)
```

## Using the framework

### Activate on a project

```bash
bash /path/to/agent-framework/scripts/activate.sh /path/to/your/project
```

This copies `CLAUDE.md` into the project root and creates a `.agent/` directory for handoff artifacts.

### Starting a project

Tell Claude: `"New project: [name]"` — the Architect role activates and produces an Architecture Brief. Confirm the brief, then say `"start working"`.

### CI

The spec validator runs on every push and PR. It checks that all role files, templates, protocol.md, and CLAUDE.md contain their required sections. A missing or renamed section fails the build.

```bash
python scripts/validate.py
```

## Design decisions

- **Four roles, not six** — Presentation collapsed into Analyst (what's worth charting is inseparable from how you'd present it). Architecture collapsed into Architect/Management.
- **Sequential handoffs with hard artifacts** — not parallel, to maintain accountability.
- **Conflict of interest rule** — the agent that builds a thing cannot sign off on it. QA is always independent.
- **No external dependencies** — plain markdown files and a stdlib Python validator. Activate with a shell script.

## Pilot

First project run through the framework: `feat/color-efficiency-post` branch of [gatheringdata-blog](https://github.com/ckeneha1/gatheringdata-blog). Issues caught by QA: 1 (factual error in prose). Issues caught by Archivist: 1 (output artifacts writing to `/tmp`). Both fixed before merge.
