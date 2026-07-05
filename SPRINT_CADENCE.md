# Sprint Cadence — day_9x

How the onboarding programme is paced. Two clocks run at once — **15-day sprints** pace the work;
**9-day day-9x checkpoints** pace stakeholder communication — and they share the day-90 endpoint.
Everything here re-derives from `config.py` (`SPRINT_DAYS=15`, `CHECKPOINT_DAYS=9`) and
`charter.py`, so changing the hiring manager's duration changes this whole picture live.

---

## The default 90-day programme (STARS = Turnaround)

```
Day:   1        15        30        45        60        75        90
       |--------|--------|--------|--------|--------|--------|
Sprint    S1       S2       S3       S4       S5       S6
Phase   SHADOW  |========= GATED =========|===== AUTONOMOUS =====|
9x       x1,x2  | x2..x4    |  x5,x6  | x7,x8  | x9    | x10
```

- **6 sprints** (15 days each). **10 day-9x checkpoints** (days 9, 18, … 90).
- Phase boundaries move with the **STARS** situation: a *turnaround* shortens SHADOW (fast into
  scoped work); a *start-up* lengthens it (heavy learning first). The gates never disappear —
  only the pace changes.

## Per-sprint focus + exit gates

| Sprint | Days | Dominant phase | Focus | Exit gate |
|---|---|---|---|---|
| S1 | 1–15 | SHADOW | Read-only; drafts only; 100% review; build first Skills from team knowledge | Baseline eval pass on runbook Q&A; charter signed; first Skills coached |
| S2 | 16–30 | GATED | Scoped 4–8h early wins behind approval gates; attribution on everything | Per-class approval rate at threshold; escalation behaviour verified |
| S3 | 31–45 | GATED | Widen task classes; weekly retro reviews agent contribution log | Same gate, more classes green |
| S4 | 46–60 | GATED→AUTONOMOUS | First classes that pass evals unlock autonomy; others stay gated | Eval gate green per unlocked class |
| S5 | 61–75 | AUTONOMOUS | Autonomy within charter; audit sampling (~20%) | Audit sample clean; rework % trending down |
| S6 | 76–90 | AUTONOMOUS | Steady state; prep the probation review | **Probation review**: expand / hold / reduce, recorded |

*(Ranges shift for non-turnaround STARS — the app's Charter tab shows the exact snapshot.)*

## Ceremonies

| Ceremony | Cadence | Output |
|---|---|---|
| Daily stand-up | 09:30 daily | blockers surfaced early; escalations logged |
| **Day-9x checkpoint report** | every 9 days | 6–8 line stakeholder note: outputs verified, escalations, analyst-hours consumed/created, cumulative net, breakeven status |
| Sprint review + retro | end of each 15-day sprint | demo increment; inspect + adapt |
| Probation review | day 90 | eval-gated autonomy decision per task class |

## The two build sprints (how the prototype itself was made)

We ran the same shape to build the tool (dogfooding the cadence):

- **Build Sprint 1 — the engine (D9X-2…D9X-8):** config contract, synthetic world, RAG,
  charter, agent, board, evals. Exit gate: `python evals.py` behaves as designed
  (2 culture reds uncoached → all green coached).
- **Build Sprint 2 — story & ship (D9X-9…D9X-15):** breakeven ledger, Streamlit app, tests,
  docs, deploy prep, stakeholder deck. Exit gate: 15/15 tests green; app boots $0/keyless.

Blocked on external credentials (a human action, by design): **D9X-13** GitHub push (PAT at
push time), **D9X-14** HF Space deploy (HF token).

## What "done" means each checkpoint (Definition of Done)

Peer-reviewed, evidence attached (citations / eval run / recon arithmetic), incident & ticket
logs updated, no open DQ breaches, provenance label on every surfaced output.
