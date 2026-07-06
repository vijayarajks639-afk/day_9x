# REVIEW_v2.md — Independent review of day_9x v2.0 "the knowledge miner"

**Story:** D9X-26 · **Reviewer:** partner Opus review agent (independent) · **Date:** 2026-07-06
**Scope:** audit the v2.0 delivery (six gaps G1–G6) — run the suite, read the source, check the
honesty of the demo claims against the code, and check research alignment against
`Projects/enterprise_ai_pov/` (POV §4/§7, EVIDENCE C6/C8/D3/D4/D10).
Read-only review; the repo was reset to its clean "before" state afterward.

---

## Executive verdict

**SHIP-WITH-FIXES.**

The v2.0 *code* is sound and honest — 23/23 tests pass, the evals behave exactly as documented, and
every one of the six new mechanisms does what its docstring claims. The single material problem is a
**documentation defect, not a code defect**: `DEMO_WALKTHROUGH.md`'s flagship "money-shot #2" is
scripted around the Thursday question producing a knowledge gap, but the code does not create a gap
for that question. For a live interview asset that mismatch is a credibility risk and must be fixed
before presenting. No code blockers. One doc-level Major.

---

## 1 · Results table (verbatim, reproduced by the reviewer)

| Command | Expected | Observed | Exit |
|---|---|---|---|
| `python -m pytest test_day9x.py -q` | 23 passed | `23 passed in 17.66s` | **0** ✅ |
| `python evals.py` (uncoached) | exit 1; exactly 2 culture RED | 2 RED, 2 GREEN (below) | **1** ✅ |
| `python evals.py --coached` | exit 0; all GREEN | 4/4 classes GREEN (below) | **0** ✅ |

**Uncoached `python evals.py` (verbatim):**
```
[RED] Runbook Q&A: 8/9 = 89% (gate 90%)
       FAIL: Can I rerun the CreditMart load on Thursday morning? — missing tokens ['Thursday']  (culture case — coach the Skill)
[GREEN] Data-incident triage: 6/6 = 100% (gate 85%)
[GREEN] Reconciliation variance check: 4/4 = 100% (gate 88%)
[RED] DQ rule authoring: 3/4 = 75% (gate 90%)
       FAIL: lgd/completeness — missing ['2%']  (culture case — coach the Skill)

Probation review: gates red — hold; coach Skills / keep reviewing.
```

**Coached `python evals.py --coached` (verbatim):**
```
Coached Skills in corpus: ['unwritten_rules.md']

[GREEN] Runbook Q&A: 9/9 = 100% (gate 90%)
[GREEN] Data-incident triage: 6/6 = 100% (gate 85%)
[GREEN] Reconciliation variance check: 4/4 = 100% (gate 88%)
[GREEN] DQ rule authoring: 4/4 = 100% (gate 90%)

Probation review: ALL GATES GREEN — promotion may be offered.
```

**Clean-state check.** `.gitignore` covers `data/` (verified with `git check-ignore data/gaps.json
data/skills/x.md data/contribution_log.json` — all three matched). The on-disk `data/` I inherited
was *not* clean (it carried leftover `skills/unwritten_rules.md`, `contribution_log.json`,
`sme_credit.json`, `skill_authors.json` from prior runs) — which would have masked the two uncoached
RED cases. I reset to the true "before" (skills empty; only `backlog.json`, `golden_set.json`,
`team.json` remain) *before* the uncoached run, and again afterward. **No `data/` artifact is
tracked; a fresh clone boots clean** (`generate_data.ensure_generated()` writes runbooks/backlog/
golden set only — it never coaches a Skill). v2.0 currently lives as **uncommitted working-tree
changes on top of tag `v0.1`**, plus the untracked `gaps.py`; it is not yet committed or tagged.

## 2 · Edge cases the reviewer actually ran (`python -c` probes)

| Probe | Result |
|---|---|
| (a) `interview_questions()` with **no API key** | Returns **exactly 3** deterministic lines (Haiku path skipped). ✅ |
| (b) `author_skill()` → re-ask the question | Answer is non-abstained, **cites the new `skill_*.md`**, contains the mined token ("11:00"); gap flips to **closed**. ✅ |
| (c) ACL question ("What is Priya's salary?") | `acl_blocked=True`, `abstained=True`, **citations empty**, escalation says "scope". ✅ |
| (d) Superseded doc | `index.superseded = {2025 → 2026}`; **no `escalation_contacts_2025` id in `index.ids`**; 2026 chunks present. ✅ |
| (e) Credit only coached Skills | `credit_citations([skill#0, runbook_dq_rules.md#1])` → only the SME's counter increments; the runbook citation is ignored. ✅ |
| (f) Gap dedupe + persistence | Re-recording the same question (whitespace/case-normalized) returns the same `G-001`; reload from disk preserves id + status. ✅ |

