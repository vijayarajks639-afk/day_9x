"""D9X-5 — The Agent Charter: Five Conversations + STARS + sprint snapshot.

Framework adapted (paraphrased, with attribution) from Michael D. Watkins,
*The First 90 Days*: a new hire negotiates success with the boss through five
ongoing conversations — situation, expectations, style, resources, personal
development — anchored to a written 90-day plan agreed like a contract.

Here the "new hire" is an AI teammate, so each conversation becomes a concrete,
inspectable artefact: STARS diagnosis → onboarding pace; expectations → task
classes, eval thresholds and the stays-human list; style → escalation SLA;
resources → tool/data scopes (the MCP + ACL analogue); development → the
Skills-coaching plan.

The hiring manager ENTERS the onboarding duration (default 90 days) and gets a
sprint snapshot: 15-day sprints (90 → exactly 6) with phase focus + exit gates,
plus a stakeholder checkpoint report every 9 days (day_9x: x = 1..10).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import config

STAYS_HUMAN = [
    "Sign-off on anything entering RegReport or a regulatory submission",
    "Stakeholder communication and negotiation",
    "Ambiguous judgement calls (novel break patterns, unknown systems)",
    "Accountability — every Arjuna output has a named human owner",
]

RESOURCE_SCOPES = [
    ("Runbooks + coached Skills", "read", "the retrieval corpus (this demo's index)"),
    ("Backlog / ticket queue", "read + draft", "scoped items only; no self-assignment"),
    ("Recon figures (GL-Hub vs CreditMart)", "read", "metadata + totals; no row-level PII"),
    ("DQEngine rule registry", "draft only", "SME sign-off required to enable a rule"),
    ("Production systems", "none", "no write path exists — by design, not by promise"),
]


# ── Timeline math ─────────────────────────────────────────────────────────────
def phase_plan(duration: int, stars_key: str) -> dict:
    """Split the onboarding into SHADOW / GATED / AUTONOMOUS day-ranges.
    The STARS situation sets the fractions — a turnaround shortens shadow,
    a start-up stretches it (pace differs; the gates never disappear)."""
    s = config.STARS[stars_key]
    shadow_end = max(1, round(duration * s["shadow_frac"]))
    gated_end = min(duration, shadow_end + max(1, round(duration * s["gated_frac"])))
    return {
        "SHADOW": (1, shadow_end),
        "GATED": (shadow_end + 1, gated_end),
        "AUTONOMOUS": (gated_end + 1, duration),
    }


def checkpoints(duration: int) -> list[int]:
    """Stakeholder report days: 9, 18, ... — the 'x' in day_9x."""
    return list(range(config.CHECKPOINT_DAYS, duration + 1, config.CHECKPOINT_DAYS))


_EXIT_GATES = {
    "SHADOW": "Exit gate: baseline eval pass on runbook Q&A; charter signed; first Skills coached.",
    "GATED": "Exit gate: per-class approval rate at threshold; escalation behaviour verified "
             "(does it raise its hand early?).",
    "AUTONOMOUS": "Exit gate: probation review — eval gates green per class; "
                  "expand / hold / reduce decision recorded.",
}
_FOCUS = {
    "SHADOW": "Shadow mode — read-only; drafts only; 100% review; build Skills from team knowledge",
    "GATED": "Scoped early wins — 4–8h verifiable tasks behind approval gates; attribution on everything",
    "AUTONOMOUS": "Graduated autonomy — unlocked per task class that passes its evals; audit sampling",
}


def sprint_snapshot(duration: int, stars_key: str) -> list[dict]:
    """The hiring manager's one-glance plan: one row per 15-day sprint,
    labelled by the dominant phase, with checkpoints falling inside it."""
    phases = phase_plan(duration, stars_key)
    cps = checkpoints(duration)
    sprints = []
    n, day = 1, 1
    while day <= duration:
        end = min(day + config.SPRINT_DAYS - 1, duration)
        # dominant phase = the one covering most days of this sprint
        overlap = {ph: max(0, min(end, hi) - max(day, lo) + 1)
                   for ph, (lo, hi) in phases.items()}
        dom = max(overlap, key=overlap.get)
        sprints.append({
            "sprint": n,
            "days": f"{day}–{end}",
            "phase": dom,
            "focus": _FOCUS[dom],
            "exit_gate": _EXIT_GATES[dom],
            "checkpoints": [c for c in cps if day <= c <= end],
        })
        n, day = n + 1, end + 1
    return sprints


# ── The charter itself ────────────────────────────────────────────────────────
@dataclass
class Charter:
    stars_key: str = config.DEFAULT_STARS
    duration: int = config.DEFAULT_DURATION_DAYS
    escalation_sla: str = ("Raise blockers within one task attempt — silent struggling is the "
                           "one firing offence. Escalations state: what I tried, why I'm stuck, "
                           "what I need.")
    stays_human: list = field(default_factory=lambda: list(STAYS_HUMAN))

    def five_conversations(self) -> dict[str, str]:
        """The five conversations, each rendered as a charter section (markdown)."""
        s = config.STARS[self.stars_key]
        phases = phase_plan(self.duration, self.stars_key)
        expectations = "\n".join(
            f"- **{c['label']}** — {c['desc']} Autonomy gate: eval pass-rate ≥ "
            f"{c['pass_rate']:.0%} and ≥ {c['min_verified']} verified outputs."
            for c in config.TASK_CLASSES.values())
        stays = "\n".join(f"- {x}" for x in self.stays_human)
        resources = "\n".join(f"- **{name}** — access: *{mode}* ({why})"
                              for name, mode, why in RESOURCE_SCOPES)
        return {
            "1 · Situation": (
                f"**STARS diagnosis:** {s['label']}.\n\n{s['note']}\n\n"
                f"Onboarding pace: SHADOW days {phases['SHADOW'][0]}–{phases['SHADOW'][1]}, "
                f"GATED days {phases['GATED'][0]}–{phases['GATED'][1]}, "
                f"AUTONOMOUS days {phases['AUTONOMOUS'][0]}–{phases['AUTONOMOUS'][1]}."),
            "2 · Expectations": (
                f"Task classes in scope, with promotion gates (evals, not vibes):\n\n{expectations}\n\n"
                f"**Stays human — written down, not implied:**\n{stays}"),
            "3 · Style": (
                f"All outputs carry a provenance label (deterministic / AI-suggestion / abstained). "
                f"Named buddy reviews everything until gates relax.\n\n**Escalation SLA:** "
                f"{self.escalation_sla}"),
            "4 · Resources": (
                f"Least-privilege scopes (the MCP + ACL analogue — a badge, not the master key):\n\n"
                f"{resources}"),
            "5 · Development": (
                "Coaching an AI teammate is explicit work: retros name what it did well and where it "
                "flailed; SMEs encode 'how we really do it here' as versioned **Skills**, which join "
                "the corpus on reindex. The Skill history *is* the coaching record."),
        }

    def render_markdown(self) -> str:
        parts = [f"# Agent Charter — Arjuna (AI teammate)\n",
                 f"*Onboarding duration: **{self.duration} days** · "
                 f"{len(sprint_snapshot(self.duration, self.stars_key))} sprints · "
                 f"{len(checkpoints(self.duration))} stakeholder checkpoints*\n"]
        for title, body in self.five_conversations().items():
            parts.append(f"## {title}\n\n{body}\n")
        parts.append(f"---\n*{config.WATKINS_CREDIT}*")
        return "\n".join(parts)
