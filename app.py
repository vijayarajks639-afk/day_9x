"""day_9x — Onboarding Your First AI Teammate (Streamlit app, D9X-10).

Five tabs = the AI teammate's first 90 days, modelled on Watkins' *The First 90 Days*:
  Charter · Shadow mode · Early wins · Probation review · Breakeven + Retro

Runs $0 keyless (deterministic) — safe for a PUBLIC HuggingFace Space. With a local
ANTHROPIC_API_KEY, shadow-mode Q&A adds a Haiku synthesis pass; nothing else changes.
"""
from __future__ import annotations

import json

import altair as alt
import pandas as pd
import streamlit as st

import config
import generate_data
import breakeven as be
import gaps as gaps_mod
from charter import Charter, sprint_snapshot, checkpoints, phase_plan

st.set_page_config(page_title="day_9x — Your First AI Teammate", page_icon="🧑‍🚀", layout="wide")

PHASE_COLOR = {"SHADOW": "#6366f1", "GATED": "#0ea5e9", "AUTONOMOUS": "#10b981"}


# ── Boot: generate world + build the index once (cached) ──────────────────────
@st.cache_resource(show_spinner="Onboarding Arjuna — reading the team's runbooks…")
def boot():
    generate_data.ensure_generated()
    import rag
    import board as board_mod
    import gaps as gaps_mod
    from agent import Teammate, load_backlog
    idx = rag.Index().build()
    # v2.0 (m2): a fresh PROCESS starts from the honest "before" — no coached
    # Skills, teachers, gaps or contribution log carried over from a prior run
    # (matters on a shared public Space, where a new audience must not inherit
    # stale state). In-session progress persists because @st.cache_resource runs
    # boot() only once per process; concurrent viewers of one process still share
    # state — press "Full demo reset" to re-baseline, or run one Space per demo.
    board_mod.uncoach_all(idx)
    board_mod.reset_logs()
    gaps_mod.GapRegister().reset()
    return idx, Teammate(idx), load_backlog()


index, arjuna, backlog = boot()

if "board" not in st.session_state:
    from board import Board
    st.session_state.board = Board(tasks=backlog)
    st.session_state.coached = False
board = st.session_state.board
gap_register = gaps_mod.GapRegister()          # file-backed; survives reruns

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

tab_start, tab_charter, tab_shadow, tab_wins, tab_review, tab_be = st.tabs(
    ["👋 Start here", "📋 Charter", "👀 Shadow mode", "🎯 Early wins",
     "🎓 Probation review", "📈 Breakeven + Retro"])


# ── TAB 0 · Start here (the explainer landing — business + tech) ───────────────
with tab_start:
    import streamlit.components.v1 as components
    _about = config.ROOT / "about.html"
    if _about.exists():
        components.html(_about.read_text(encoding="utf-8"), height=3700, scrolling=True)
    else:
        st.info("Explainer page not found — see the tabs above to explore the demo.")


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
        preset = st.selectbox("Ask Arjuna (or type your own below)", [
            "What severity is an incident touching RegReport, and where does it route?",
            "What is the tolerance for the daily GL-Hub vs CreditMart reconciliation?",
            "Is it ever unsafe to rerun a load, and when?",
            "Can I rerun the CreditMart load on Thursday morning?",
            "Who won the football world cup?",
        ])
        q = st.text_input("Question", value=preset)
        if st.button("Ask Arjuna", type="primary"):
            import board as board_mod
            out = arjuna.answer(q)
            badge = {config.LABEL_ABSTAIN: "🟠", config.LABEL_LLM: "🟢",
                     config.LABEL_DETERMINISTIC: "🔵"}[out.label]
            st.markdown(f"**{badge} {out.label}**")
            st.markdown(out.text)
            if out.citations:
                st.caption("Citations: " + " · ".join(f"`{c}`" for c in out.citations))
                board_mod.credit_citations(out.citations)   # teachers get credit
                board_mod.log_contribution("qa", "shadow", f"answered: {q[:60]}")
            if out.acl_blocked:
                st.warning("🔒 " + out.escalation)
            elif out.escalation:
                gap = gap_register.record(q, out.escalation, source="qa")
                st.info(f"🙋 Escalation: {out.escalation}")
                st.success(f"⛏️ Logged as knowledge gap **{gap.id}** — nothing Arjuna "
                           "can't answer is lost; it becomes a mining lead below.")
    with right:
        st.markdown("##### The cultural-learning moment")
        st.write("Arjuna's **technical** learning is instant — it read every runbook. Its "
                 "**cultural** learning is zero until a human encodes it. Uncoached, the "
                 "*Thursday* question gets a confident answer from the nearest recon "
                 "runbook that silently **omits the Thursday rule** — the probation eval "
                 "catches it (missing 'Thursday'). Coach the rule and it answers "
                 "correctly, with a citation:")
        if not st.session_state.coached:
            if st.button("👩‍🏫 Coach the unwritten rules → write a Skill"):
                from board import coach_unwritten_rules
                coach_unwritten_rules(index)
                st.session_state.coached = True
                st.rerun()
            st.caption("Skill not yet coached — the Thursday rule lives in nobody's "
                       "runbook, only in people's heads, so the eval gate stays red "
                       "until it's coached.")
        else:
            st.success("✅ Skill `unwritten_rules.md` coached into the corpus. "
                       "Arjuna can now answer the Thursday question — with a citation.")
        if st.button("↺ Full demo reset (skills · gaps · logs)"):
            import board as board_mod
            board_mod.uncoach_all(index)
            board_mod.reset_logs()
            gap_register.reset()
            st.session_state.coached = False
            st.rerun()
        if index.superseded:
            st.caption("🗓️ Freshness rule active — excluded as superseded: "
                       + ", ".join(f"`{old}` (replaced by `{new}`)"
                                   for old, new in index.superseded.items()))
        import board as board_mod
        teachers = board_mod.teachers_of_the_sprint()
        if teachers:
            st.markdown("##### 🏆 Teachers of the sprint")
            st.caption("Named credit is the incentive that flips knowledge "
                       "hoarding into teaching — 'your knowledge answered N questions.'")
            st.dataframe(pd.DataFrame(teachers), hide_index=True,
                         use_container_width=True)

    # ── The knowledge miner (v2.0): gap register → Arjuna interviews the SME ─────
    st.divider()
    st.markdown("#### ⛏️ Knowledge gaps — Arjuna mines what the corpus can't answer")
    open_gaps = gap_register.open_gaps()
    if not open_gaps:
        st.caption("No open gaps. Ask Arjuna something no runbook covers — try "
                   "*\"Is it ever unsafe to rerun a load, and when?\"* — and the "
                   "miss lands here as a mining lead.")
    else:
        import board as board_mod
        pick_gap = st.selectbox(
            "Open gaps", open_gaps,
            format_func=lambda g: f"{g.id} · {g.question}  ({g.status})")
        st.caption(f"Arjuna's hypothesis: {pick_gap.hypothesis}")
        st.markdown("**🎤 Arjuna's interview questions for the SME:**")
        for i, iq in enumerate(arjuna.interview_questions(pick_gap), 1):
            st.markdown(f"{i}. {iq}")
        with st.form(f"interview_{pick_gap.id}"):
            humans = [m["name"] for m in json.loads(
                (config.DATA_DIR / "team.json").read_text(encoding="utf-8"))
                if m["name"] != "Arjuna"]
            sme = st.selectbox("SME being interviewed", humans, index=3)
            answer = st.text_area(
                "The SME's answer (type what the expert says)",
                placeholder="e.g. Never rerun that load while Finance holds its "
                            "reconciliation window — wait until after 13:00…")
            if st.form_submit_button("✍️ Arjuna: write it up as a Skill", type="primary"):
                if answer.strip():
                    fname = board_mod.author_skill(index, pick_gap, sme, answer)
                    gap_register.close(pick_gap.id, sme, fname)
                    st.success(f"Skill `{fname}` authored — coached by **{sme}**, "
                               f"cited from now on, gap **{pick_gap.id}** closed. "
                               "Re-ask the question above to see it answered.")
                    st.rerun()
                else:
                    st.error("The SME's answer is empty — knowledge can't be "
                             "mined from silence.")


