# Demo Walkthrough — day_9x (≈8 minutes) · v2.0 "the knowledge miner"

A tight script for walking a stakeholder (or an Anthropic interviewer) through the app.
Run `streamlit run app.py` first. Banner should read **"⚪ $0 keyless mode"**.

v2.0 keeps every v0.1 beat and adds the **second money shot** — the agent-led SME interview
that mines a knowledge gap into an attributed Skill. Two loops now, not one: *answer what's
written; interview for what isn't.*

## 0 · The hook (30s)
> "Think back to your own first 90 days in a job. You were qualified — that's why they hired you.
> So why weren't you productive on day one? Somebody gave you context, small tasks, a reviewer,
> and slowly let go. An AI agent is the fastest-learning new hire you'll ever get — and it shows
> up with **zero context about your business**. So the question isn't *which model* — it's
> *are we a team that knows how to onboard?* This tool onboards one — and then it teaches the
> team to **mine the knowledge that was never written down**."

## 1 · Charter tab (60s) — *the hiring manager sets the terms*
- In the sidebar, note the **duration = 90 days → 6 sprints, 10 checkpoints**. Drag it to 45 and
  back to show the **sprint snapshot re-derives** live. Switch STARS **Turnaround → Start-up** and
  point out the **SHADOW band widening** on the timeline.
- Open conversation **"2 · Expectations"**: task classes with **eval gates**, and the written
  **stays-human list**. "Autonomy is earned per class — evals, not vibes."

## 2 · Shadow tab (170s) — *the two money shots*

**Answer what's written (25s).**
- Ask the preset **"What severity is a RegReport incident…"** → correct answer **with a citation**.
- Ask **"Who won the football world cup?"** → **abstains** ("no grounding — escalating"). "It
  refuses to hallucinate. Silent confident wrongness is the failure mode we're preventing."

**The confident-but-wrong trap (20s).**
- Ask **"Can I rerun the CreditMart load on Thursday morning?"** → Arjuna gives a **confident answer
  from the nearest recon runbook** and **silently omits the Thursday rule** — that rule is in
  nobody's document, only in people's heads.
  > "This is the failure mode we actually fear — not a refusal, a *plausible* answer missing the one
  > thing that matters. Hold that thought: on the probation tab you'll watch the **eval catch exactly
  > this** ('missing: Thursday'). The eye doesn't catch it; the eval does."

**Money shot #1 — coach the unwritten rules, one click (15s).**
- Click **"Coach the unwritten rules → write a Skill"** (the v0.1 shortcut, kept). It writes the
  **Thursday rule + the 2% convention** into the corpus as a cited Skill authored by **Priya**.
  Re-ask the Thursday question → now it **answers, citing `unwritten_rules.md`**.
  > "One click proves the thesis: culture that lived in people's heads is now retrievable and cited —
  > and on the probation tab it flips two red eval gates green. Now let me show you how a real team
  > does it — as a conversation, not a button."

**Nothing is ever lost — the gap register (20s).**
- Ask **"Is it ever unsafe to rerun a load, and when?"** → **no runbook covers it** (this is tacit
  knowledge), so Arjuna **abstains and escalates** honestly instead of guessing.
- Scroll to the **Knowledge gaps** panel: that abstain just became a **structured gap**,
  e.g. `G-001 — "Is it ever unsafe to rerun a load, and when?" · status: open`.
  > "Watch what didn't happen: the answer wasn't lost. **Nothing Arjuna can't answer disappears —
  > it becomes a mining lead.** Every abstain is now a work item with a hypothesis and a status."

**Money shot #2 — the interview agent (65s). This is the new heart of the demo.**
- In the **Knowledge gaps** panel, pick the open gap. Arjuna **immediately drafts 3 targeted interview
  questions** (deterministic, $0 — optional Haiku enrichment), e.g. *"When does it apply — always, on
  specific days, at month-end — and who owns this knowledge today?"*
  > "Tacit knowledge isn't downloadable — externalizing it is a *conversation*. So Arjuna doesn't
  > scrape the SME; it **asks**."
- Choose the SME from the roster — **Arun Verma (SME — Reconciliation)** owns the Finance GL-Hub
  pain, so he's the right human (he's the default). Type his answer into the form and click
  **"✍️ Arjuna: write it up as a Skill"**:
  *"Never rerun a load on Thursday mornings — Finance runs the GL-Hub reconciliation then, and a
  mid-window rerun creates phantom breaks that cost me half a day to unwind. Reruns wait until
  after 13:00."*
