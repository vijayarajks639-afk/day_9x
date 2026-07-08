"""D9X-17 — The knowledge-gap register (v2.0 "knowledge miner" substrate).

Every time Arjuna abstains or escalates, the moment is no longer lost: it is recorded
as a structured KNOWLEDGE GAP — a mining lead. The interview loop (agent.py +
board.py) turns an open gap into SME interview questions, an SME answer, and an
authored, attributed Skill; closing the gap makes the knowledge retrievable.

This is the POV's "our prototype opportunity" made concrete: agents notice corpus
gaps and schedule questions to humans (agent-led externalization — arXiv 2507.03811
reached 94.9% recall in simulation). Persisted to data/gaps.json so gaps survive
reruns; deterministic ids G-001, G-002, …
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import date

import config

GAPS_PATH = config.DATA_DIR / "gaps.json"

OPEN, INTERVIEWING, CLOSED = "open", "interviewing", "closed"


def slugify(text: str, max_len: int = 40) -> str:
    """A filesystem-safe slug for Skill filenames authored from a gap."""
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:max_len].rstrip("_") or "gap"


@dataclass
class Gap:
    id: str
    source: str                 # "qa" (shadow question) | "task" (backlog escalation)
    question: str               # what Arjuna was asked / asked to do
    hypothesis: str             # Arjuna's read on WHAT knowledge is missing (the escalation text)
    created: str = field(default_factory=lambda: date.today().isoformat())
    status: str = OPEN
    sme: str = ""               # who taught it (set on close)
    skill_file: str = ""        # the authored Skill (set on close)


class GapRegister:
    """File-backed register. record() dedupes on the normalized question so
    asking the same unanswerable thing twice stays ONE mining lead."""

    def __init__(self, path=GAPS_PATH):
        self.path = path
        self.gaps: list[Gap] = []
        self._load()

    # ── persistence ───────────────────────────────────────────────────────────
    def _load(self) -> None:
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.gaps = [Gap(**g) for g in raw]

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([asdict(g) for g in self.gaps], indent=2),
                             encoding="utf-8")

    # ── lifecycle ─────────────────────────────────────────────────────────────
    @staticmethod
    def _norm(q: str) -> str:
        return re.sub(r"\s+", " ", q.strip().lower())

    def record(self, question: str, hypothesis: str, source: str = "qa") -> Gap:
        for g in self.gaps:
            if self._norm(g.question) == self._norm(question):
                return g                                  # dedupe: one lead per question
        gap = Gap(id=f"G-{len(self.gaps) + 1:03d}", source=source,
                  question=question.strip(), hypothesis=hypothesis.strip())
        self.gaps.append(gap)
        self._save()
        return gap

    def open_gaps(self) -> list[Gap]:
        return [g for g in self.gaps if g.status != CLOSED]

    def get(self, gap_id: str) -> Gap | None:
        return next((g for g in self.gaps if g.id == gap_id), None)

    def mark_interviewing(self, gap_id: str) -> None:
        g = self.get(gap_id)
        if g and g.status == OPEN:
            g.status = INTERVIEWING
            self._save()

    def close(self, gap_id: str, sme: str, skill_file: str) -> None:
        g = self.get(gap_id)
        if g:
            g.status, g.sme, g.skill_file = CLOSED, sme, skill_file
            self._save()

    def reset(self) -> None:
        """Demo/test reset: forget all gaps."""
        self.gaps = []
        if self.path.exists():
            self.path.unlink()
