# Jira Status — day_9x (project D9X)

Single source of truth for the D9X board, kept in-repo so it stays current even when no Jira API
token is in session. **Worklogs are AI-actual minutes** (not human-equivalent), per the team cadence
([[jira-story-first]]). Stories are created **before** the work and updated live — never batch-logged.
Sync to Jira via UI, or provide a token and I'll push it via the REST API.

**What this builds:** "The New Team Member" — an AI teammate's first 90 days on a credit-risk
data-ops scrum team, modelled mechanism-by-mechanism on Watkins' *The First 90 Days*. Interview
asset for the Anthropic Applied AI / Solutions Architect application ([[project-anthropic-application]]).

_Last updated: 2026-07-06 (**SHIPPED & LIVE**: v2.0 tagged; GitHub published
github.com/vijayarajks639-afk/day_9x (tags v0.1 + v2.0); HF Space live at
**huggingface.co/spaces/vijayarajks/day-9x** — Docker runtime, $0/keyless, no API key secret.
Epic D9X-1 exit criteria all met → **Done**.)_

> **Upload to Jira:** import `JIRA_IMPORT.csv` (Jira Cloud → Filters/Board → *Import issues from CSV*).
> It carries Issue Key, Type, Summary, Description, Sprint, Status, Epic Link, and AI-actual
> Time Spent. Or create project **D9X** (Kanban, 2 sprints) and copy the tables below.

## Epic
- **D9X-1 — Epic: day_9x — AI teammate's first-90-days demo (Watkins-grounded)** — ✅ **Done**
  (exit criteria met 2026-07-06: 23/23 tests + evals green · GitHub pushed with tags v0.1/v2.0 ·
  HF Space live and serving)

## Sprint 1 — the engine
| Key | Story | Status | AI worklog |
|---|---|---|---|
| D9X-2 | Scaffold repo + `config.py` shared contract + docs skeleton | ✅ Done | 20 |
| D9X-3 | Synthetic team data generator (runbooks, tickets, backlog, roster, golden set) | ✅ Done | 35 |
| D9X-4 | RAG shadow engine (fastembed → numpy cosine → citations + abstain) | ✅ Done | 30 |
| D9X-5 | Charter module (Five Conversations + STARS + duration→sprint snapshot) | ✅ Done | 30 |
| D9X-6 | Agent core (draft/scoped-task/escalate; $0 deterministic + optional Haiku) | ✅ Done | 35 |
| D9X-7 | Task board + approval gates (approve / reject / coach→Skill) | ✅ Done | 25 |
| D9X-8 | Eval harness + per-task-class trust ledger (exit-code gates promotion) | ✅ Done | 30 |

**Sprint 1 verification (D9X-8):** `python evals.py` — uncoached: exactly the 2 culture
cases RED (Thursday rule, 2% convention), other classes GREEN → *hold*. `--coached`:
all 4 classes GREEN → *promotion may be offered*. The retrieval fix (contextual chunk
headers) took the tiny "## Tolerance" section into the top-k. Behaves as designed.

## Sprint 2 — story & ship
| Key | Story | Status | AI worklog |
|---|---|---|---|
| D9X-9 | Breakeven ledger (value consumed vs created) + per-checkpoint 9-day reports | ✅ Done | 30 |
| D9X-10 | Streamlit assembly (5 tabs + checkpoint slider + duration control) | ✅ Done | 40 |
| D9X-11 | `test_day9x.py` unit tests + QA run | ✅ Done (15/15 green) | 25 |
| D9X-12 | README (HF front-matter + Watkins credit) + PROMPTS_LOG + docs; POV/STORY pointers | ✅ Done | 25 |
| D9X-13 | Push all commits to GitHub | ✅ Done | 10 (repo created via API; main + tags v0.1/v2.0 pushed; token used once, not stored) |
| D9X-14 | Deploy to HuggingFace Spaces ($0 public, keyless) | ✅ Done | 20 (HF deprecated native Streamlit SDK → Docker runtime added; Space live, no API-key secret) |
| D9X-15 | Demo walkthrough + SPRINT_RETRO + stakeholder PPT | ✅ Done | 30 |

**Burn-up:** 13/15 stories Done · 2 Blocked (external credential) · **AI-actual total: ~410 min**.

## Sprint 3 — v2.0 "the knowledge miner" (gap analysis vs enterprise_ai_pov research, 2026-07-05)

v0.1 is **frozen** (tag `v0.1`). v2.0 closes the six gaps found when auditing the delivery against
the POV research (G1 agent-led gap mining · G2 SME credit incentive · G3 fear answered in product ·
G4 staleness/ACL realism · G5 ritual artifacts · G6 workflow-redesign slide).

