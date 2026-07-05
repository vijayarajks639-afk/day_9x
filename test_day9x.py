"""D9X-11 — Unit tests for day_9x. Run: python -m pytest test_day9x.py -q

Covers the load-bearing claims: sprint math (90 days = 6 sprints, 10 checkpoints),
STARS pacing, the deterministic agent backbone, the escalation contract, the trust
state machine, the coaching→retrieval loop, and the breakeven ledger.
"""
from __future__ import annotations

import pytest

import config
import generate_data
import charter
import breakeven as be


@pytest.fixture(scope="session")
def world():
    generate_data.ensure_generated(force=True)


@pytest.fixture(scope="session")
def index(world):
    import rag
    return rag.Index().build()


@pytest.fixture(scope="session")
def kai(index):
    from agent import Teammate
    return Teammate(index)


# ── Charter / sprint math ─────────────────────────────────────────────────────
def test_default_90_is_six_sprints_ten_checkpoints():
    snap = charter.sprint_snapshot(90, "Turnaround")
    assert len(snap) == 6
    assert charter.checkpoints(90) == [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]


def test_duration_rederives_snapshot():
    assert len(charter.sprint_snapshot(30, "Turnaround")) == 2
    assert len(charter.checkpoints(45)) == 5


def test_stars_changes_pace_not_gates():
    fast = charter.phase_plan(90, "Turnaround")["SHADOW"][1]
    slow = charter.phase_plan(90, "Start-up")["SHADOW"][1]
    assert slow > fast                      # start-up shadows longer than a turnaround
    for key in config.STARS:                # every situation still has all three phases
        ph = charter.phase_plan(90, key)
        assert set(ph) == {"SHADOW", "GATED", "AUTONOMOUS"}


def test_charter_has_five_conversations():
    c = charter.Charter()
    convos = c.five_conversations()
    assert len(convos) == 5
    assert any("stays human" in v.lower() for v in convos.values())


# ── Agent backbone (deterministic $0 path) ────────────────────────────────────
def test_triage_regulatory_is_sev1(kai):
    t = {"cls": "ticket_triage", "id": "x", "system": "RegReport", "detail": "nulls in feed"}
    out = kai.attempt(t)
    assert "SEV1" in out.text and "Risk-Reg-Ops" in out.text and not out.abstained


def test_triage_unknown_system_escalates(kai):
    t = {"cls": "ticket_triage", "id": "x", "system": "OrionLedger", "detail": "late batch"}
    out = kai.attempt(t)
    assert out.escalation and out.abstained            # raises its hand, does not guess


def test_recon_arithmetic_and_verdicts(kai):
    assert "BENIGN" in kai.attempt({"cls": "recon_check", "id": "x", "break_id": "R-201"}).text
    assert "BREACH" in kai.attempt({"cls": "recon_check", "id": "x", "break_id": "R-202"}).text
    assert "WATCH" in kai.attempt({"cls": "recon_check", "id": "x", "break_id": "E-R3"}).text


def test_abstain_on_out_of_scope(kai):
    assert kai.answer("Who won the football world cup?").abstained


def test_answer_cites_source(kai):
    out = kai.answer("What severity is a RegReport incident and where does it route?")
    assert not out.abstained and out.citations
    assert "SEV1" in out.text and "Risk-Reg-Ops" in out.text


# ── The coaching → retrieval loop (the core teaching moment) ───────────────────
def test_culture_needs_coaching(index, kai):
    # Uncoached, Kai can't answer the Thursday rule — it isn't in any runbook, so the
    # answer never mentions Thursday (it retrieves the nearest doc instead). This is the
    # failure the EVAL catches (missing token), the honest teaching moment. Coaching the
    # Skill puts the rule in the corpus, and the answer then cites it.
    import board
    board.uncoach_all(index)
    q = "Can I rerun the CreditMart load on Thursday morning?"
    assert "Thursday" not in kai.answer(q).text        # no grounding for the rule
    board.coach_unwritten_rules(index)
    out = kai.answer(q)
    assert "Thursday" in out.text and any("unwritten" in c for c in out.citations)
    board.uncoach_all(index)


def test_dq_rule_convention_flips_after_coaching(index, kai):
    import board
    board.uncoach_all(index)
    t = {"cls": "dq_rule_authoring", "id": "x", "cde": "lgd",
         "dimension": "completeness", "regulatory": True}
    assert "5%" in kai.attempt(t).text          # documented default before coaching
    board.coach_unwritten_rules(index)
    assert "2%" in kai.attempt(t).text          # team convention after coaching
    board.uncoach_all(index)


# ── Trust state machine ───────────────────────────────────────────────────────
def test_trust_promotes_only_on_evidence():
    from board import TrustLedger
    tl = TrustLedger()
    assert tl.state["ticket_triage"] == config.SHADOW
    tl.record_eval("ticket_triage", 0.90)                  # passes gate -> GATED
    assert tl.state["ticket_triage"] == config.GATED
    assert not tl.autonomy_ready("ticket_triage")          # no verified outputs yet
    for _ in range(config.TASK_CLASSES["ticket_triage"]["min_verified"]):
        tl.record_review("ticket_triage", True)
    assert tl.autonomy_ready("ticket_triage") and tl.promote("ticket_triage")
    assert tl.state["ticket_triage"] == config.AUTONOMOUS
    tl.demote("ticket_triage")                             # trust is revocable
    assert tl.state["ticket_triage"] == config.GATED


def test_failing_gate_blocks_promotion():
    from board import TrustLedger
    tl = TrustLedger()
    tl.record_eval("dq_rule_authoring", 0.50)              # below gate
    assert tl.state["dq_rule_authoring"] == config.SHADOW
    assert not tl.autonomy_ready("dq_rule_authoring")


# ── Breakeven ledger ──────────────────────────────────────────────────────────
def test_simulation_is_deterministic_and_reaches_breakeven():
    e1 = be.simulate(90, "Turnaround")
    e2 = be.simulate(90, "Turnaround")
    assert [x.__dict__ for x in e1] == [x.__dict__ for x in e2]   # seeded
    daily = be.ledger(e1)
    assert be.breakeven_day(daily) is not None                    # net turns positive
    assert daily["cum_net"].iloc[-1] > 0


def test_checkpoint_report_renders():
    e = be.simulate(90, "Turnaround")
    rpt = be.checkpoint_report(e, 90, 90, "Turnaround")
    assert "day-9x" in rpt.lower() and "analyst-hours" in rpt
