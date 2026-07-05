"""day_9x — Onboarding Your First AI Teammate (Streamlit app, D9X-10).

Five tabs = the AI teammate's first 90 days, modelled on Watkins' *The First 90 Days*:
  Charter · Shadow mode · Early wins · Probation review · Breakeven + Retro

Runs $0 keyless (deterministic) — safe for a PUBLIC HuggingFace Space. With a local
ANTHROPIC_API_KEY, shadow-mode Q&A adds a Haiku synthesis pass; nothing else changes.
"""
from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

import config
import generate_data
import breakeven as be
from charter import Charter, sprint_snapshot, checkpoints, phase_plan

st.set_page_config(page_title="day_9x — Your First AI Teammate", page_icon="🧑‍🚀", layout="wide")

PHASE_COLOR = {"SHADOW": "#6366f1", "GATED": "#0ea5e9", "AUTONOMOUS": "#10b981"}


# ── Boot: generate world + build the index once (cached) ──────────────────────
@st.cache_resource(show_spinner="Onboarding Kai — reading the team's runbooks…")
def boot():
    generate_data.ensure_generated()
    import rag
    from agent import Teammate, load_backlog
    idx = rag.Index().build()
    return idx, Teammate(idx), load_backlog()


index, kai, backlog = boot()

if "board" not in st.session_state:
    from board import Board
    st.session_state.board = Board(tasks=backlog)
    st.session_state.coached = False
board = st.session_state.board

key_on = bool(config.get_key())
st.title("🧑‍🚀 day_9x — Onboarding Your First AI Teammate")
st.caption(
    ("🟢 Live mode — Claude Haiku enriching shadow-mode answers." if key_on
     else "⚪ $0 keyless mode — fully deterministic (public-Space safe). "
          "Set ANTHROPIC_API_KEY locally for Haiku-enriched answers.")
    + f"  ·  v{config.VERSION}  ·  All data synthetic. "
    + config.WATKINS_CREDIT.split(".")[0] + ".")

# ── Sidebar: the hiring manager's controls ────────────────────────────────────
with st.sidebar:
    st.header("🧑‍💼 Hiring manager")
    st.write("Set the onboarding duration and situation; the sprint plan re-derives.")
    stars_key = st.selectbox("STARS situation (Watkins ch.3)", list(config.STARS),
                             index=list(config.STARS).index(config.DEFAULT_STARS),
                             format_func=lambda k: config.STARS[k]["label"])
    duration = st.slider("Onboarding duration (days)", config.MIN_DURATION_DAYS,
                         config.MAX_DURATION_DAYS, config.DEFAULT_DURATION_DAYS,
                         step=config.CHECKPOINT_DAYS,
                         help="Default 90 days = exactly 6 sprints, 10 stakeholder checkpoints.")
    snap = sprint_snapshot(duration, stars_key)
    cps = checkpoints(duration)
    st.metric("Sprints (15-day)", len(snap))
    st.metric("Day-9x checkpoints", f"{len(cps)}  (x=1…{len(cps)})")
    st.caption(config.STARS[stars_key]["note"])

charter = Charter(stars_key=stars_key, duration=duration)

tab_charter, tab_shadow, tab_wins, tab_review, tab_be = st.tabs(
    ["📋 Charter", "👀 Shadow mode", "🎯 Early wins", "🎓 Probation review", "📈 Breakeven + Retro"])


