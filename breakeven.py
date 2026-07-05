"""D9X-9 — The breakeven ledger + day-9x checkpoint reports.

The demo's headline metric, adapted with attribution from Watkins' breakeven-point
idea: a new hire consumes value before creating it. For an AI teammate both sides
are measurable in analyst-minutes:

  CONSUMED  review minutes on drafts (shadow/gated), coaching minutes when an SME
            writes a Skill, eval-review minutes, audit minutes once autonomous
  CREATED   the analyst baseline-minutes of every output that a human verified
            (or that passed audit once autonomous) — value counts only when checked

simulate() produces a deterministic, seeded "fast-forward" of a plausible run so
the public demo can show a full curve instantly; the interactive tabs add real
entries on top. Checkpoint reports summarise every 9 days — the 'x' in day_9x.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd

import config
import charter

COACH_MINUTES = 45          # one SME coaching session -> one written Skill
EVAL_REVIEW_MINUTES = 30    # human time to review one probation-review eval run
ESCALATION_MINUTES = 5      # human time to pick up a well-formed escalation


@dataclass
class Entry:
    day: int
    cls: str          # task class, or "coaching"/"evals"
    kind: str         # qa | task | autonomous | escalated | rejected | coaching | evals
    consumed: float   # analyst-minutes spent on Kai
    created: float    # analyst-minutes Kai's verified output saved
    note: str = ""


# ── Ledger math ───────────────────────────────────────────────────────────────
def ledger(entries: list[Entry]) -> pd.DataFrame:
    """Per-day totals + cumulative net (created − consumed), in analyst-hours."""
    if not entries:
        return pd.DataFrame(columns=["day", "consumed", "created", "net", "cum_net"])
    df = pd.DataFrame([e.__dict__ for e in entries])
    daily = df.groupby("day")[["consumed", "created"]].sum().reset_index()
    daily["net"] = daily["created"] - daily["consumed"]
    daily["cum_net"] = daily["net"].cumsum()
    for col in ("consumed", "created", "net", "cum_net"):
        daily[col] = daily[col] / 60.0   # minutes -> hours
    return daily


def breakeven_day(daily: pd.DataFrame) -> int | None:
    """First day the cumulative net turns non-negative (Watkins' breakeven point)."""
    hit = daily[daily["cum_net"] >= 0]
    return None if hit.empty else int(hit.iloc[0]["day"])


# ── Deterministic fast-forward simulation ─────────────────────────────────────
def simulate(duration: int = config.DEFAULT_DURATION_DAYS,
             stars_key: str = config.DEFAULT_STARS) -> list[Entry]:
    """A scripted, seeded, PLAUSIBLE run — labelled as simulation in the UI.
    Follows the charter's phase plan: shadow Q&A with 100% review, a coaching
    event mid-shadow, gated tasks with ramping approval, eval runs at the phase
    boundaries, then autonomous throughput with audit sampling."""
    rng = random.Random(config.SEED)
    phases = charter.phase_plan(duration, stars_key)
    (sh_lo, sh_hi), (g_lo, g_hi), (a_lo, a_hi) = (
        phases["SHADOW"], phases["GATED"], phases["AUTONOMOUS"])
    coach_day = max(sh_lo, sh_lo + int((sh_hi - sh_lo) * 0.6))
    qa = config.TASK_CLASSES["runbook_qa"]
    gated_classes = ["ticket_triage", "recon_check", "dq_rule_authoring"]
    entries: list[Entry] = []

    for day in range(1, duration + 1):
        if day <= sh_hi:                                   # ── shadow phase (pure investment)
            for _ in range(rng.choice((1, 1, 2))):
                ok = rng.random() < (0.97 if day > coach_day else 0.88)
                # drafts only: the human still owns the output, so realized value = 0.
                # Shadow mode is the onboarding COST — the dip before the breakeven climb.
                entries.append(Entry(day, "runbook_qa", "qa",
                                     consumed=qa["review_minutes"], created=0,
                                     note="draft reviewed (human still owns it)"
                                     if ok else "sent back"))
            if day == coach_day:
                entries.append(Entry(day, "coaching", "coaching", COACH_MINUTES, 0,
                                     "SME encodes the unwritten rules as a Skill"))
            if day == sh_hi:
                entries.append(Entry(day, "evals", "evals", EVAL_REVIEW_MINUTES, 0,
                                     "baseline eval — shadow exit gate"))
        elif day <= g_hi:                                  # ── gated phase
            ramp = (day - g_lo) / max(1, g_hi - g_lo)      # approval 0.80 -> 0.95
            for _ in range(2):
                cls = rng.choice(gated_classes)
                spec = config.TASK_CLASSES[cls]
                r = rng.random()
                if r < 0.05:
                    entries.append(Entry(day, cls, "escalated", ESCALATION_MINUTES, 0,
                                         "raised its hand early — desired behaviour"))
                elif r < 0.05 + (0.95 - (0.80 + 0.15 * ramp)):
                    entries.append(Entry(day, cls, "rejected", spec["review_minutes"], 0,
                                         "buddy sent the draft back"))
                else:
                    entries.append(Entry(day, cls, "task", spec["review_minutes"],
                                         spec["baseline_minutes"], "approved at the gate"))
            if day == g_hi:
                entries.append(Entry(day, "evals", "evals", EVAL_REVIEW_MINUTES, 0,
                                     "probation review — autonomy decision"))
        else:                                              # ── autonomous phase
            for _ in range(3):
                cls = rng.choice(gated_classes + ["runbook_qa"])
                spec = config.TASK_CLASSES[cls]
                audited = rng.random() < config.AUDIT_SAMPLE_RATE
                entries.append(Entry(
                    day, cls, "autonomous",
                    consumed=spec["audit_minutes"] if audited else 0,
                    created=spec["baseline_minutes"],
                    note="audit sample" if audited else "autonomous within charter"))
    return entries


# ── Day-9x checkpoint reports ─────────────────────────────────────────────────
def checkpoint_report(entries: list[Entry], day: int, duration: int,
                      stars_key: str) -> str:
    """The 9-day stakeholder report (markdown) as of a checkpoint day."""
    upto = [e for e in entries if e.day <= day]
    window = [e for e in entries if day - config.CHECKPOINT_DAYS < e.day <= day]
    daily = ledger(upto)
    be = breakeven_day(daily)
    cum = float(daily["cum_net"].iloc[-1]) if not daily.empty else 0.0
    phases = charter.phase_plan(duration, stars_key)
    phase = next(ph for ph, (lo, hi) in phases.items() if lo <= day <= hi)
    x = day // config.CHECKPOINT_DAYS

    def n(kind):
        return sum(1 for e in window if e.kind == kind)

    lines = [
        f"### Day-9x checkpoint · x={x} (day {day} of {duration}) — phase: {phase}",
        "",
        f"- Outputs verified this window: **{n('task') + n('qa')}** · "
        f"autonomous: **{n('autonomous')}** · sent back: **{n('rejected')}** · "
        f"escalations (desired behaviour): **{n('escalated')}**",
        f"- Analyst-hours this window: consumed "
        f"**{sum(e.consumed for e in window) / 60:.1f}h**, created "
        f"**{sum(e.created for e in window) / 60:.1f}h**",
        f"- Cumulative net position: **{cum:+.1f} analyst-hours**",
        f"- Breakeven: " + (f"**reached day {be}**" if be is not None and be <= day
                            else "not yet — still an investment, as any new hire is"),
    ]
    return "\n".join(lines)
