"""D9X-6 — Kai, the AI teammate (agent core).

Two abilities, both provenance-labelled (config.LABEL_*):
  answer(question)      shadow-mode Q&A: grounded in the index, cited, abstains
  attempt(task)         gated-phase scoped tasks: deterministic drafting backbone
                        per task class, with helpful-abstain escalation

$0 mode (no ANTHROPIC_API_KEY): everything below runs deterministically — the
public HuggingFace Space works keyless. With a key (local only), answer() adds a
Haiku synthesis pass over the retrieved passages; the deterministic backbone and
the citations never change.

The escalation contract ("raise your hand early"): when a task references a
system outside the glossary, or grounding is too weak, Kai does not guess — it
returns WHAT it tried, WHY it is stuck, and WHAT it needs.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field

import config
import generate_data


# ── Result envelope ───────────────────────────────────────────────────────────
@dataclass
class Output:
    text: str
    citations: list = field(default_factory=list)   # chunk ids like "runbook_x.md#2"
    label: str = config.LABEL_DETERMINISTIC
    abstained: bool = False
    escalation: str = ""                             # non-empty => needs a human
    acl_blocked: bool = False                        # refused on SCOPE, not on knowledge —
                                                     # an ACL refusal is NOT a knowledge gap


# ── Optional Haiku enrichment (local-key only; never on the public Space) ─────
def _haiku(prompt: str) -> str | None:
    key = config.get_key()
    if not key:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model=config.AI_MODEL, max_tokens=config.AI_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}])
        return msg.content[0].text.strip()
    except Exception:
        return None   # any API trouble degrades gracefully to the $0 path


class Teammate:
    """Kai. Holds the retrieval index + data-file paths; stateless otherwise —
    trust state lives on the board (board.py), not inside the agent."""

    def __init__(self, index):
        self.index = index

    # ── ACL: the charter's resource scopes, enforced (v2.0, D9X-20) ──────────
    def _acl_check(self, question: str) -> Output | None:
        if any(t in question.lower() for t in config.ACL_BLOCKED_TOPICS):
            return Output(
                text=("That topic is outside my resource scopes (least-privilege "
                      "charter: runbooks, backlog, recon figures, DQ rules — no HR "
                      "or compensation data). I can't retrieve it and won't guess; "
                      "please ask Daniel Osei (Engineering Manager)."),
                label=config.LABEL_ABSTAIN, abstained=True, acl_blocked=True,
                escalation="ACL: outside charter resource scopes — routed to a human, "
                           "by design (a badge, not the master key).")
        return None

    # ── Shadow mode: grounded Q&A ────────────────────────────────────────────
    def answer(self, question: str) -> Output:
        blocked = self._acl_check(question)
        if blocked:
            return blocked
        hits, abstained = self.index.grounded(question)
        if abstained:
            return Output(
                text=("I don't have grounding for that in the runbooks or coached Skills. "
                      "Rather than guess, I'm flagging it: if this is team knowledge, "
                      "coaching it in as a Skill will let me answer next time."),
                label=config.LABEL_ABSTAIN, abstained=True,
                escalation="No passage above the similarity floor — needs an SME or a Skill.")
        cites = [h[0] for h in hits]
        context = "\n\n---\n\n".join(f"[{h[0]}]\n{h[1]}" for h in hits)
        llm = _haiku(
            "Answer the team member's question STRICTLY from these passages; cite the "
            f"[chunk ids] you used; say so if they don't cover it.\n\n{context}\n\n"
            f"Question: {question}")
        if llm:
            return Output(text=llm, citations=cites, label=config.LABEL_LLM)
        # $0 extractive fallback: the retrieved passages verbatim — retrieval is the demo
        stitched = "\n\n".join(f"**[{h[0]}]** (score {h[2]:.2f})\n{h[1]}" for h in hits)
        return Output(text=stitched, citations=cites)

    # ── Gated phase: scoped task drafting (deterministic backbone) ────────────
    def attempt(self, task: dict) -> Output:
        return {
            "ticket_triage": self._triage,
            "recon_check": self._recon,
            "dq_rule_authoring": self._dq_rule,
        }[task["cls"]](task)

    def _escalate(self, tried: str, stuck: str, need: str) -> Output:
        msg = f"What I tried: {tried} Why I'm stuck: {stuck} What I need: {need}"
        return Output(text=msg, label=config.LABEL_ABSTAIN, abstained=True, escalation=msg)

    # triage: severity matrix from the runbook, applied deterministically
    def _triage(self, task: dict) -> Output:
        system = task.get("system", "")
        detail = task.get("detail", "").lower()
        cites = [h[0] for h in self.index.retrieve("severity matrix routing incident triage", 2)]
        if system not in generate_data.GLOSSARY_SYSTEMS:
            return self._escalate(
                f"Classifying '{task.get('title', task.get('detail', ''))}'.",
                f"'{system}' is not in the team glossary — the triage runbook says never "
                "guess a route for an unknown system.",
                "A human to confirm what feeds from this system, or a Skill documenting it.")
        if system == "RegReport" or "regulatory" in detail:
            sev, route, why = "SEV1", "Risk-Reg-Ops", "regulatory impact — regulatory beats everything"
        elif system == "RiskLens" or "dashboard" in detail or "internal report" in detail:
            sev, route, why = "SEV2", "Data-Engineering", "internal analytics impact, no regulatory exposure"
        elif any(w in detail for w in ("metadata", "description", "label", "cosmetic", "glossary")):
            sev, route, why = "SEV3", "Backlog", "cosmetic / metadata only"
        else:
            return self._escalate(
                "Applying the severity matrix.",
                "The ticket doesn't match any documented severity pattern.",
                "A human read on the impact before I route it.")
        return Output(
            text=(f"**Triage: {sev} → route to {route}.**\n\nRationale: {why} "
                  f"(system: {system}). Per the triage runbook, "
                  + ("notify Risk-Reg-Ops + on-call within 15 minutes."
                     if sev == "SEV1" else
                     "resolve within one business day." if sev == "SEV2" else
                     "fix in the next sprint.")),
            citations=cites)

    # recon: real arithmetic over recon_data.csv + the runbook's verdict rules
    def _recon(self, task: dict) -> Output:
        rows = {}
        with (config.DATA_DIR / "recon_data.csv").open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows[r["break_id"]] = r
        row = rows.get(task["break_id"])
        if row is None:
            return self._escalate(f"Looking up break {task['break_id']}.",
                                  "No figures exist for this break id.",
                                  "The recon extract for today.")
        gl, mart = float(row["gl_total"]), float(row["mart_total"])
        var_pct = abs(gl - mart) / gl * 100
        marker, days_over = row["marker"], int(row["consecutive_days_over"])
        cites = [h[0] for h in self.index.retrieve("reconciliation tolerance benign break verdict", 2)]
        if var_pct <= 0.5:
            verdict = "BENIGN"
            why = {"late_adj": "late-posted adjustments (self-corrects next load)",
                   "fx_reval": "month-end FX revaluation window"}.get(
                       marker, "within tolerance; no escalation needed")
        elif days_over >= 2:
            verdict, why = "BREACH", ("over tolerance for two consecutive days — escalate to "
                                      "Risk-Reg-Ops today with the variance history")
        else:
            verdict, why = "WATCH", "over tolerance for a single day — recheck tomorrow per runbook"
        return Output(
            text=(f"**Recon verdict: {verdict}** — {row['portfolio']}.\n\n"
                  f"Evidence: GL {gl:,.0f} vs mart {mart:,.0f} → variance {var_pct:.2f}% "
                  f"(tolerance 0.5%). {why.capitalize()}."),
            citations=cites)

    # dq rule: template from the runbook; the 2% CONVENTION only exists once coached
    def _dq_rule(self, task: dict) -> Output:
        cde, dim = task["cde"], task["dimension"]
        regulatory = task.get("regulatory", False)
        owner = "Risk-Reg-Ops" if regulatory else "Data-Engineering"
        cites = [h[0] for h in self.index.retrieve("DQ rule template threshold dimensions", 2)]
        if dim == "completeness":
            threshold = "2%" if self._skill_teaches_2pct() and regulatory else "5%"
            logic = f"null/missing rate of {cde} must stay below {threshold}"
            if threshold == "2%":
                cites = [h[0] for h in self.index.retrieve("completeness threshold convention regulatory", 2)]
        elif dim == "validity":
            logic, threshold = f"{cde} must be {task.get('constraint', 'within its documented domain')}", "0 violations"
        elif dim == "timeliness":
            logic, threshold = f"feed carrying {cde} must arrive by {task.get('deadline', 'its documented deadline')}", "0 late days"
        else:
            return self._escalate(f"Drafting a {dim} rule.",
                                  f"'{dim}' isn't a dimension in the DQ runbook.",
                                  "SME guidance on the intended check.")
        return Output(
            text=(f"**Draft DQ rule `DQ-{cde}-{dim}`** (needs SME sign-off before enabling)\n\n"
                  f"- CDE: {cde}\n- Dimension: {dim}\n- Logic: {logic}\n"
                  f"- Threshold: {threshold}\n- Owner / escalation: {owner}"),
            citations=cites)

    def _skill_teaches_2pct(self) -> bool:
        """True once the unwritten-rules Skill has been coached into the corpus."""
        return any("2%" in p.read_text(encoding="utf-8")
                   for p in config.SKILLS_DIR.glob("*.md"))

    # ── The knowledge miner (v2.0, D9X-18): Kai interviews the SME ────────────
    def interview_questions(self, gap) -> list[str]:
        """Turn an open knowledge gap into 2–3 SME interview questions.
        Deterministic $0 backbone; a local key lets Haiku sharpen the wording.
        This is the agent-led externalization loop: Kai asks, the human teaches,
        the answer becomes a cited, versioned Skill (board.author_skill)."""
        base = [
            (f'When I was asked "{gap.question}" I had no grounding in any '
             "runbook or Skill. What's the rule or context I'm missing?"),
            ("When does it apply - always, on specific days, at month-end - and "
             "who owns this knowledge today?"),
            ("What goes wrong if I follow only the documented runbooks here, and "
             "what should I do instead?"),
        ]
        llm = _haiku(
            "You are Kai, an AI teammate interviewing a human SME to capture "
            "undocumented team knowledge. Sharpen these three interview questions "
            "for this specific gap. Return exactly three lines, one question per "
            f"line, no numbering.\n\nGap: {gap.question}\n"
            f"My hypothesis: {gap.hypothesis}\n\n" + "\n".join(base))
        if llm:
            lines = [l.strip("-•0123456789. ").strip()
                     for l in llm.splitlines() if l.strip()]
            if len(lines) >= 3:
                return lines[:3]
        return base


def load_backlog() -> list[dict]:
    return json.loads((config.DATA_DIR / "backlog.json").read_text(encoding="utf-8"))
