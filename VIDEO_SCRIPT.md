# day_9x — Explainer Video Script

**Project:** day_9x — an interactive Streamlit demo that simulates the first 90 days of an AI agent ("Arjuna") being onboarded onto a human credit-risk data-operations scrum team, modelled on Michael Watkins' *The First 90 Days*.
**Built by:** Vijayaraj Shanmugam
**Live demo:** https://huggingface.co/spaces/vijayarajks/day-9x
**Source:** https://github.com/vijayarajks639-afk/day_9x
**Purpose of this asset:** AI-generated explainer video (Google Gemini / Veo), clip-by-clip.
**Primary cut:** 90 seconds (LinkedIn / portfolio). **Extended cut:** ~3 minutes (appendix).

---

## Production Notes (read first)

**Audience (dual):** business stakeholders — hiring managers, execs — first; technical credibility second. The **voiceover stays plain-English and confident** (no jargon). The **on-screen text carries the technical specifics** (trust states, eval gates, tab names).

**Visual style:** clean, modern, enterprise-credible. Calm and confident, not cartoonish, no stock-corporate cliché (no handshakes, no glowing brains, no robot-vs-human imagery). Think a well-shot product film for a serious data platform.

**Palette — the trust progression (use it as the film's spine):**
- **Indigo** `#4F46E5` — *Shadow* (drafts only, 100% reviewed)
- **Sky blue** `#38BDF8` — *Gated* (may act, every output needs human sign-off)
- **Emerald green** `#10B981` — *Autonomous* (acts, light audit sample)

Color should literally *travel* indigo → sky → emerald across the film as trust is earned. Backgrounds: near-white or deep slate; generous whitespace; one accent at a time.

**Show the real product.** Wherever a scene references the app, favour genuine glimpses of the Streamlit UI over abstraction: the **STARS timeline re-shaping**, the **eval gates flipping green**, the **breakeven curve** drawing itself, the **"Teachers of the sprint"** board.

**Voice:** warm, senior, unhurried. Female or male, mid-range, documentary tone. No hype-y announcer.

**Pace target:** ~2.5 words/second. Word counts are listed per scene so narration fits the shot.

**Framing guardrail (non-negotiable):** ONE TEAM, not human-vs-AI. Humans are mentors, reviewers, and deciders; the agent is the junior. Keep it hopeful and collaborative. Never imply job loss.

---

# PRIMARY CUT — 90 SECONDS

**8 scenes · total narration ≈ 223 words · ~89s at 2.5 wps**

---

## Scene 1 — The Hook
**Duration:** 0:00–0:10 (10s) · Narration: 21 words

**VISUAL:** A calm, bright modern office at dawn, seen wide. A single empty desk with a laptop waking up; a soft indigo login glow reflects on the screen. Slow push-in on the screen. No people yet. Understated, cinematic, shallow depth of field. The mood is "first day."

**ON-SCREEN TEXT:**
`The fastest-learning new hire you'll ever get.`

**NARRATION:**
> "An AI agent is the fastest-learning new hire you'll ever get. But on day one, it knows nothing about your business."

---

## Scene 2 — Reframe the Question
**Duration:** 0:10–0:22 (12s) · Narration: 30 words

**VISUAL:** Two lines of text resolve on a clean slate background. The first — "Which model?" — fades and dims. The second — "Can this team onboard one?" — sharpens and holds in indigo. Then a small team of four analysts appears seated around a table, an empty chair among them, calm and collaborative. Gentle motion.

**ON-SCREEN TEXT:**
`Wrong question: "Which model?"`
`Right question: "Can this team onboard one?"`

**NARRATION:**
> "So the real question was never 'which model?' It's quieter: is this a team that knows how to onboard one? Humans mentor and decide; the agent starts as the junior."

---

## Scene 3 — Meet day_9x + STARS
**Duration:** 0:22–0:34 (12s) · Narration: 30 words

**VISUAL:** The day_9x Streamlit app materialises on screen. Title "day_9x" and a friendly agent nameplate, "Arjuna." Then the **STARS timeline** — a horizontal 90-day bar — visibly *re-shapes* as a selector cycles through the five situations: Start-up, Turnaround, Accelerating growth, Realignment, Sustaining success. The shadow segment stretches and shrinks with each choice. Screen-capture realism.

**ON-SCREEN TEXT:**
`Arjuna · onboarded over 90 days`
`STARS sets the pace: Start-up · Turnaround · Accelerating growth · Realignment · Sustaining success`

**NARRATION:**
> "Meet day_9x — a working demo where an agent named Arjuna is onboarded over ninety days, from Michael Watkins' playbook. Step one: diagnose the situation — five patterns that set the pace."

---

## Scene 4 — Charter, Shadow, Early Wins
**Duration:** 0:34–0:48 (14s) · Narration: 35 words

**VISUAL:** Three app tabs flow past in sequence.
1. **Charter** — a written page with a highlighted "Stays human" list of decisions the agent never makes.
2. **Shadow mode** — a read-only answer with a visible **citation chip**; then a query where the agent returns "No grounding — raising my hand" instead of guessing (indigo).
3. **Early wins** — a small task card behind an **Approve / Reject / Escalate** gate; a human clicks Approve (sky blue). Smooth left-to-right camera drift; color warms indigo → sky.

**ON-SCREEN TEXT:**
`1 Charter — what stays human`
`2 Shadow — cited, or it abstains`
`3 Early wins — behind a human gate`

**NARRATION:**
> "From there, a charter writes down what stays human. Then shadow mode — read-only, every answer cited; with no grounding, it raises its hand instead of guessing. Early wins follow, each behind a human approval gate."

---

## Scene 5 — Probation Review (Day 90)
**Duration:** 0:48–1:00 (12s) · Narration: 32 words

**VISUAL:** The **Probation review** tab. A grid of task classes with **eval gates**. Most flip from grey to **emerald green** with a satisfying tick. Two cells labelled "culture" stay **red**. A human writes a short note ("the unwritten rule") and those two cells then turn green. Evidence, not vibes — show the pass/fail bars.

**ON-SCREEN TEXT:**
`Autonomy earned by evals, not vibes`
`2 culture tests stay red — until a human coaches the rule in`

**NARRATION:**
> "At day ninety, autonomy is earned by evidence, not vibes. Every task class must pass a quality gate — and two culture tests stay red until a human coaches the unwritten rule in."

---

## Scene 6 — The Knowledge Miner
**Duration:** 1:00–1:12 (12s) · Narration: 33 words

**VISUAL:** The agent hits a question with no runbook answer. A short, respectful "interview" exchange appears with a named human expert. Their answer crystallises into a **versioned "Skill" card** with the expert's name attached and a citation link. Cut to the **"Teachers of the sprint"** board — a leaderboard of human names, each credited. Warm, human, sky-blue accent.

**ON-SCREEN TEXT:**
`When knowledge lives only in a head → the agent interviews the expert`
`→ a versioned, attributed, citable Skill`
`Teachers of the sprint`

**NARRATION:**
> "Here's the twist. When knowledge lives only in someone's head, the agent interviews them and turns it into a credited, citable skill. A 'Teachers of the sprint' board names whose expertise now answers."

---

## Scene 7 — Breakeven & Payoff
**Duration:** 1:12–1:24 (12s) · Narration: 28 words

**VISUAL:** The **Breakeven** tab. A **value curve** in analyst-hours draws itself left to right: it dips below the line first (the agent consuming effort), then crosses and climbs into **emerald green** (creating value, hours returned). Small callouts show hours handed back to named humans, and a shift from "doing" to "reviewing." Confident, data-film clarity.

**ON-SCREEN TEXT:**
`Value in analyst-hours`
`Attribution turns hoarding → teaching`
`Breakeven in sprints, not months`

**NARRATION:**
> "That attribution turns hoarding into teaching. And the payoff shows here — a value curve in analyst-hours, when the agent starts giving hours back. Breakeven in sprints, not months."

---

## Scene 8 — Thesis + Call to Action
**Duration:** 1:24–1:30 (6s) · Narration: 14 words

**VISUAL:** Return to the team from Scene 2 — now the empty chair is filled, the whole group facing forward, calm and in sync. Color settles on a confident emerald. The demo URL types itself on screen.

**ON-SCREEN TEXT:**
`Try the live demo`
`huggingface.co/spaces/vijayarajks/day-9x`
`day_9x · built by Vijayaraj Shanmugam · $0 / keyless`

**NARRATION:**
> "The best time to learn to onboard one is now. Try it — link below."

---

## Closing Card (holds ~3s over/after Scene 8, silent)

**ON-SCREEN TEXT:**
```
day_9x
Live: huggingface.co/spaces/vijayarajks/day-9x
Source: github.com/vijayarajks639-afk/day_9x

Onboarding model paraphrased from Michael Watkins, "The First 90 Days" (with attribution).
All data shown is synthetic.
```

---

# APPENDIX — EXTENDED ~3-MINUTE CUT

Same spine, same order, same thesis. Expand the primary cut by letting the product breathe and by adding two beats. Target ~180s, narration ≈ 430–450 words. **Which scenes to expand:**

- **Scene 1 (→ 15s):** Add one line establishing the setting — a credit-risk data-operations scrum team — so the stakes are concrete before the agent appears.
- **Scene 2 (→ 18s):** Spell out the ONE TEAM framing explicitly: humans as mentors, reviewers, and deciders; the agent as the junior who never touches the "stays-human" decisions. This is the anti-"job-loss" anchor — give it room.
- **Scene 3 (→ 25s):** Walk all **five STARS situations** individually, showing the timeline re-shape for two contrasting cases — e.g. *Turnaround* (short shadow, fast tight-leashed wins) vs *Start-up* (long learning phase because there are no runbooks yet). Name the "why" for each.
- **NEW Scene 3b — The Trust Ladder (~15s):** A dedicated beat on the three revocable, evidence-based states, per task class, with the colors: **SHADOW (indigo)** → **GATED (sky-blue)** → **AUTONOMOUS (emerald)**. Show a task class climbing one rung. On-screen text: "Revocable. Per task class. Earned by evidence."
- **Scene 4 (→ 30s):** Give Charter, Shadow, and Early wins one clean beat each instead of a flyby. On Shadow, dwell on the abstain moment — name "silent confident wrongness" as the failure mode being designed out. On Early wins, show an *approval building trust* (a second task unlocking after a first is approved).
- **Scene 5 (→ 25s):** Show the eval grid in full — task class by task class — then the two red culture cells, the human coaching note, and the flip to green. Emphasise: autonomy is a decision backed by evals, not a vibe.
- **Scene 6 (→ 30s):** Play the expert interview as a genuine short exchange, then the versioned Skill card, then the "Teachers of the sprint" board filling with names. Land the point clearly: attribution flips the instinct to hoard knowledge into an incentive to teach — experts are *credited, not replaced*.
- **NEW Scene 6b — The Two Clocks (~12s):** Explain the name and cadence: **day_9x** = a stakeholder report every **9 days** (x = 1…10, so x=10 → 90 days). Two clocks: **15-day sprints** pace the work; **9-day checkpoints** pace stakeholder communication.
- **Scene 7 (→ 25s):** Let the breakeven curve draw slowly; call out the shift from *doing* to *reviewing* and the hours handed back to each named human. Reiterate "breakeven in sprints, not months."
- **Scene 8 (→ 15s):** Restate the thesis in full — *the winning question isn't "which model?", it's "is this a team that knows how to onboard one?"* — then the CTA and URL.
- **Closing card:** unchanged (Watkins attribution + "all data synthetic").

---

# VEO / GEMINI GENERATION PROMPTS (copy-paste, clip-by-clip)

> Veo/Gemini generates one clip at a time. **Prepend the GLOBAL STYLE PREFIX to every scene prompt** for a consistent look. Each scene prompt below is self-contained (visuals + camera + mood + text overlay). Keep clips 6–14s to match the script. If a model won't render legible UI text, generate the shot as a clean abstraction and composite the real Streamlit screen-capture / on-screen text in post.

### GLOBAL STYLE PREFIX (prepend to each prompt)
```
Clean, modern, enterprise-credible explainer film. Calm and confident, not cartoonish, no stock-corporate cliché, no robots, no glowing brains, no human-vs-machine imagery. Generous whitespace, near-white or deep-slate backgrounds, one accent color at a time. Trust-progression palette used deliberately: indigo #4F46E5, then sky blue #38BDF8, then emerald green #10B981. Cinematic, shallow depth of field, smooth slow camera moves, soft natural light, subtle film grain. 16:9. High detail, photoreal product-film aesthetic. Any on-screen UI should read as a real, tasteful Streamlit web app.
```

### Scene 1 — Hook
```
A quiet, bright modern open-plan office at dawn. One empty desk, a laptop just waking, a soft indigo login glow reflecting on the screen. Slow push-in toward the screen. No people yet. Cinematic, understated, "first day" mood. Overlay text, small, lower third: "The fastest-learning new hire you'll ever get."
```

### Scene 2 — Reframe the Question
```
Minimal slate background. Text "Which model?" appears then fades and dims to grey. Text "Can this team onboard one?" sharpens in indigo and holds center. Then reveal four analysts seated calmly around a table with one empty chair among them, collaborative, warm. Slow gentle dolly. Overlay text: "Wrong question: Which model?  /  Right question: Can this team onboard one?"
```

### Scene 3 — Meet day_9x + STARS
```
Screen-capture realism of a tasteful Streamlit web app titled "day_9x" with an agent nameplate "Arjuna". A horizontal 90-day timeline bar visibly re-shapes as a selector cycles five labels: Start-up, Turnaround, Accelerating growth, Realignment, Sustaining success. The early "shadow" segment stretches and shrinks with each selection. Clean UI, indigo accents, smooth transitions. Overlay text: "Arjuna · onboarded over 90 days — STARS sets the pace."
```

### Scene 4 — Charter, Shadow, Early Wins
```
Smooth left-to-right camera drift across three app panels. Panel 1: a written "Charter" page with a highlighted "Stays human" list. Panel 2: a "Shadow mode" answer with a visible citation chip, then a message "No grounding — raising my hand." Panel 3: an "Early wins" task card with Approve / Reject / Escalate buttons, a cursor clicking Approve. Color warms from indigo to sky blue across the move. Overlay text: "Charter · Shadow · Early wins."
```

### Scene 5 — Probation Review
```
A tasteful Streamlit "Probation review" grid of task classes with status cells. Most cells flip from grey to emerald green with a soft tick. Two cells labelled "culture" stay red. A cursor adds a short human note, and those two cells then turn green. Small pass/fail bars visible. Confident, data-film clarity. Overlay text: "Autonomy earned by evals, not vibes."
```

### Scene 6 — The Knowledge Miner
```
A short, respectful on-screen interview exchange between the app and a named human expert. Their answer crystallises into a versioned "Skill" card with the expert's name and a citation link. Cut to a "Teachers of the sprint" leaderboard filling with human names, each credited. Warm, human, sky-blue accent, hopeful tone. Overlay text: "The agent interviews the expert → an attributed, citable Skill."
```

### Scene 7 — Breakeven & Payoff
```
A tasteful Streamlit "Breakeven" chart. A value curve in analyst-hours draws itself left to right: it dips below zero first, then crosses the baseline and climbs into emerald green. Small callouts show hours handed back to named humans and a shift from "doing" to "reviewing". Clean, confident data-film look. Overlay text: "Value in analyst-hours — breakeven in sprints, not months."
```

### Scene 8 — Thesis + CTA
```
Return to the same four analysts around the table — now the empty chair is filled and the whole group faces forward, calm and in sync. Color settles into confident emerald green. A URL types itself onto a clean lower third. Warm, resolved, optimistic. Overlay text: "Try the live demo — huggingface.co/spaces/vijayarajks/day-9x".
```

### Closing Card
```
Static clean end card on deep slate, centered text, generous whitespace, emerald accent line. Text:
"day_9x
Live: huggingface.co/spaces/vijayarajks/day-9x
Source: github.com/vijayarajks639-afk/day_9x
Onboarding model paraphrased from Michael Watkins, 'The First 90 Days' (with attribution).
All data shown is synthetic."
No motion except a slow subtle fade-in.
```

---

## Optional: NEW scenes for the extended cut

### Scene 3b — Trust Ladder
```
A clean three-rung ladder visual for a single task class climbing upward. Rung 1 "SHADOW" glows indigo (drafts only, 100% reviewed). Rung 2 "GATED" glows sky blue (may act, human sign-off on every output). Rung 3 "AUTONOMOUS" glows emerald (acts, light audit sample). The task-class chip climbs one rung. Overlay text: "Trust ladder — revocable, per task class, earned by evidence."
```

### Scene 6b — The Two Clocks
```
Two elegant minimalist clock/ progress dials side by side on a slate background. Left dial marked "15-day sprints — pace the work." Right dial marked "9-day checkpoints — pace stakeholder communication." A small marker labelled "x = 1…10" advances; at x=10 a "90 days" label lights up. Calm, precise, confident. Overlay text: "day_9x = a stakeholder report every 9 days."
```
