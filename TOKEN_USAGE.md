# Token Usage Ledger — day_9x

Per-sprint token accounting for **all agents** (orchestrator + partner subagents), started at
Build Sprint 3 per the team cadence (tracking was not yet in place for Sprints 1–2 / v0.1).
Figures marked **(est.)** are conservative orchestrator estimates — the harness does not expose
the orchestrator's own exact meter; subagent figures are taken from harness completion reports
where available. Update live, never batch-log.

## Build Sprint 3 — v2.0 "the knowledge miner" (D9X-16…D9X-20)

| Agent | Role | Model | Input tokens | Output tokens | Status |
|---|---|---|---|---|---|
| Orchestrator | gap analysis, plan, freeze, engine code (gaps/rag/agent/board), app, board upkeep | Fable 5 | ~250k (est., incl. re-read of POV/EVIDENCE + full source read) | ~35k (est.) | in progress |
| Docs partner | DEMO_WALKTHROUGH v2 · SPRINT_RETRO v2 · JIRA_IMPORT.csv append | Opus 4.8 | 68,166 total (harness-reported; 14 tool uses, 3m19s) | included in total | ✅ done |

## Build Sprint 4 — v2.0 "one team" & ship (D9X-21…D9X-26)

| Agent | Role | Model | Input tokens | Output tokens | Status |
|---|---|---|---|---|---|
| Orchestrator | team impact, retro artifacts, tests, evals, deck v2, board upkeep, verification, review-fix application | Fable 5 / Opus 4.8 | ~140k (est., incremental over cached context) | ~25k (est.) | ✅ done |
| Review partner | independent v2.0 audit → REVIEW_v2.md (D9X-26) | Opus 4.8 | 137,632 total (harness-reported; 26 tool uses) | included in total | ✅ done |

## Reporting snapshot (for the summary)
- **Partner subagents:** docs partner **68,166 tokens** (14 tool uses, 3m19s, ✅);
  review partner **137,632 tokens** (26 tool uses, ✅). Partner total ≈ **205,798 tokens**.
- **Orchestrator (est.):** ~410k input / ~60k output across Sprints 3–4 — dominated by the
  one-time re-read of the POV/EVIDENCE dossier + full v0.1 source at the start of Sprint 3;
  incremental turns run on warm cache. Includes applying the review's fixes (M1 gap-seed +
  app copy, m1 label, m2 boot reset, n1 ASCII) and re-verification.
- These are best-effort figures; the harness reports exact totals only for subagents on
  completion. **Grand total (all agents, Sprints 3–4): ≈ 616k input / ≈ 65k output**, dominated
  by the one-time dossier re-read; the app itself remains $0/keyless at runtime.

## Notes
- v0.1 (Sprints 1–2) predates this ledger; its effort is recorded as AI-actual **minutes** in
  `JIRA_STATUS.md` (~410 min) — going forward both minutes and tokens are kept.
- Cost guardrail unchanged: the app itself runs **$0/keyless**; Haiku enrichment is local-key
  only and never part of the public deploy.
