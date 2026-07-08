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
    # Uncoached, Arjuna can't answer the Thursday rule — it isn't in any runbook, so the
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


# ── v2.0 · the knowledge miner (gap register → interview → authored Skill) ────
def test_gap_register_records_and_dedupes(tmp_path):
    import gaps
    reg = gaps.GapRegister(path=tmp_path / "gaps.json")
    g1 = reg.record("Can I load vendor files on the 1st?", "no grounding")
    g2 = reg.record("  can i load vendor files on the 1st?", "still nothing")
    assert g1.id == "G-001" and g2.id == g1.id            # dedupe on the question
    assert len(reg.open_gaps()) == 1
    assert gaps.GapRegister(path=tmp_path / "gaps.json").gaps[0].id == "G-001"  # persisted


def test_interview_roundtrip_authors_cited_skill(index, kai, tmp_path):
    import board
    import gaps
    board.uncoach_all(index)
    q = "Can vendor reference files be loaded on the first business day of the month?"
    before = kai.answer(q)
    assert "11:00" not in before.text                     # the rule exists nowhere yet
    reg = gaps.GapRegister(path=tmp_path / "gaps.json")
    gap = reg.record(q, before.escalation or "answered without the actual rule")
    qs = kai.interview_questions(gap)
    assert len(qs) == 3 and any("missing" in x.lower() or "rule" in x.lower() for x in qs)
    fname = board.author_skill(
        index, gap, "Arun Verma",
        "Never load vendor reference files on the first business day of the month — "
        "vendors restate prices overnight; wait for the second run at 11:00.")
    reg.close(gap.id, "Arun Verma", fname)
    assert reg.get(gap.id).status == "closed"
    after = kai.answer(q)
    assert not after.abstained and any(fname in c for c in after.citations)
    assert "11:00" in after.text                          # mined knowledge now serves
    board.uncoach_all(index)


def test_sme_credit_ledger_flips_hoarding_to_teaching(index, tmp_path):
    import board
    import gaps
    board.uncoach_all(index)
    reg = gaps.GapRegister(path=tmp_path / "g.json")
    gap = reg.record("What is the vendor file cutover rule?", "no grounding")
    fname = board.author_skill(index, gap, "Sofia Lindqvist",
                               "Cutover happens on the 11:00 second run.")
    sofia = next(r for r in board.teachers_of_the_sprint() if r["SME"] == "Sofia Lindqvist")
    assert sofia["Skills coached"] == 1 and sofia["Citations served"] == 0
    board.credit_citations([f"{fname}#0", "runbook_dq_rules.md#1"])   # only Skills credit
    sofia = next(r for r in board.teachers_of_the_sprint() if r["SME"] == "Sofia Lindqvist")
    assert sofia["Citations served"] == 1
    board.uncoach_all(index)


# ── v2.0 · ACL + freshness realism ────────────────────────────────────────────
def test_acl_scope_refusal(kai):
    out = kai.answer("What is the salary band for the Senior Data Engineer role?")
    assert out.abstained and out.acl_blocked
    assert "scope" in out.escalation.lower() and not out.citations


def test_superseded_runbook_excluded_from_retrieval(index, kai):
    assert "runbook_escalation_contacts_2025.md" in index.superseded
    assert not any(i.startswith("runbook_escalation_contacts_2025") for i in index.ids)
    out = kai.answer("Where do I raise the escalation for a reconciliation BREACH "
                     "per the escalation contacts runbook?")
    assert "RRO-1" in out.text
    assert any("escalation_contacts_2026" in c for c in out.citations)
    assert not any("escalation_contacts_2025" in c for c in out.citations)


# ── v2.0 · team impact + retro artifacts ──────────────────────────────────────
def test_team_impact_returns_hours_per_human():
    rows = be.team_impact(be.simulate(90, "Turnaround"))
    assert {r["Who"] for r in rows} >= {"Priya Raghavan", "Arun Verma", "Sofia Lindqvist"}
    assert sum(r["Hours returned"] for r in rows) > 0
    assert all("Before Arjuna (doer)" in r and "With Arjuna (reviewer)" in r for r in rows)


def test_contribution_log_and_copresentation(world):
    import board
    board.reset_logs()
    board.log_contribution("qa", "shadow", "answered: test question")
    board.log_contribution("escalation", "T-104", "escalated: unknown system")
    log = board.contribution_log()
    assert len(log) == 2 and log[0]["kind"] == "qa"
    md = board.co_presentation()
    assert "Co-presentation" in md and "T-104" in md and "Escalations" in md
    board.reset_logs()


def test_retrieval_scorecard_covers_golden_qa(index):
    from evals import retrieval_scorecard
    rows = retrieval_scorecard(index)
    assert len(rows) >= 8                                  # all golden Q&A queries
    assert any(r["Expected"].startswith("abstain") for r in rows)
    assert all(0.0 <= r["Score"] <= 1.0 for r in rows)
