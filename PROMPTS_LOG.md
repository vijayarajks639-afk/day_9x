# PROMPTS_LOG — day_9x

Append-only record of the human intent that shaped this build (paraphrased), for transparency
about the AI-pair workflow. Newest last.

---

**Origin.** Vijay's Anthropic-interview thesis: enterprises will adopt AI at every level, but
legacy modernization stalls because knowledge is *trapped* in SMEs, processes, work logs and
documents. Chosen stakeholder metaphor: **"the new team member"** — onboard an AI agent like a
new hire. See `Projects/enterprise_ai_pov/STORY_new_team_member.md`.

**Build request.** "Using this metaphor, start building the prototype — as usual: JIRA sprint
planning, stories, GitHub evidence, and if needed HuggingFace Space uploads. Do a deep review
first." → deep review + plan, approved.

**Grounding in Watkins.** Vijay supplied *The First 90 Days* (Watkins, HBS Press 2003) and asked
to read it and fold it into the prototype. Decision (via AskUserQuestion): **full Watkins spine**
— Five Conversations charter, STARS selector, breakeven curve, cited throughout; **full 90-day
journey** scope; **public HF Space, $0 keyless**; naming **day_9x** (his idea: a "9-day report to
stakeholders" — x=1..10, so x=10 ⇒ 90 days ⇒ 6 sprints).

**Hiring-manager control.** "Give the hiring manager an option to enter the onboarding duration
and show a sprint snapshot; default/propose 90 days. Keep the sprint plan in JIRA, GitHub, and HF."
→ sidebar duration slider (default 90) + STARS selector; sprint snapshot re-derives; `JIRA_STATUS.md`
is the in-repo board (project key D9X).

**Interim reporting.** "Share the sprint and progress as an interim report" / "keep things recorded
and at the end give me a detailed PPT." → live `JIRA_STATUS.md` updates during the build; a
generated stakeholder deck (`make_deck.py` → `day_9x_stakeholder_deck.pptx`) at the end.

---

## Governance rails honoured throughout
- All data **synthetic** — no real firm data, no real people.
- Public Space runs **$0 keyless**; `ANTHROPIC_API_KEY` is local-env only, never a public secret.
- Watkins frameworks **paraphrased with attribution**; no book text reproduced.
- **Story-first** cadence: stories created before the work; `JIRA_STATUS.md` updated live;
  worklogs are AI-actual minutes.
- GitHub PAT / HF token requested **only at push/deploy time** — deliberately not stored.
