# Close Report — [project name]

## Metrics
Run `python scripts/metrics.py /path/to/session.jsonl` and paste the output here.
To find the session JSONL: `ls -t ~/.claude/projects/<project-slug>/*.jsonl | head -1`

| Metric | This project | Baseline | Δ |
|---|---|---|---|
| Tool error rate | [X%] | 8% | [+/-] |
| Tool errors (count) | [N] | — | — |
| Git errors | [N] | ~18/session | [+/-] |
| Files edited >3x | [N files] | 4/session | [+/-] |
| User turns | [N] | — | — |
| Output tokens | [N] | — | — |
| QA loops | [0/1/2] | N/A | — |
| QA issues found | [N] | N/A | — |

Notes: [anything that skews the numbers — e.g. exploratory work, teardown/reinstall cycles]

## Reproducibility
Build command: [command]
Test result: [passed / failed — and what was fixed if failed]

## Decisions log
| Decision | Alternatives considered | Reason chosen | Where implemented |
|---|---|---|---|
| [decision] | [alternatives] | [reason] | [file/line] |

## Memory files updated
- [file]: [what was changed]

## Outstanding items
| Item | Why deferred | Where tracked |
|---|---|---|
| [item] | [reason] | [file or issue] |

## Project closed
[date]

---
*Architect post-project retro follows.*