Every v2.0 code claim in tasks 2(a)–(f) holds. The `�` glyphs seen when printing interview
questions to a Windows cp1252 console are the source's curly quotes/em-dashes — cosmetic (see Nit 1),
not a defect; Streamlit renders UTF-8.

---

## 3 · Findings by severity

### Blocker — none found
The suite is green, the evals are exact, and all six mechanisms are correct. Stated plainly: there
are **zero code blockers**.

### Major
**M1 — The demo's "money-shot #2" is scripted on a gap the code never creates.**
`DEMO_WALKTHROUGH.md:34-37` claims the Thursday question "**abstains and escalates**" and "that
abstain just became a **structured gap**, e.g. `G-001 — "Can I rerun the CreditMart load on Thursday
morning?"`", and `:47-49` then says "pick the open Thursday gap and click **Interview an SME**."
The code does the opposite: uncoached, that question retrieves `runbook_recon_gl_vs_creditmart.md#1`
at **score 0.399 > `MIN_SCORE` 0.30** (`config.py:50`), so `answer()` returns a **non-abstained**
answer with **empty `escalation`** (`agent.py:76-98`). The Shadow tab only logs a gap on
`elif out.escalation:` (`app.py:141-145`), so **no gap `G-001` appears** — the Knowledge-gaps panel
stays empty and money-shot #2 cannot be run as written. The eval correctly flags the same answer as
RED ("missing tokens ['Thursday']"), so the *harness* is honest; only the *walkthrough* over-claims.
Note the prose is even self-contradictory ("answers from the nearest runbook … so it abstains").
*Fix (doc-only, no code change needed):* seed the gap from a path that genuinely escalates — I
verified **T-104 "Feed delay reported on OrionLedger"** (Early-wins tab, unknown system) escalates
and logs a real gap (`app.py:234-235`); or use an out-of-scope question. Rewrite `:32-49` and the
`:45` parenthetical to interview on that gap, and drop "abstains and escalates" for the Thursday
question (it answers, wrongly, which is the eval's teaching moment — not the gap register's).

### Minor
**m1 — Freshness beat mislabels the superseded runbook as "2024".**
`DEMO_WALKTHROUGH.md:68-69` says Kai "shows the **v1 (2024)** runbook excluded as superseded." The
file is `runbook_escalation_contacts_2025.md`, "*Last updated: 2025-03-10*" (`generate_data.py:150`),
and the UI caption (`app.py:169-171`) prints `runbook_escalation_contacts_2025.md`. *Fix:* change
"(2024)" to "(2025)". (The beat itself is real — I confirmed the 2026 runbook is cited and the 2025
one is absent from `index.ids`.)

**m2 — Persistent, process-global mutable state under `data/` with no boot reset.**
`skills/`, `gaps.json`, `sme_credit.json`, `contribution_log.json` (`board.py:25-27`, `gaps.py:22`)
persist across app restarts and are shared by all users of a single process. On a public HF Space,
concurrent viewers mutate one another's gaps/teachers/log, and a fresh audience sees stale
"Teachers of the sprint" / contribution log until someone presses **Full demo reset** (`app.py:161-167`).
*Fix:* clear the v2.0 registries on `boot()` (or namespace them per `st.session_state.session_id`),
so every session starts from the honest "before".

### Nit
**n1 — Deterministic interview questions use Unicode curly quotes/em-dashes** (`agent.py:211-216`:
`"…"`, `—`). Fine in Streamlit (UTF-8); mangled on any cp1252 CLI/log surface. *Fix:* plain ASCII
quotes/dashes, or `reconfigure(encoding="utf-8")` on any CLI entry point that prints them.

---

## 4 · Research-alignment (G1–G6 vs `enterprise_ai_pov`)

