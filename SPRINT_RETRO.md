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
