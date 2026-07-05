# Demo Walkthrough — day_9x (≈6 minutes)

A tight script for walking a stakeholder (or an Anthropic interviewer) through the app.
Run `streamlit run app.py` first. Banner should read **"⚪ $0 keyless mode"**.

## 0 · The hook (30s)
> "Think back to your own first 90 days in a job. You were qualified — that's why they hired you.
> So why weren't you productive on day one? Somebody gave you context, small tasks, a reviewer,
> and slowly let go. An AI agent is the fastest-learning new hire you'll ever get — and it shows
> up with **zero context about your business**. So the question isn't *which model* — it's
> *are we a team that knows how to onboard?* This tool onboards one."

## 1 · Charter tab (60s) — *the hiring manager sets the terms*
- In the sidebar, note the **duration = 90 days → 6 sprints, 10 checkpoints**. Drag it to 45 and
  back to show the **sprint snapshot re-derives** live. Switch STARS **Turnaround → Start-up** and
  point out the **SHADOW band widening** on the timeline.
- Open conversation **"2 · Expectations"**: task classes with **eval gates**, and the written
  **stays-human list**. "Autonomy is earned per class — evals, not vibes."

## 2 · Shadow tab (90s) — *the trapped-knowledge moment (the money shot)*
- Ask the preset **"What severity is a RegReport incident…"** → correct answer **with a citation**.
- Ask **"Can I rerun the CreditMart load on Thursday morning?"** → Kai answers from the nearest
  runbook but **does not know the Thursday rule** — it's in nobody's document, only in people's heads.
- Ask **"Who won the football world cup?"** → **abstains** ("no grounding — escalating"). "It
  refuses to hallucinate. Silent confident wrongness is the failure mode we're preventing."
- Click **"Coach the unwritten rules → write a Skill."** Re-ask the Thursday question → now it
  **answers, citing `unwritten_rules.md`**. "That's the thesis in one click: the knowledge was
  trapped in an SME; we unlocked it as a reusable, cited, versioned Skill."

## 3 · Early-wins tab (60s) — *scoped work behind gates*
- Draft **T-101 (RegReport nulls)** → SEV1 → Risk-Reg-Ops, with rationale + citation. **Approve** it.
- Draft **T-104 (OrionLedger)** → Kai **escalates**: unknown system, "raise my hand, don't guess."
  "That escalation is the behaviour that separates a teammate from a tool."

## 4 · Probation-review tab (60s) — *trust is earned*
- Click **Run probation-review evals** *before coaching* (reset on the Shadow tab if needed):
  two classes **RED** on the culture cases → "hold." Coach the Skill, re-run → **all GREEN** →
  "promotion may be offered per class." "Same logic as a human's 90-day probation."

## 5 · Breakeven tab (60s) — *the number a COO remembers*
- Show the curve **dip through shadow, then climb**; breakeven ≈ **day 15** (turnaround). Switch to
  **Start-up** → dip is deeper, breakeven ≈ **day 38**. "Watkins says a mid-level manager breaks
  even around 6 months. Onboarded well, the AI teammate breaks even in **sprints, not months** —
  and the situation you're in changes when."
- Drag the **day-9x checkpoint slider** to show the stakeholder report at x=5 vs x=10.

## Close (20s)
> "This isn't a job-loss story. In it, the AI is the junior; your people are the mentors, reviewers,
> and the ones who decide. That's a **promotion story** for your team — and it's built on the
> management playbook they already trust."

---
*All data synthetic. Runs $0/keyless. Onboarding framework adapted from Watkins, The First 90 Days.*