# ── TAB 3 · Early wins ────────────────────────────────────────────────────────
with tab_wins:
    st.subheader("Days N–M — scoped tasks behind approval gates")
    st.write("Arjuna drafts 4–8h verifiable tasks; the **buddy approves, rejects, or receives an "
             "escalation**. Approvals build the per-class trust ledger. Note the deliberate "
             "unknown-system trap (T-104) — the right move is to raise its hand, not guess.")
    for t in backlog:
        with st.expander(f"`{t['id']}` · {config.TASK_CLASSES[t['cls']]['label']} — {t['title']}"
                         + ("  ⭐ early-win candidate" if t.get("early_win") else "")):
            st.caption(t["detail"])
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("Arjuna: draft", key=f"d{t['id']}"):
                out = arjuna.attempt(t)
                board.submit_draft(t, out)
                if out.escalation and not out.acl_blocked:
                    gap_register.record(t["title"], out.escalation, source="task")
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
        st.session_state.evalres = run_evals(arjuna)
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

    with st.expander("🔎 Retrieval-eval scorecard — does the right knowledge surface?"):
        st.caption("Task evals grade the ANSWER; this grades the RETRIEVAL. Most "
                   "production RAG teams run no retrieval evaluation at all — "
                   "this scorecard is the discipline that separates a demo from "
                   "a deployable.")
        from evals import retrieval_scorecard
        st.dataframe(pd.DataFrame(retrieval_scorecard(index)), hide_index=True,
                     use_container_width=True)


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

    # ── Team impact (v2.0): the 52%-fear answer, in the product ───────────────
    st.divider()
    st.markdown("#### 🧑‍🤝‍🧑 One team — what each human gets back")
    st.write("In this story the AI is the **junior**; the humans are the mentors, "
             "reviewers and deciders. Every hour Arjuna returns is redeployed toward "
             "the review-and-judgement work that was always understaffed — where AI "
             "is embedded well, **48% of workers report feeling energized vs 19% "
             "without** (Adaptavist, 2025).")
    st.dataframe(pd.DataFrame(be.team_impact(entries)), hide_index=True,
                 use_container_width=True)
    st.caption("**Stays human — written down, not implied:** " +
               " · ".join(charter.stays_human))

    # ── Retro: Arjuna's contribution log + co-presentation (v2.0) ────────────────
    st.divider()
    st.markdown("#### 📋 Retro — Arjuna's contribution log")
    import board as board_mod
    log = board_mod.contribution_log()
    if log:
        st.dataframe(pd.DataFrame(log), hide_index=True, use_container_width=True)
        st.download_button("⬇️ Sprint-review co-presentation (markdown)",
                           board_mod.co_presentation(),
                           file_name="sprint_review_copresentation.md")
    else:
        st.caption("Nothing logged yet this session — ask questions on the Shadow "
                   "tab or work the Early-wins board, and the retro fills itself. "
                   "The retro that analyzes the agent's log is the new team ritual.")
