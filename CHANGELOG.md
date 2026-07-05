# Changelog — day_9x

All notable changes to the day_9x prototype. Versions follow the delivery decisions
recorded on the D9X board (`JIRA_STATUS.md`); v0.1 is frozen as tagged.

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