# ── TAB 1 · Charter ───────────────────────────────────────────────────────────
with tab_charter:
    st.subheader("Day 0 — the charter (Watkins' Five Conversations)")
    st.write("An AI agent is the fastest-learning new hire you'll ever get — and it shows up "
             "with **zero context about your business**. The charter is how you onboard it like "
             "a teammate: scoped, reviewed, trust earned per task class.")

    st.markdown("#### Sprint snapshot")
    snap_df = pd.DataFrame([{
        "Sprint": r["sprint"], "Days": r["days"], "Phase": r["phase"],
        "Focus": r["focus"], "Checkpoints (day-9x)": ", ".join(map(str, r["checkpoints"])) or "—",
        "Exit gate": r["exit_gate"],
    } for r in snap])
    st.dataframe(snap_df, hide_index=True, use_container_width=True)

    # phase timeline bar
    ph = phase_plan(duration, stars_key)
    tl = pd.DataFrame([{"Phase": p, "start": lo, "end": hi + 1} for p, (lo, hi) in ph.items()])
    bar = alt.Chart(tl).mark_bar(height=26).encode(
        x=alt.X("start:Q", title="Day", scale=alt.Scale(domain=[1, duration + 1])),
        x2="end:Q",
        color=alt.Color("Phase:N", scale=alt.Scale(domain=list(PHASE_COLOR),
                        range=list(PHASE_COLOR.values())), legend=alt.Legend(orient="bottom")),
        tooltip=["Phase", "start", "end"])
    rules = alt.Chart(pd.DataFrame({"day": cps})).mark_rule(
        color="#94a3b8", strokeDash=[3, 3]).encode(x="day:Q")
    st.altair_chart(bar + rules, use_container_width=True)
    st.caption("Dashed lines = day-9x stakeholder checkpoints. Phase widths follow the STARS pace.")

    st.markdown("#### The Five Conversations, as the agent charter")
    for title, body in charter.five_conversations().items():
        with st.expander(title, expanded=title.startswith("2")):
            st.markdown(body)
    st.download_button("⬇️ Download charter (markdown)", charter.render_markdown(),
                       file_name="agent_charter.md")


# ── TAB 2 · Shadow mode ───────────────────────────────────────────────────────
with tab_shadow:
    st.subheader("Days 1–N — shadow mode: read-only, cited, abstains")
    left, right = st.columns([3, 2])
    with left:
        preset = st.selectbox("Ask Kai (or type your own below)", [
            "What severity is an incident touching RegReport, and where does it route?",
            "What is the tolerance for the daily GL-Hub vs CreditMart reconciliation?",
            "Can I rerun the CreditMart load on Thursday morning?",
            "Who won the football world cup?",
        ])
        q = st.text_input("Question", value=preset)
        if st.button("Ask Kai", type="primary"):
            out = kai.answer(q)
            badge = {config.LABEL_ABSTAIN: "🟠", config.LABEL_LLM: "🟢",
                     config.LABEL_DETERMINISTIC: "🔵"}[out.label]
            st.markdown(f"**{badge} {out.label}**")
            st.markdown(out.text)
            if out.citations:
                st.caption("Citations: " + " · ".join(f"`{c}`" for c in out.citations))
            if out.escalation:
                st.info("🙋 Escalation: " + out.escalation)
    with right:
        st.markdown("##### The cultural-learning moment")
        st.write("Kai's **technical** learning is instant — it read every runbook. Its "
                 "**cultural** learning is zero until a human encodes it. Ask the *Thursday* "
                 "question before and after coaching:")
        if not st.session_state.coached:
            if st.button("👩‍🏫 Coach the unwritten rules → write a Skill"):
                from board import coach_unwritten_rules
                coach_unwritten_rules(index)
                st.session_state.coached = True
                st.rerun()
            st.caption("Skill not yet coached — the Thursday question will abstain.")
        else:
            st.success("✅ Skill `unwritten_rules.md` coached into the corpus. "
                       "Kai can now answer the Thursday question — with a citation.")
            if st.button("↺ Reset coaching"):
                from board import uncoach_all
                uncoach_all(index)
                st.session_state.coached = False
                st.rerun()


# ── TAB 3 · Early wins ────────────────────────────────────────────────────────
with tab_wins:
    st.subheader("Days N–M — scoped tasks behind approval gates")
    st.write("Kai drafts 4–8h verifiable tasks; the **buddy approves, rejects, or receives an "
             "escalation**. Approvals build the per-class trust ledger. Note the deliberate "
             "unknown-system trap (T-104) — the right move is to raise its hand, not guess.")
    for t in backlog:
        with st.expander(f"`{t['id']}` · {config.TASK_CLASSES[t['cls']]['label']} — {t['title']}"
                         + ("  ⭐ early-win candidate" if t.get("early_win") else "")):
            st.caption(t["detail"])
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("Kai: draft", key=f"d{t['id']}"):
                board.submit_draft(t, kai.attempt(t))
            draft = board.drafts.get(t["id"])
            if draft:
                badge = "🟠" if draft.abstained else "🔵"
                st.markdown(f"**{badge} {draft.label}**")
                st.markdown(draft.text)
                if draft.citations:
                    st.caption("Citations: " + " · ".join(f"`{c}`" for c in draft.citations))
                if not draft.abstained:
                    if c2.button("✅ Approve", key=f"a{t['id']}"):
                        board.review(t, True); st.rerun()
                    if c3.button("❌ Reject", key=f"r{t['id']}"):
                        board.review(t, False); st.rerun()
            st.caption(f"Status: **{board.status[t['id']]}**")
    st.divider()
    cts = board.counts()
    m = st.columns(5)
    for col, (k, v) in zip(m, cts.items()):
        col.metric(k.title(), v)


