# Sprint Retro — day_9x

## What we set out to build
An interview-asset prototype: onboard an AI agent into a human scrum team using Watkins'
*The First 90 Days*, with the hiring manager setting duration (default 90 days = 6 sprints).

## Delivered (Sprints 1–2)
- **Config-as-contract** (`config.py`): task classes, STARS pacing, trust states, value model,
  Watkins attribution — every module keys off it.
- **Synthetic world** (`generate_data.py`): 6 runbooks, an *unwritten-rules* doc (the coachable
  Skill), a 10-task backlog with an unknown-system escalation trap, recon figures with real
  arithmetic, and a 21-case golden eval set.
- **Shadow-mode RAG** (`rag.py`): structure-aware chunking + **contextual chunk headers**,
  local ONNX embeddings, citations, abstain guardrail. $0 by default.
- **Charter** (`charter.py`): Five Conversations, STARS→phase pacing, duration→sprint snapshot
  + day-9x checkpoints.
- **Agent** (`agent.py`): deterministic backbones for triage / recon / DQ-rule authoring +
  helpful-abstain escalation; optional Haiku enrichment.
- **Board + trust ledger** (`board.py`): approval gates, per-class trust state machine, the
  coaching→reindex loop.
- **Probation review** (`evals.py`): per-class eval gates; two culture cases red until coached.
- **Breakeven ledger** (`breakeven.py`): value consumed vs created; STARS-differentiated curve;
  day-9x reports.
- **App** (`app.py`): five-tab journey; hiring-manager sidebar (duration + STARS).
- **Tests** (`test_day9x.py`): 15 passing. **Evals**: green (coached) / 2 culture reds (uncoached).

## What went well
- **The eval before/after is the demo.** Uncoached, exactly the Thursday-rule and 2%-convention
  cases fail; coaching flips both green. It proves the trapped-knowledge thesis in one click.
- **STARS visibly changes breakeven.** Turnaround breaks even ~day 15 with a shallow dip;
  start-up dips deeper and breaks even ~day 38. The situation drives the story, not one-size-fits-all.
- **Reuse paid off.** RAG pipeline, eval-harness pattern, and $0-fallback/abstain patterns came
  straight from `reg_rag_assistant` and `river_fish`.

## What we fixed mid-flight
- A tiny "## Tolerance" section wouldn't retrieve on its own → **contextual chunk headers**
  (prefix the doc title) lifted it into the top-k. Retrieval hygiene, not a model change.
- Breakeven hit day 1 (wrong story) → **shadow drafts create zero realized value** (the human
  still owns the output). Now the curve dips through shadow then climbs — the true Watkins point.

## Still open (blocked on a human credential)
- **D9X-13** GitHub push — needs a PAT at push time (deliberately not stored).
- **D9X-14** HF Space deploy — needs an HF token; follows the push.

## If we had another sprint
- Persist the trust ledger + contribution log across sessions (currently in `st.session_state`).
- A GraphRAG pass over the runbooks for multi-hop "how do X and Y interact" questions.
- A "fleet" view — Watkins' *Expedite everyone*: onboarding many agents with one common language.

---

# Build Sprint 3–4 — v2.0 "the knowledge miner"

## What we set out to build
We froze v0.1 and then **audited our own delivery against our own research** (the
`enterprise_ai_pov/` dossier — POV §4 pushbacks P2/P3/P5 and §7, EVIDENCE C6/C8/D3/D4/D5/D10).
The audit found six real gaps between what the demo showed and what the POV *claimed the winning
play was*. v2.0 closes them: G1 agent-led gap mining · G2 SME credit incentive · G3 fear answered
in product · G4 staleness/ACL realism · G5 ritual artifacts · G6 workflow-redesign framing.

## Delivered (Sprints 3–4, D9X-16…D9X-25)
- **Gap register** (`gaps.py` + `data/gaps.json`): every abstain/escalation persists as a
  structured knowledge gap (`G-001…`, question, hypothesis, status open→closed). Knowledge-gaps
  panel on the Shadow tab.
