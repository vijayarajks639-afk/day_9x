"""D9X-7 — The task board, approval gates, and the coaching loop.

The accountability structure that makes an agent a TEAMMATE instead of a tool:
a task moves todo → drafted → (approved | rejected | escalated); every approval
or rejection updates the per-class trust ledger; and "coach" is the explicit act
of an SME writing cultural knowledge into data/skills/ so it enters the corpus
on reindex.

Trust is per task class and evidence-based (statistical, never social):
  SHADOW      drafts only, 100% reviewed
  GATED       unlocked when the class passes its eval gate (evals.py)
  AUTONOMOUS  offered when the gate holds AND enough gated outputs were verified
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field

import config


# ── Trust ledger ──────────────────────────────────────────────────────────────
@dataclass
class TrustLedger:
    """Per-class trust state + the evidence behind it."""
    state: dict = field(default_factory=lambda: {c: config.SHADOW for c in config.TASK_CLASSES})
    verified: dict = field(default_factory=lambda: {c: 0 for c in config.TASK_CLASSES})
    rejected: dict = field(default_factory=lambda: {c: 0 for c in config.TASK_CLASSES})
    eval_rate: dict = field(default_factory=lambda: {c: None for c in config.TASK_CLASSES})

    def record_review(self, cls: str, approved: bool) -> None:
        (self.verified if approved else self.rejected)[cls] = \
            (self.verified if approved else self.rejected)[cls] + 1

    def record_eval(self, cls: str, rate: float) -> None:
        self.eval_rate[cls] = rate
        spec = config.TASK_CLASSES[cls]
        if rate >= spec["pass_rate"] and self.state[cls] == config.SHADOW:
            self.state[cls] = config.GATED

    def autonomy_ready(self, cls: str) -> bool:
        """AUTONOMOUS is OFFERED on evidence; a human still flips the switch."""
        spec = config.TASK_CLASSES[cls]
        return (self.state[cls] == config.GATED
                and (self.eval_rate[cls] or 0) >= spec["pass_rate"]
                and self.verified[cls] >= spec["min_verified"])

    def promote(self, cls: str) -> bool:
        if self.autonomy_ready(cls):
            self.state[cls] = config.AUTONOMOUS
            return True
        return False

    def demote(self, cls: str) -> None:
        """The probation review can also HOLD or REDUCE — trust is revocable."""
        self.state[cls] = config.GATED if self.state[cls] == config.AUTONOMOUS else config.SHADOW


# ── Task board ────────────────────────────────────────────────────────────────
TODO, DRAFTED, APPROVED, REJECTED, ESCALATED = "todo", "drafted", "approved", "rejected", "escalated"


@dataclass
class Board:
    tasks: list                                  # backlog dicts (generate_data.BACKLOG shape)
    ledger: TrustLedger = field(default_factory=TrustLedger)
    status: dict = field(default_factory=dict)   # task id -> lifecycle state
    drafts: dict = field(default_factory=dict)   # task id -> agent Output

    def __post_init__(self):
        for t in self.tasks:
            self.status.setdefault(t["id"], TODO)

    def submit_draft(self, task: dict, output) -> str:
        """Kai hands in work. Escalations short-circuit the gate — that IS the
        desired behaviour, so they never count against trust."""
        self.drafts[task["id"]] = output
        self.status[task["id"]] = ESCALATED if output.escalation else DRAFTED
        return self.status[task["id"]]

    def review(self, task: dict, approved: bool) -> None:
        """The buddy's approval gate — the human judgement the whole model rests on."""
        self.status[task["id"]] = APPROVED if approved else REJECTED
        self.ledger.record_review(task["cls"], approved)

    def counts(self) -> dict:
        out = {s: 0 for s in (TODO, DRAFTED, APPROVED, REJECTED, ESCALATED)}
        for s in self.status.values():
            out[s] += 1
        return out


# ── Coaching (the Watkins development conversation, made concrete) ────────────
def coach_unwritten_rules(index) -> list[str]:
    """An SME promotes data/coaching/unwritten_rules.md into data/skills/ and the
    index is rebuilt — cultural knowledge becomes retrievable, versioned, and
    citable. Returns the list of coached Skill filenames."""
    src = config.DATA_DIR / "coaching" / "unwritten_rules.md"
    dst = config.SKILLS_DIR / "unwritten_rules.md"
    if src.exists() and not dst.exists():
        shutil.copyfile(src, dst)
    index.reindex()
    return sorted(p.name for p in config.SKILLS_DIR.glob("*.md"))


def uncoach_all(index) -> None:
    """Reset the coaching (demo reset): remove coached Skills and reindex."""
    for p in config.SKILLS_DIR.glob("*.md"):
        p.unlink()
    index.reindex()
