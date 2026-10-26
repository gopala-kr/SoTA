# Loops

Each file here describes one loop that runs on this site, using the six parts from
docs/LOOP-ENGINEERING.md: trigger, stop condition, state, verifier, limits, escalation.
They are reviewed like code. A loop may only raise its autonomy level when its verifier
would have caught every bad change it has produced so far (see `outcomes` in each file).

| Loop | File | Autonomy |
|---|---|---|
| Daily data refresh | data-refresh.yml | time-based, generated data only |
| Weekly paper discovery | discovery.yml | time-based, candidates only |
| Weekly Claude data review | weekly-review.yml | time-based, report-only (pull requests) |
| Authoring sessions | authoring.yml | turn by turn (owner reviews every change) |

Shared gate for all loops: `python3 scripts/build.py --check`, `python3 scripts/guard_validators.py`,
`python3 scripts/run_article_code.py` (all run in .github/workflows/site-check.yml).