- **Interview agent** (the new money shot): for an open gap, Arjuna drafts 3 SME interview questions
  ($0 deterministic, optional Haiku), the user picks an SME and types the answer, and Arjuna writes a
  versioned, **attributed** Skill ("Coached by <SME>, <date>, v1 — interviewed by Arjuna, source gap
  G-00N"), reindexes, and closes the gap. The old one-click coach button remains as a demo shortcut.
- **SME credit ledger**: per-SME counters (Skills coached, citations served) surfaced as
  "Teachers of the sprint."
- **Staleness + ACL realism**: a v1/v2 conflicting escalation-contacts runbook pair; the v2 declares
  `Supersedes:` the v1 and retrieval excludes the superseded doc (freshness rule, visible in UI).
  ACL: comp/appraisal questions are refused with a least-privilege message citing the charter scopes.
- **Team impact panel**: hours returned per named human, doer→reviewer shift, 48%-vs-19%
  energization contrast, stays-human list with owners.
- **Contribution log + retro artifacts** (`data/contribution_log.json`): a retro view + a
  downloadable sprint-review **co-presentation** markdown (the Scrum.org D10 ritual).
- **Evals + retrieval scorecard**: golden `runbook_qa` set grows to 9 (adds the freshness case and
  the ACL-refusal case); a per-golden-query scorecard (top doc + cosine + abstain flag) now runs on
  the Probation tab, closing the "70% run no retrieval evals" gap inside our own demo.

## What went well
- **v0.1 froze cleanly with a tag.** CHANGELOG + version stamp + `git tag v0.1` gave us an honest
  baseline to build against — and a documented list of the six known gaps at freeze, so v2.0 scope
  wrote itself.
- **Auditing the build against our own research found six *real* gaps.** Not cosmetic — each one was
  a claim the POV made (SME incentives, tacit-knowledge loop, freshness/ACLs, retrieval evals,
  ritual artifacts) that v0.1 asserted in narrative but didn't *demonstrate*.
- **The interview loop closed the POV's #1 novel-feature promise.** §7 named the agent-led SME
  interview as "our prototype opportunity"; the gap→interview→attributed-Skill roundtrip is now a
  live, cited, $0 loop grounded in arXiv 2507.03811 (94.9% recall in simulation, [C6]). It's the
  second money shot the demo was missing.
- **Attribution turned out to be a mechanism, not a nicety.** Wiring the SME credit ledger made the
  D4/D5 "hoarding flips to teaching" finding *visible* — "your knowledge answered N questions" is a
  concrete incentive, not a slogan.

## What to improve
- **We should have run this audit before shipping v0.1**, not after. The gaps were derivable from the
  POV the whole time; calling v0.1 "done" was premature by our own standard.
- **The eval math got fragile as the golden set grew.** Adding the freshness and ACL cases nudged the
  uncoached `runbook_qa` pass rate to exactly 8/9 = 89% against a 90% gate — correct, but the margin
  is one case wide. It needs a comment in `evals.py` explaining *why* the threshold sits there so a
  future edit doesn't silently break the red-before-coaching story.
- **Persistence is still half-done.** Gaps and the contribution log now write to `data/*.json`, but
  the trust ledger still lives in `st.session_state`. Two storage models in one app invites drift.
- **GitHub/HF push (D9X-13/14) is still blocked on a human credential** — unchanged from v0.1.

## Three lessons
1. **Audit your delivery against your own research before you call it done.** Our own POV predicted
   the exact features v0.1 was missing. "Passing tests" is not "matching the thesis."
2. **Attribution is corpus-quality engineering, not sentiment.** Crediting SMEs isn't a morale
   feature — it's the input-quality control that keeps the 35% who hoard from poisoning or starving
   the corpus. Design the credit ledger with the same seriousness as the retrieval eval.
3. **Freshness and ACLs are the difference between a RAG demo and a deployable.** A similarity search
   that happily serves last year's on-call list or answers a salary question is a prototype;
   supersedes-rules, provenance, and least-privilege refusals are what a banking buyer actually buys.
