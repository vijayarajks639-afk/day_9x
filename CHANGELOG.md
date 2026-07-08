# Changelog — day_9x

All notable changes to the day_9x prototype. Versions follow the delivery decisions
recorded on the D9X board (`JIRA_STATUS.md`); v0.1 is frozen as tagged.

## v2.0 — 2026-07-06 — "the knowledge miner"

Closes the six gaps found auditing v0.1 against the research dossier in
`Projects/enterprise_ai_pov/` (POV §4/§7; EVIDENCE C6/C8/D3/D4/D10). Built across
build-sprints 3–4 (D9X-16…D9X-26).

- **Knowledge-gap register** (`gaps.py`, G1): every abstain/escalation is persisted as a
  structured mining lead (`data/gaps.json`, deduped), surfaced on the Shadow tab —
  nothing Arjuna can't answer is silently lost.
- **Arjuna's SME interview loop** (G1, the second money shot): Arjuna turns an open gap into
  interview questions; the SME answers; Arjuna writes a **versioned, attributed Skill**
  (`Coached by <SME>, <date>, v1 — captured by Arjuna's interview, source gap G-00N`) and
  reindexes, so the once-unanswerable question now answers with a citation. Grounds the
  POV's "our prototype opportunity" (agent-led externalization, arXiv 2507.03811).
- **SME credit ledger** (`board.py`, G2): per-SME Skills-coached + citations-served,
  shown as "Teachers of the sprint" — attribution as the incentive that flips the
  35%-hoard instinct into teaching.
- **Staleness + ACL realism** (`rag.py` + `agent.py`, G4): a `Supersedes:` freshness rule
  excludes the retired 2025 escalation runbook from the index; an ACL check refuses
  salary/HR questions with a least-privilege message and escalates (a badge, not the
  master key).
- **Team-impact panel** (`breakeven.py`, G3): analyst-hours returned per named human,
  doer→reviewer shift, 48%-vs-19% energization, written stays-human list — the
  52%-job-fear stat answered in the product, not just the pitch.
- **Contribution log + retro co-presentation** (`board.py`, G5): Arjuna's actions persist to
  `data/contribution_log.json`; a downloadable sprint-review co-presentation artifact.
- **Retrieval-eval scorecard** (`evals.py`, C8): per-golden-query top chunk + cosine +
  abstain flag on the Probation tab — we refuse to be one of the ~70% of RAG teams that
  run no retrieval evals.
- Golden set grew to 9 runbook_qa cases (adds the freshness RRO-1 case + the ACL salary
  case). **Eval contract preserved**: uncoached still fails exactly the 2 culture cases
  (Thursday → 8/9; 2% → dq_rule_authoring); coached all green. **23/23 pytest** green.
- Deck regenerated to 13 slides (adds: the miner, Teachers of the sprint, one-team impact).
  Independent partner-agent review documented in `REVIEW_v2.md` (D9X-26). Token usage
  tracked per sprint in `TOKEN_USAGE.md`.

Still blocked on a human credential (carried from v0.1): **D9X-13** GitHub push,
**D9X-14** HF Space deploy.

## v0.1 — 2026-07-05 (frozen)

The first complete delivery: **Onboarding Your First AI Teammate**, the Watkins-grounded
90-days demo. Built across build-sprints 1–2 (D9X-2…D9X-15).

- Five-tab Streamlit app: Charter (Five Conversations + STARS + duration→sprint snapshot) ·
  Shadow mode (RAG + citations + abstain + one-click coaching) · Early wins (approval gates +
  escalation) · Probation review (eval gates) · Breakeven + Retro (day-9x checkpoint reports)
- Hiring-manager controls: onboarding duration (default 90 days = 6 sprints, 10 checkpoints),
  STARS situation selector re-derives the whole plan
- Trapped-knowledge money shot: uncoached evals fail exactly the 2 culture cases
  (Thursday rule, 2% convention); coaching the Skill turns all gates green
- STARS-differentiated breakeven curve (turnaround ≈ day 15, start-up ≈ day 38);
  shadow drafts credit zero realized value (honest value model)
- $0 keyless (public-Space safe); optional local-key Haiku enrichment
- 15/15 pytest green; Jira-ready board (JIRA_STATUS.md + JIRA_IMPORT.csv);
  10-slide stakeholder deck with live numbers (make_deck.py)

Known gaps at freeze (from the 2026-07-05 audit against `Projects/enterprise_ai_pov/`):
no agent-led gap mining/SME interview loop [G1], SME credit not an incentive system [G2],
fear answered in narrative not product [G3], no staleness/ACL realism [G4],
no persistent contribution log/retro artifacts [G5], workflow redesign implicit [G6].
These are the v2.0 scope (Sprints 3–4, D9X-16…D9X-25).