# ── TAB 4 · Probation review ──────────────────────────────────────────────────
with tab_review:
    st.subheader("Day 90 — the probation review (evals, not vibes)")
    st.write("Each task class must pass its **eval gate** before autonomy is offered — the same "
             "way a human junior passes probation. Two golden cases depend on **culture** "
             "(the Thursday rule, the 2% convention): they stay red until the Skill is coached "
             "on the Shadow tab.")
    if st.button("▶️ Run probation-review evals", type="primary"):
        from evals import run_evals
        st.session_state.evalres = run_evals(kai)
    res = st.session_state.get("evalres")
    if res:
        for cls, r in res.items():
            spec = config.TASK_CLASSES[cls]
            board.ledger.record_eval(cls, r["rate"])
            state = board.ledger.state[cls]
            mark = "🟢" if r["green"] else "🔴"
            st.markdown(f"**{mark} {spec['label']}** — {r['passed']}/{r['total']} "
                        f"= {r['rate']:.0%} (gate {r['gate']:.0%}) · trust: **{state}**")
            for d in r["details"]:
                if not d["ok"]:
                    tag = " — coach the Skill on the Shadow tab" if d["culture"] else ""
                    st.caption(f"   🔴 {d['case']} — {d['note']}{tag}")
        allg = all(r["green"] for r in res.values())
        (st.success if allg else st.warning)(
            "ALL GATES GREEN — promotion may be offered per class."
            if allg else "Gates red — hold. Coach Skills / keep reviewing. Trust is earned.")


# ── TAB 5 · Breakeven + Retro ─────────────────────────────────────────────────
with tab_be:
    st.subheader("The breakeven curve + day-9x stakeholder reports")
    st.write("Watkins' **breakeven point**: a new hire consumes value before creating it "
             "(~6.2 months for a typical mid-level manager). For an AI teammate both sides are "
             "measurable in analyst-minutes — so we can show the curve, in **sprints not months**.")
    entries = be.simulate(duration, stars_key)
    daily = be.ledger(entries)
    beday = be.breakeven_day(daily)

    line = alt.Chart(daily).mark_area(opacity=0.25, line={"color": "#10b981"},
                                      color="#10b981").encode(
        x=alt.X("day:Q", title="Day"),
        y=alt.Y("cum_net:Q", title="Cumulative net value (analyst-hours)"))
    zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#ef4444").encode(y="y:Q")
    layers = [line, zero]
    if beday:
        layers.append(alt.Chart(pd.DataFrame({"day": [beday]})).mark_rule(
            color="#10b981", strokeDash=[4, 4]).encode(x="day:Q"))
    st.altair_chart(alt.layer(*layers).properties(height=320), use_container_width=True)
    c1, c2 = st.columns(2)
    c1.metric("Breakeven day", f"Day {beday}" if beday else "not yet (still investing)")
    c2.metric("Net position at day " + str(duration),
              f"{daily['cum_net'].iloc[-1]:+.1f} analyst-hours")
    st.caption("⚠️ Deterministic **simulation** of a plausible run (seeded), so the curve renders "
               "instantly for the demo. Interactive approvals on the Early-wins tab are real.")

    st.markdown("#### Day-9x stakeholder reports")
    pick = st.select_slider("Checkpoint (x)", options=checkpoints(duration),
                            value=checkpoints(duration)[-1])
    st.markdown(be.checkpoint_report(entries, pick, duration, stars_key))
