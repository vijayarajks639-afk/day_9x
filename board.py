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

import json
import shutil
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime

import config

# v2.0 registries (all under data/, reset with the coaching state)
SKILL_AUTHORS_PATH = config.DATA_DIR / "skill_authors.json"   # skill file -> who taught it
SME_CREDIT_PATH = config.DATA_DIR / "sme_credit.json"         # the hoarding→teaching flip
CONTRIB_LOG_PATH = config.DATA_DIR / "contribution_log.json"  # Kai's performance file


def _load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _save_json(path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


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
        log_contribution("escalation" if output.escalation else "draft", task["id"],
                         f"{'escalated' if output.escalation else 'drafted'}: {task['title']}"
                         if "title" in task else task["id"])
        return self.status[task["id"]]

    def review(self, task: dict, approved: bool) -> None:
        """The buddy's approval gate — the human judgement the whole model rests on."""
        self.status[task["id"]] = APPROVED if approved else REJECTED
        self.ledger.record_review(task["cls"], approved)
        log_contribution("approved" if approved else "rejected", task["id"],
                         f"buddy {'approved' if approved else 'sent back'} {task['id']}")

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
        _register_author("unwritten_rules.md", "Priya Raghavan", "coaching session")
        log_contribution("coaching", "unwritten_rules.md",
                         "Priya coached the unwritten rules into a Skill")
    index.reindex()
    return sorted(p.name for p in config.SKILLS_DIR.glob("*.md"))


def uncoach_all(index) -> None:
    """Reset the coaching (demo reset): remove coached Skills, their attribution
    and credit records, and reindex — back to the clean 'before' state."""
    for p in config.SKILLS_DIR.glob("*.md"):
        p.unlink()
    for p in (SKILL_AUTHORS_PATH, SME_CREDIT_PATH):
        if p.exists():
            p.unlink()
    index.reindex()


# ── The knowledge miner (v2.0, D9X-18): gap → interview → authored Skill ──────
def author_skill(index, gap, sme: str, answer: str) -> str:
    """Kai writes the SME's interview answer up as a versioned, ATTRIBUTED Skill,
    reindexes so it's immediately citable, closes the gap, and credits the SME.
    Attribution is the point: named credit is what flips knowledge hoarding into
    teaching (the SME is the teacher, never an extraction target)."""
    import gaps as gaps_mod
    fname = f"skill_{gaps_mod.slugify(gap.question)}.md"
    title = gap.question.strip().rstrip("?")
    body = (
        f"# Skill: {title}\n\n"
        f"*(Coached by **{sme}**, {date.today().isoformat()} — v1. Captured by Kai's "
        f"SME interview, source gap {gap.id}. This knowledge lived in a person's "
        f"head, not in any runbook.)*\n\n"
        f"## The rule\n{answer.strip()}\n\n"
        f"## Applies to\n{gap.question.strip()}\n"
    )
    (config.SKILLS_DIR / fname).write_text(body, encoding="utf-8")
    _register_author(fname, sme, f"Kai interview · {gap.id}")
    index.reindex()
    log_contribution("interview_skill", fname,
                     f"Kai interviewed {sme}; authored Skill for {gap.id}")
    return fname


def _register_author(fname: str, sme: str, source: str) -> None:
    authors = _load_json(SKILL_AUTHORS_PATH, {})
    authors[fname] = {"sme": sme, "date": date.today().isoformat(),
                      "version": 1, "source": source}
    _save_json(SKILL_AUTHORS_PATH, authors)
    credit = _load_json(SME_CREDIT_PATH, {})
    credit.setdefault(sme, {"skills": [], "citations": 0})
    if fname not in credit[sme]["skills"]:
        credit[sme]["skills"].append(fname)
    _save_json(SME_CREDIT_PATH, credit)


# ── SME credit ledger (v2.0, D9X-19): the hoarding→teaching flip, visible ─────
def credit_citations(citations: list[str]) -> None:
    """Every time a coached Skill is CITED in an answer, its teacher gets credit —
    'your knowledge answered N questions this sprint' is the incentive that
    counters the 35%-hoard instinct."""
    authors = _load_json(SKILL_AUTHORS_PATH, {})
    credit = _load_json(SME_CREDIT_PATH, {})
    changed = False
    for c in citations:
        fname = c.split("#")[0]
        if fname in authors:
            sme = authors[fname]["sme"]
            credit.setdefault(sme, {"skills": [], "citations": 0})
            credit[sme]["citations"] += 1
            changed = True
    if changed:
        _save_json(SME_CREDIT_PATH, credit)


def teachers_of_the_sprint() -> list[dict]:
    """Credit board rows, most-cited teacher first."""
    credit = _load_json(SME_CREDIT_PATH, {})
    rows = [{"SME": sme, "Skills coached": len(v["skills"]),
             "Citations served": v["citations"],
             "Skills": ", ".join(v["skills"])} for sme, v in credit.items()]
    return sorted(rows, key=lambda r: (-r["Citations served"], -r["Skills coached"]))


# ── Contribution log + retro artifacts (v2.0, D9X-22) ─────────────────────────
def log_contribution(kind: str, ref: str, summary: str) -> None:
    log = _load_json(CONTRIB_LOG_PATH, [])
    log.append({"ts": datetime.now().isoformat(timespec="seconds"),
                "kind": kind, "ref": ref, "summary": summary})
    _save_json(CONTRIB_LOG_PATH, log)


def contribution_log() -> list[dict]:
    return _load_json(CONTRIB_LOG_PATH, [])


def reset_logs() -> None:
    if CONTRIB_LOG_PATH.exists():
        CONTRIB_LOG_PATH.unlink()


def co_presentation() -> str:
    """The sprint-review co-presentation artifact (markdown): the human presents,
    Kai's contribution log is the evidence — the mixed-team ritual, made real."""
    log = contribution_log()
    counts = Counter(e["kind"] for e in log)
    lines = [
        "# Sprint Review — Co-presentation (buddy + Kai)",
        "",
        f"*Generated {date.today().isoformat()} from Kai's contribution log "
        f"({len(log)} entries). The human presents; this log is the evidence.*",
        "",
        "## Contribution summary",
        f"- Q&A answered (cited): **{counts.get('qa', 0)}**",
        f"- Task drafts submitted: **{counts.get('draft', 0)}** · approved: "
        f"**{counts.get('approved', 0)}** · sent back: **{counts.get('rejected', 0)}**",
        f"- Escalations (raised its hand): **{counts.get('escalation', 0)}**",
        f"- Knowledge gaps mined into Skills: **{counts.get('interview_skill', 0)}** "
        f"· coaching sessions: **{counts.get('coaching', 0)}**",
        "",
        "## The log",
        "| When | What | Ref | Summary |",
        "|---|---|---|---|",
    ]
    lines += [f"| {e['ts']} | {e['kind']} | `{e['ref']}` | {e['summary']} |"
              for e in log[-30:]]
    lines += ["", "---", f"*{config.WATKINS_CREDIT}*"]
    return "\n".join(lines)