| Key | Story | Status | AI worklog |
|---|---|---|---|
| D9X-16 | Freeze v0.1: CHANGELOG, version stamp (config/app/README), local git tag | ✅ Done | 20 |
| D9X-17 | Gap register (`gaps.py` + data/gaps.json + Knowledge-gaps panel) [G1 substrate] | ✅ Done | 30 |
| D9X-18 | Interview agent: gap → SME interview → authored, attributed Skill → reindex [G1] | ✅ Done | 40 |
| D9X-19 | SME credit ledger: Skills coached / citations served per SME ("Teachers of the sprint") [G2] | ✅ Done | 25 |
| D9X-20 | Staleness (v1/v2 runbook conflict, freshness-aware) + ACL scope enforcement [G4] | ✅ Done | 35 |

**Sprint 3 verification:** the eval before/after contract is preserved — uncoached still fails
exactly the 2 culture cases (Thursday → runbook_qa 8/9 = 89% < 90%; 2% → dq_rule_authoring
3/4 = 75%); the new freshness (RRO-1) and ACL (salary) cases pass GREEN throughout, because they
are realism, not the teaching moment. Coached → all GREEN.

## Sprint 4 — v2.0 "one team" & ship

| Key | Story | Status | AI worklog |
|---|---|---|---|
| D9X-21 | Team impact panel: hours returned, doer→reviewer shift, energization contrast [G3] | ✅ Done | 25 |
| D9X-22 | Contribution log + retro view + sprint-review co-presentation artifact [G5] | ✅ Done | 30 |
| D9X-23 | Extend test_day9x.py (gap capture, interview roundtrip, credit, ACL, freshness) | ✅ Done (23/23 green) | 30 |
| D9X-24 | Extend evals (interview-loop golden cases) + retrieval-eval scorecard [C8] | ✅ Done | 35 |
| D9X-25 | Docs + deck v2 (13 slides, two money shots + one-team) + JIRA_IMPORT.csv append | ✅ Done | 30 |
| D9X-26 | **Independent review pass**: partner agent audits v2.0 (code + tests + honesty of claims), documents outcomes in REVIEW_v2.md | ✅ Done | — (partner Opus review agent) |
| D9X-27 | Apply review findings: M1 gap-seed + honest app/walkthrough copy, m1 (2025 label), m2 boot reset, n1 ASCII; re-verify (23/23 tests, eval contract, e2e) | ✅ Done | 25 |

**v2.0 burn-up:** 12/12 Sprint 3–4 stories Done · review **SHIP-WITH-FIXES**, all findings
applied & re-verified ·  **AI-actual (v2.0): ~325 min** · partner-agent tokens tracked in
`TOKEN_USAGE.md`. Carried blocked (external credential): **D9X-13** GitHub push, **D9X-14** HF deploy.

**Review outcome (D9X-26 → REVIEW_v2.md):** verdict SHIP-WITH-FIXES; zero code blockers, 23/23
tests, eval contract exact. One Major (M1, doc/app copy: the Thursday question answers-but-wrong
rather than abstaining — gap-mining money-shot re-seeded on a genuinely-ungrounded question) +
2 Minors (m1 label, m2 boot reset) + 1 nit (n1 ASCII). All fixed in D9X-27; G6 confirmed
Partial-by-design (framing/deck, not a product mechanism).

## Sprint cadence (documented for the D9X board)

The **team** cadence (what the synthetic scrum team runs — this is what the *demo portrays*)
and the **build** cadence (how we actually built the prototype) are deliberately the same shape,
so the tool practises what it preaches.

| Ceremony | When | Purpose | Where it shows up |
|---|---|---|---|
| Sprint length | **15 days** | so 90-day onboarding = exactly **6 sprints** | duration slider → sprint snapshot |
| Daily stand-up | 09:30 daily | surface blockers early ("silent struggling is the firing offence") | `team_ways_of_working.md` |
| **Day-9x checkpoint** | every **9 days** (x=1…10) | short stakeholder progress report | Breakeven tab slider → `checkpoint_report()` |
| Sprint review + retro | last day of each sprint | demo increment; inspect + adapt | `SPRINT_RETRO.md` |
| Probation review | end of onboarding (day 90) | eval-gated autonomy decision (expand / hold / reduce) | Probation-review tab |

**Why two clocks (15-day sprint vs 9-day checkpoint) are intentional:** sprints pace the *work*;
the day-9x checkpoints pace *stakeholder communication*. They interleave — a stakeholder never
waits a full sprint for a signal, and the team never re-plans mid-sprint just to report. At 90
days the two clocks share the endpoint (day 90 = sprint 6 close = checkpoint x=10 = probation review).

Cadence detail lives in `SPRINT_CADENCE.md`.

## Legend
⚪ To Do · 🔵 In Progress · ✅ Done · ⏳ Blocked (needs a human action)

## Summary
- **Plan:** 15 stories (D9X-2…D9X-15) across 2 sprints; engine first, then story & ship.
- **Cadence:** story-first, AI-actual worklog minutes, in-repo board is the live source of truth.
- **Governance rails:** synthetic data only; public Space runs $0/keyless; GitHub PAT requested only
  at push time (D9X-13); Watkins frameworks paraphrased with attribution.
