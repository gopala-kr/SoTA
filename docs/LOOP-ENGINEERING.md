# Loop engineering on this site: audit and backlog

Status as of 30 Oct 2026. This note checks the site's own automation against the six-part loop framework from a LinkedIn post the owner shared (citing Addy Osmani's essay, Geoffrey Huntley's "Ralph" technique and a 36,710-repository study; figures in that post were not independently verified here). Items marked ✅ ADOPTED were built on 30 Oct 2026; the rest remain backlog.

## The six parts, applied to our loops

We run four loops today:

- **A. Daily data refresh:** GitHub Actions; HF papers and the RSI catalog.
- **B. Weekly paper discovery:** GitHub Actions; RSI candidates and citations.
- **C. Weekly Claude data review:** scheduled task "Weekly model release + stack innovation review", Mondays 06:07 UTC.
- **D. The authoring loop:** a Claude session writing articles, maps and data, with the owner prompting.

| Part | A. Daily refresh | B. Discovery | C. Weekly Claude review | D. Authoring session |
|---|---|---|---|---|
| **Trigger** | ✅ cron | ✅ cron | ✅ cron | ❌ the owner presses Enter (human is the loop) |
| **Stop condition** | ✅ script finishes; skips incomplete months | ✅ script finishes | ⚠️ implicit ("nothing qualified" or a PR opened) | ⚠️ implicit: `build.py --check` clean + Playwright clean + screenshots look right |
| **State** | ✅ data files in git | ✅ `rsi-candidates.json` | ⚠️ only git history; no notes file of what was searched/skipped | ❌ lives in the chat; lost when context resets (CLAUDE.md partly fills this) |
| **Verifier** | ✅ `build.py --check` validators (`validate_rsi`, `validate_hf`) | ✅ `validate_discovery` | ⚠️ same validators check structure, but nothing independent checks that facts match sources | ⚠️ the same agent that writes also verifies (no separate "default no" verifier); the owner is the real verifier |
| **Limits** | ⚠️ workflow timeouts only | ⚠️ timeouts only | ⚠️ "never edit from a script without sources", "do not edit pages X" in the prompt; no token/time budget or never-touch file list in git | ❌ no budget; no never-touch list |
| **Escalation** | ✅ failures open or comment on a `data-refresh` issue | ⚠️ none beyond a failed run | ✅ a pull request the owner must approve (report-only, L2) | ✅ owner reviews every change |

**Autonomy levels** (Osmani's handoff ladder):

- A and B are time-based but only touch generated data.
- C is time-based and report-only through PRs: the right level.
- D is turn by turn.

None should rise until a verifier exists that would have caught every bad change so far.

## Already adopted (keep)

1. Progress lives on disk, not in the agent: data in git, `CLAUDE.md` as the long-term brief, generated blocks rebuilt by `build.py`.
2. A machine-checkable gate: `build.py --check` runs in CI (`site-check.yml`) and fails on broken links, stale blocks and invalid data.
3. Report-only for anything factual: the weekly Claude review can only open a PR, never push to the working branch.
4. Honest labelling as a design rule: ⚠️ for secondary sources, "scenario" boxes, "not executed" on code that was not run, disclosure when Anthropic appears.
5. Real verification of code in articles: scripts are run and their real output pasted (this is how Maestro Parts 1–2 caught their own failures).

## Gaps and the changes to make (backlog, in priority order)

Each item follows "design the verifier first": a loop satisfies the gate we write, not the goal behind it.

1. ✅ ADOPTED (`validate_content()` in build.py; caught a missing disclosure on its first run) **Independent content verifier** (gate for loops C and D). A separate check, default "no", that a page passes only if:
   - every Maestro scenario section sits inside a scenario box;
   - every page that mentions Anthropic or Claude carries the disclosure;
   - every `.mo-out` output has its script in the repo;
   - every number tagged as sourced has a source link in the same section.

   Added to `build.py --check` as `validate_content()`.
2. ✅ ADOPTED (`scripts/run_article_code.py`, code in `data/code/<slug>/`, runs in CI) **Article-code harness** (`scripts/run_article_code.py`): keep article scripts under `data/code/<slug>/` and re-run every CPU-runnable one in CI. Fail if output drifts from the published `.mo-out`, which stops "green pipeline, stale article".
3. ✅ ADOPTED (`loops/*.yml`) **Loop config in git** (`loops/*.yml`): one file per loop, reviewed like code. Each file records:
   - the trigger;
   - the stop condition;
   - the state file path;
   - the verifier command;
   - limits: max run minutes or tokens, and a never-touch list (e.g. `pages/*.html` for the data loop, HF and RSI data for the Claude review);
   - the escalation path.
4. ✅ ADOPTED (`loops/state/weekly-review.md`, `docs/LESSONS.md`; the weekly task now reads and appends its state) **State files for the Claude loops:**
   - loop C writes `loops/state/weekly-review.md` (searched, added, skipped and why, open doubts), and reads it first next week;
   - the authoring loop keeps `docs/LESSONS.md` (pitfalls and fixes, e.g. SVG label clipping, `\x22` quoting in inline JS, near-plane clipping, head/nav splicing for new pages).
5. ✅ PARTLY ADOPTED (`scripts/guard_validators.py` + `loops/required-validators.txt` in CI; label-removal detection still to do) **Anti-gaming checks** (the "delete the flaky test" trap):
   - the content verifier rejects diffs that delete validators, loosen a `validate_*` rule, remove ⚠️ or scenario labels, or drop sources;
   - CI fails if `scripts/build.py` validation is weakened without an explicit `ALLOW-VALIDATOR-CHANGE` note in the commit.
6. **Visual regression:**
   - keep reference screenshots of key pages and figures (desktop and phone);
   - flag large pixel diffs after CSS or layout changes;
   - report-only first.
7. **Source monitor** (new weekly loop, report-only): check cited URLs still resolve, flag "as of" dates older than six months, open one issue with the list.
8. ✅ ADOPTED in the task prompt (45-minute cap, never-touch list, issue after two bad runs, state-only PR when nothing qualifies) **Escalation and limits for loop C:**
   - after two consecutive runs with errors or no PR, open an issue instead of retrying;
   - cap research time per run in the prompt;
   - name the reader of each PR (the owner).
9. **Measure before raising autonomy:** a small log of loop C outcomes (PRs accepted, edited, rejected) to decide whether it can ever move beyond report-only.

## Order to build

The order follows the post's template:

1. `validate_content()`: the verifier first.
2. Loop config files with limits and never-touch lists.
3. State files (`weekly-review.md`, `LESSONS.md`).
4. Article-code harness.
5. Anti-gaming checks on validator changes.
6. Visual regression and the source monitor, report-only for two weeks before they can fail CI.
