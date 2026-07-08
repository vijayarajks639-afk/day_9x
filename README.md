---
title: day_9x — Onboarding Your First AI Teammate
emoji: 🧑‍🚀
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 8501
pinned: false
license: mit
---

# day_9x — Onboarding Your First AI Teammate

An interactive demo that onboards an **AI agent into a human scrum team** the same way you'd
onboard a new hire — modelled mechanism-by-mechanism on Michael D. Watkins' *The First 90 Days*.

> **The reframe:** an AI agent is the fastest-learning new hire you'll ever get — it can read a
> million pages before Monday — and it still shows up with **zero context about your business**.
> Companies that onboard it like a junior teammate (scoped tasks, a buddy who reviews, trust earned
> task by task) get compounding value. Companies that throw it in the deep end get a failed hire.
> So the real question isn't "which model" — it's **"are we a team that knows how to onboard?"**

The hiring manager sets the **onboarding duration** (default **90 days = 6 sprints**, 10 stakeholder
checkpoints); the sprint plan re-derives. The agent — "Arjuna" — joins a synthetic **credit-risk
data-ops** team and moves through three trust states, gate by gate.

## The five tabs = the first 90 days

| Tab | Watkins concept | What it does |
|---|---|---|
| **📋 Charter** | The Five Conversations + STARS | Build Arjuna's charter as situation / expectations / style / resources / development; a STARS selector adapts the onboarding pace; sprint snapshot + phase timeline |
| **👀 Shadow mode** | Accelerate your learning | RAG over the team's runbooks with **citations** and an **abstain** guardrail; the **cultural-learning moment** — Arjuna flubs the "Thursday rule" until an SME **coaches** it into a Skill |
| **🎯 Early wins** | Secure early wins | Scoped 4–8h tasks behind **approval gates**; **helpful-abstain escalation** on an unknown-system trap ("raise your hand, don't guess") |
| **🎓 Probation review** | Build your team (trust = threshold issue) | **Eval gates** per task class; two golden cases stay red until the Skill is coached — evals, not vibes |
| **📈 Breakeven + Retro** | The breakeven point | Value **consumed vs created** in analyst-hours; the curve dips through shadow then climbs; **day-9x** stakeholder reports |

## Key properties

- **$0 / keyless** — the whole app runs deterministically with no API key, so it is **safe on a
  public HuggingFace Space**. With a local `ANTHROPIC_API_KEY`, shadow-mode Q&A adds a Claude Haiku
  synthesis pass; the deterministic backbone, citations, and evals never change.
- **Trust is earned per task class** — SHADOW (drafts, 100% reviewed) → GATED (act with approval) →
  AUTONOMOUS (act within charter, audit sample). Promotion requires an eval gate **and** verified
  evidence; it is revocable.
- **The coaching loop is real** — coaching writes a versioned Skill into the corpus and reindexes;
  the answer that abstained before now resolves **with a citation**. The Skill history *is* the
  coaching record.
- **Everything synthetic** — no real firm data, no real people, no PII.

## Run locally

```bash
pip install -r requirements.txt
python generate_data.py          # write the synthetic team world (idempotent)
python evals.py                  # probation review: uncoached → 2 culture gates RED
python evals.py --coached        # coach the Skill first → all gates GREEN
python -m pytest test_day9x.py -q
streamlit run app.py
```

## Stack

Python 3.12 · **fastembed** (local ONNX embeddings, no PyTorch) · **numpy** (transparent vector
store) · **altair** · **Streamlit 1.41** · **Claude Haiku** (optional) · synthetic corpus.

## Versions

See [CHANGELOG.md](CHANGELOG.md). **v0.1** (frozen, tag `v0.1`) = the Watkins 90-days demo.
**v2.0** = the knowledge-miner release: gap register, Arjuna-led SME interviews → authored Skills,
SME credit ledger, staleness + ACL realism, team-impact panel, contribution log + retro artifacts.

## Attribution

Onboarding framework adapted from **Michael D. Watkins, *The First 90 Days*** (Harvard Business
School Press, 2003). Frameworks are **paraphrased with attribution; no book text is reproduced**.
Built as a portfolio / interview asset by a senior banking data & AI leader.