| Gap | v2.0 mechanism | Evidence | Status |
|---|---|---|---|
| **G1** agent-led gap mining → SME interview → attributed Skill | `gaps.py` register + `agent.interview_questions()` + `board.author_skill()` → reindex → citable | POV §5 "our prototype opportunity" · **C6** (94.9% recall, in sim) | **Closed in code** (tests + probes green) · **demo path at risk — see M1** |
| **G2** SME credit as an incentive (hoarding→teaching) | `_register_author` + `credit_citations` + `teachers_of_the_sprint`; only coached Skills credited | POV P2 · **D4** (35% hoard; 48% vs 19% energized) | **Closed** |
| **G3** fear answered in the product, not the pitch | `breakeven.team_impact()` hours-returned + doer→reviewer + 48/19 caption | POV A3/P2 · **D3** (52% fear) / **D4** | **Closed** |
| **G4** staleness + ACL realism | `rag` "Supersedes:" freshness (2025 excluded) + `agent._acl_check()` + `evals.retrieval_scorecard()` | POV P5 · **C8** (staleness, ACL, 70%-no-evals) | **Closed** |
| **G5** ritual artifacts (mixed human/agent scrum) | `board.contribution_log` + `co_presentation()` (human presents, log is evidence) | POV §6 Stage 3 · **D10** | **Closed** |
| **G6** workflow redesign | Only narrated (doer→reviewer in `team_impact`); labelled "implicit"/"framing" (`CHANGELOG.md:66`, `SPRINT_RETRO.md:59`); a deck slide, no distinct in-app mechanism | POV P1 · **A2** (workflow redesign = #1 EBIT driver) | **Partial** |

Five of six gaps are genuinely closed in code. G6 is by the team's own admission a framing/deck item,
not a product mechanism — fair, and consistent with the POV's own P1 caveat that trapped-knowledge
unlock is "necessary, not sufficient" without a process-change program.

---

## 5 · What's genuinely strong (earned)

The eval story is the real asset and it is honest: uncoached, the harness lands RED on **exactly** the
two culture cases (Thursday 8/9=89%, 2% 3/4=75%) and green everywhere else, and coaching flips it to
all-green — the trust mechanism is demonstrated on the tool itself, not asserted. The v2.0 realism is
testable rather than cosmetic: the 2025 runbook is *actually* removed from `index.ids` (not just
down-ranked), and the salary question is refused with `acl_blocked=True`, no citations, and — the
subtle right call — is **not** logged as a knowledge gap (a scope refusal is not a corpus gap). The
gap→interview→authored-Skill→reindex→citable loop works end-to-end and credits only coached Skills,
which is precisely the D4 "attribution flips hoarders into teachers" thesis made mechanical. The
retrieval-eval scorecard puts the C8 "70% run no retrieval evals" differentiator directly in the UI.
23/23 tests are load-bearing (dedupe, persistence, ACL, freshness, interview roundtrip, credit) —
not vanity coverage.

## 6 · Residual risks for the interview setting

1. **M1 is a live-demo failure risk.** Following the current script, the presenter asks the Thursday
   question and the Knowledge-gaps panel shows "No open gaps" — the flagship v2.0 feature appears to
   do nothing. Fix the walkthrough (seed from T-104) and rehearse the exact click path before the room.
2. **Stale shared state (m2).** If the Space was used before, "Teachers of the sprint" and the retro
   log may already be populated. Press **Full demo reset** first, or fix boot to auto-reset.
3. **Confident-but-wrong Thursday answer.** Uncoached, Kai gives a plausible non-abstained answer from
   an unrelated recon runbook (0.399) that omits the rule — a mild instance of the very "confident
   wrongness" the demo says it prevents. The eval catches it; a live Shadow-tab viewer does not see an
   abstain. Narrate this as "the eval catches what the eye can't," not "it refuses to answer."
4. **Cold-start latency.** First boot downloads/loads the ~90MB fastembed model behind the
   "Onboarding Kai…" spinner (`app.py:29`). Warm the Space before presenting.
5. **Point-in-time snapshot.** During this review the working tree received concurrent edits to
   `CHANGELOG.md`, `PROMPTS_LOG.md`, `SPRINT_RETRO.md`, `make_deck.py`, `day_9x_stakeholder_deck.pptx`,
   and a new untracked `DEPLOYMENT_PLAN.md` appeared — from another process, not this reviewer. Findings
   reflect the code as read at review time.
6. **Not yet frozen.** v2.0 is uncommitted changes atop `v0.1` (+ untracked `gaps.py`). Nothing under
   `data/` is tracked (good), but the v2.0 delivery still needs its own commit/tag.

---

*Reviewer actions were read-only + tests + `python -c` probes; the only file written was this one.
`data/` was reset to the clean "before" state (skills empty; no stray gaps/log/credit JSON).*
