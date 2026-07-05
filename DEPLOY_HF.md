# Deploying day_9x to HuggingFace Spaces

## Prerequisites
- A HuggingFace account (free tier is sufficient)
- Git installed locally
- The `day_9x` repo checked out

## Steps

### 1. Create a new Space
1. Go to https://huggingface.co/spaces → **Create new Space**
2. Name it `day-9x` (or similar)
3. **SDK**: **Streamlit**
4. **Visibility**: **Public** (this app is built to run $0/keyless — see the governance note)
5. **Create Space** — HF creates a bare git repo for the Space

### 2. Add the Space as a git remote and push
```bash
git remote add hf https://huggingface.co/spaces/<your-username>/day-9x
git push hf main
```
HF reads `requirements.txt` and installs deps, then launches `app_file: app.py`
(declared in the YAML front-matter at the top of `README.md`).

### 3. Verify the build
- Open the Space URL and watch the **Logs** tab (first build ~2–3 min; fastembed downloads
  a ~90 MB ONNX model on first boot, then it's cached).
- App should start and show all 5 tabs. The banner should read **"⚪ $0 keyless mode"**.

---

## What the Space needs — and does NOT need

**Needed on a fresh checkout:**
- All `*.py` modules and `requirements.txt`. The synthetic world under `data/` is **gitignored**
  and **regenerated on boot** by `generate_data.ensure_generated()` (called in `app.boot()`), so a
  clean Space rebuilds it automatically. No data files are committed.

**NOT needed:**
- `data/` — gitignored; rebuilt on first run.
- Any API key (see below).

---

## CRITICAL GOVERNANCE NOTE — Public Spaces and API keys

**Do NOT set `ANTHROPIC_API_KEY` as a secret on a PUBLIC HuggingFace Space.**

Anyone who visits a public Space can trigger the app, which would make LLM calls against your
key and accumulate charges you cannot control.

The app is designed for exactly this: with **no key**, it runs in **$0 deterministic mode** —
the charter, shadow-mode retrieval + citations + abstain, scoped-task drafting, approval gates,
the coaching loop, the eval gates, and the breakeven curve **all work fully** using local
embeddings and rule-based logic. The optional Haiku layer (shadow-mode answer synthesis)
degrades gracefully and is labelled in the UI.

To enable the Haiku layer for your own private use:
- Set `ANTHROPIC_API_KEY` only on a **Private** Space, **or**
- Run locally: `export ANTHROPIC_API_KEY=<your-key> && streamlit run app.py`

---

## Dependency note
`fastembed` runs ONNX models with no PyTorch. First boot downloads a small (~90 MB) embedding
model to the Space cache; subsequent boots reuse it. No manual action needed.