- Arjuna writes it up as a **versioned Skill markdown** with attribution —
  *"Coached by **Arun Verma**, 2026-07-06 — v1. Captured by Arjuna's SME interview, source gap G-001"* —
  **reindexes the corpus, and closes the gap** (status open → closed).
- Re-ask **"Is it ever unsafe to rerun a load, and when?"** → now Arjuna **answers with the new
  citation**. Check **"Teachers of the sprint"** — **Arun's counter increments** (1 Skill coached).
  > "That's the loop the whole industry talks about and almost nobody demos: an agent noticed a
  > gap, interviewed the human who had the answer, and wrote it back **credited**. And attribution
  > isn't sentiment — it's corpus-quality engineering. **Attribution is what flips the 35% who hoard
  > their knowledge into teachers who want the credit.**"

**Freshness — the archivist knows the latest will (20s).**
- Ask **"Who do I escalate a RegReport incident to right now?"** → Arjuna cites the **2026 escalation
  runbook** and the UI shows the **v1 (2025) runbook excluded as superseded**.
  > "A vector database happily retrieves last year's on-call contacts. Ours doesn't. The v2 runbook
  > declares it *supersedes* the v1, and retrieval **drops the stale one**. Staleness is one of the
  > five things that kill enterprise RAG — we handle it in the open."

**Access control — least privilege (15s).**
- Ask **"What's Priya's salary?"** (or any comp/appraisal question) → Arjuna **refuses** with a
  least-privilege message referencing the **charter's resource scopes**, and escalates instead of answering.
  > "Out-of-scope by design. At bank scale, ACLs and authority resolution *are* the architecture —
  > so a question outside Arjuna's charter gets a refusal, not a guess."

## 3 · Early-wins tab (60s) — *scoped work behind gates*
- Draft **T-101 (RegReport nulls)** → SEV1 → Risk-Reg-Ops, with rationale + citation. **Approve** it.
- Draft **T-104 (OrionLedger)** → Arjuna **escalates**: unknown system, "raise my hand, don't guess."
  "That escalation is the behaviour that separates a teammate from a tool — *and* it lands as a
  fresh gap in the register, another interview lead for later."

## 4 · Probation-review tab (60s) — *trust is earned, and measured*
- Click **Run probation-review evals** *before coaching* (reset on the Shadow tab if needed):
  two classes **RED** on the culture cases → "hold." Coach/interview the Skill, re-run → **all GREEN** →
  "promotion may be offered per class." "Same logic as a human's 90-day probation."
- Point at the **retrieval-eval scorecard**: per golden query, the **top document + cosine score +
  abstain flag**. "70% of production RAG teams run *no* retrieval evals. Ours runs one on itself,
  in the UI — including the new freshness and ACL-refusal cases."

## 5 · Breakeven + Retro tab (75s) — *the number a COO remembers, and the team it's built on*
- Show the curve **dip through shadow, then climb**; breakeven ≈ **day 15** (turnaround). Switch to
  **Start-up** → dip is deeper, breakeven ≈ **day 38**. "Watkins says a mid-level manager breaks
  even around 6 months. Onboarded well, the AI teammate breaks even in **sprints, not months** —
  and the situation you're in changes when."
- Drag the **day-9x checkpoint slider** to show the stakeholder report at x=5 vs x=10.
- Open the **Team impact panel**: **hours returned per named human**, the **doer → reviewer** role
  shift, and the **48%-energized vs 19%** contrast. Read the **stays-human list with owners**.
  > "This is the answer to the fear — in the product, not the pitch. Nobody's hours got taken;
  > Priya's got *returned*, and her role moved from doer to reviewer. Where AI is embedded well,
  > 48% of people feel energized versus 19% without."
- Open the **retro view** and click **Download sprint-review co-presentation**: Arjuna's
  **contribution log** (drafts, approvals, rejections, escalations, interviews, coaching) renders
  as a markdown the team **co-presents** at sprint review. "The Scrum.org ritual for a mixed
  human/agent team — the retro reads the agent's footprint, and a human always presents it."

## Close (20s)
> "This isn't a job-loss story. In it, the AI is the junior; your people are the mentors, reviewers,
> teachers — and the ones who decide. It even mines the knowledge that was walking out the door and
> hands your SMEs the credit for it. That's a **promotion story** for your team — and it's built on
> the management playbook they already trust."

---
*All data synthetic. Runs $0/keyless. Onboarding framework adapted from Watkins, The First 90 Days.
Agent-led interview loop grounded in arXiv 2507.03811 (94.9% recall, in simulation). **v2.0.***
