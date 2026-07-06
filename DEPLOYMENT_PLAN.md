# Deployment Plan — day_9x v2.0 (GitHub · Jira · Hugging Face)

The build is complete and verified (23/23 tests, eval contract holds, deck v2). This is the
publish plan across the three targets, and exactly what is needed from Vijay. Everything that
needs a credential is deliberately **not stored** — supply it at the moment of the step.

---

## 0. One decision to make first (blocks GitHub + HF)

**Which GitHub / HF identity do we publish under?**
- The handle `vijayarajks639-afk` was flagged as an application risk in the Anthropic prep
  (the `-afk` suffix reads oddly on a portfolio link a hiring manager will click).
- Recommendation: publish under a **clean handle** (e.g. `vijayaraj-shanmugam` or similar) that
  you'd be happy to put on a résumé and in a cover note. HF account `vijayarajks` already exists
  (the risk-dq-governance Space builds there).
- **Needed from you:** confirm the GitHub username and the HF username to use.

---

## 1. GitHub (story D9X-13)

**State now:** local git repo initialised; **v0.1 committed and tagged**; v2.0 committed on `main`
(after the review lands). No remote yet.

**Plan:**
1. You create an **empty** repo on GitHub (no README/……/.gitignore — the repo already has them):
   `https://github.com/<user>/day_9x` — Public.
2. I run (with your **PAT** provided at that moment, used once, never stored):
   ```bash
   git remote add origin https://github.com/<user>/day_9x.git
   git push -u origin main
   git push origin v0.1 v2.0        # publish both tags
   ```
3. Verify the repo renders `README.md` and the tags show under *Releases*.

**Needed from you:**
- The GitHub username (from step 0).
- A **fine-grained PAT** with `Contents: read/write` on that one repo, pasted at push time.

---

## 2. Jira (story tracking — D9X board)

**State now:** the board lives in-repo as the single source of truth (`JIRA_STATUS.md`), and there
is a ready-to-import **`JIRA_IMPORT.csv`** (25 stories D9X-2…D9X-26, statuses, sprints, AI worklogs).

**Two ways to land it in real Jira — pick one:**
- **(a) No credential — CSV import (recommended, 2 min):** in Jira Cloud → your project →
  *Filters / Board → Import issues from CSV* → upload `JIRA_IMPORT.csv` → map the columns
  (Issue Key, Type, Summary, Description, Sprint, Status, Epic Link, Time Spent). Done.
- **(b) API sync:** provide a Jira base URL + email + API token and I'll push via REST. Only worth
  it if you want live two-way sync; for a portfolio artifact, (a) is enough.

**Needed from you:** either nothing (do the CSV import yourself — I can screen-share the steps),
or a Jira URL + API token if you want me to push it.

---

## 3. Hugging Face Space (story D9X-14) — this is what produces the public URL

**State now:** `README.md` carries the HF Streamlit front-matter (`sdk: streamlit`,
`app_file: app.py`); `requirements.txt` pinned; app runs **$0/keyless**; `data/` is gitignored and
**regenerated on boot**. Full steps are in `DEPLOY_HF.md`.

**Plan:**
1. You create a **Public** Streamlit Space: `https://huggingface.co/spaces/<hf-user>/day-9x`.
2. I add the remote and push (with your **HF token** at that moment):
   ```bash
   git remote add hf https://huggingface.co/spaces/<hf-user>/day-9x
   git push hf main
   ```
3. Watch the *Logs* tab — first build ~2–3 min (fastembed downloads a ~90 MB ONNX model once).
   Banner should read **"⚪ $0 keyless mode"**; all five tabs live.

**Needed from you:**
- The HF username (from step 0).
- An **HF access token** (write scope), pasted at push time.

**GOVERNANCE — non-negotiable:** do **NOT** set `ANTHROPIC_API_KEY` as a secret on the public
Space. Anyone could trigger paid calls on your key. The app is built to run fully without it; the
optional Haiku layer is for local/private use only.

---

## The prototype URL

**There is no public URL yet — it comes into existence only after step 3 (the HF push).** It will be:

> `https://huggingface.co/spaces/<hf-user>/day-9x`

Until then, to view it **locally**:
```bash
cd Projects/day_9x
pip install -r requirements.txt
streamlit run app.py         # opens http://localhost:8501
```
(First local run also downloads the ~90 MB embedding model once.)

---

## Suggested order

1. **Decide the handle** (step 0).
2. **Wait for the review** (D9X-26 → `REVIEW_v2.md`); apply any fixes; final commit + tag `v2.0`.
3. **GitHub push** (PAT) → **HF deploy** (HF token) → **Jira CSV import**.
4. **Résumé + LinkedIn update** — once the review is clean and the URL is live (see below).

---

## Résumé / LinkedIn (queued — after review + live URL)

Once `REVIEW_v2.md` is clean and the Space URL is live, the résumé-worthy line writes itself. Draft
angle to tailor for the Anthropic Applied AI / Solutions-Architect application:

> Built **day_9x**, an interactive prototype that onboards an AI agent into a human scrum team as a
> governed "new hire" — RAG with citations + abstain, an **agent-led SME-interview loop that turns
> trapped tacit knowledge into versioned, attributed Skills**, per-task-class eval gates as the
> probation mechanism, and a breakeven model in analyst-hours. Runs $0/keyless; grounded in
> Watkins' *The First 90 Days* and a research-backed enterprise-AI POV.

I'll produce the polished résumé bullet(s) + a LinkedIn post + the one-line portfolio link when you
give the word (this is where the "one team, promotion-story" framing lands for a hiring manager).
