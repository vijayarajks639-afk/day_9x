"""Central config + shared contract for day_9x — "The New Team Member".

An AI teammate's first 90 days, modelled mechanism-by-mechanism on Michael
Watkins' *The First 90 Days* (HBS Press, 2003). Onboarding framework adapted
with attribution; no book text is reproduced.

This module is the SHARED CONTRACT every other module builds against:
  - paths, embedding + retrieval knobs, model id, env-only key (reg_rag pattern)
  - the TASK_CLASS registry (agent / trust / evals / breakeven all key off this)
  - STARS scenarios (charter pacing)
  - trust states + promotion thresholds (trust state machine)
  - duration / checkpoint / sprint constants (charter sprint snapshot)
  - the value model (breakeven ledger)

ALL data in this project is SYNTHETIC. Zero PII, no real firm data.
"""
from __future__ import annotations

import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
# The synthetic world is generated at runtime, so DATA_DIR must be WRITABLE. Locally
# that's ROOT/data; in a read-only-app container (e.g. a HuggingFace Docker Space where
# /app is root-owned) set DAY9X_DATA_DIR to a writable path such as $HOME/data.
DATA_DIR = Path(os.environ.get("DAY9X_DATA_DIR") or (ROOT / "data"))  # gitignored artefacts
RUNBOOKS_DIR = DATA_DIR / "runbooks"   # the .md corpus the agent reads in shadow mode
SKILLS_DIR = DATA_DIR / "skills"       # coached "Skills" written by SMEs (cultural knowledge)


def ensure_dirs() -> None:
    for d in (DATA_DIR, RUNBOOKS_DIR, SKILLS_DIR):
        d.mkdir(parents=True, exist_ok=True)


# ── Version (see CHANGELOG.md; v0.1 frozen as git tag v0.1) ───────────────────
VERSION = "2.0"

# ── Determinism ───────────────────────────────────────────────────────────────
SEED = 90                              # same seed = same synthetic team every run


# ── Embeddings (local, free; fastembed/ONNX, no PyTorch — ~90MB on first run) ──
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ── Chunking (structure-aware; reg_rag_assistant pattern) ─────────────────────
CHUNK_CHARS = 700
CHUNK_OVERLAP = 120

# ── Retrieval ─────────────────────────────────────────────────────────────────
TOP_K = 4
MIN_SCORE = 0.30                       # abstain guardrail: below this, the agent refuses

# ── Generation (OPTIONAL — the whole app runs $0 without a key) ───────────────
AI_MODEL = "claude-haiku-4-5-20251001"
AI_MAX_TOKENS = 600


def get_key() -> str:
    """Anthropic key via env only (never committed). Empty = $0 deterministic fallback.

    GOVERNANCE: never set ANTHROPIC_API_KEY as a secret on a PUBLIC HuggingFace
    Space. The public demo runs keyless; the LLM layer is local-only enrichment.
    """
    return os.environ.get("ANTHROPIC_API_KEY", "")


# ── The Charter: STARS situations (Watkins ch.3) ──────────────────────────────
# Each situation adapts the onboarding PACE: how long the agent shadows before it
# is trusted with scoped work, and how aggressively autonomy is unlocked.
# shadow_frac / gated_frac are fractions of the total duration.
STARS = {
    "Start-up": {
        "label": "Start-up — building a new data-ops capability from scratch",
        "shadow_frac": 0.40, "gated_frac": 0.40,
        "note": "No runbooks yet; heavy learning + Skill authoring before scoped work.",
    },
    "Turnaround": {
        "label": "Turnaround — a DQ crisis backlog that must be cleared fast",
        "shadow_frac": 0.15, "gated_frac": 0.35,
        "note": "Pressure to produce; short shadow, fast scoped wins, tight escalation SLA.",
    },
    "Accelerating growth": {
        "label": "Accelerating growth — volume scaling faster than the team",
        "shadow_frac": 0.25, "gated_frac": 0.40,
        "note": "Scale the routine task classes first to relieve the humans.",
    },
    "Realignment": {
        "label": "Realignment — team in denial that the old process is failing",
        "shadow_frac": 0.35, "gated_frac": 0.40,
        "note": "Cultural learning dominates; encode 'how we really do it' as Skills.",
    },
    "Sustaining success": {
        "label": "Sustaining success — a healthy team preserving a high bar",
        "shadow_frac": 0.30, "gated_frac": 0.40,
        "note": "Protect the standard; slow, evidence-gated autonomy, no risky moves.",
    },
}
DEFAULT_STARS = "Turnaround"

# ── The Charter: duration + sprint snapshot ───────────────────────────────────
DEFAULT_DURATION_DAYS = 90             # Watkins: a planning milestone, not a law
MIN_DURATION_DAYS = 27                 # >= 3 checkpoints
MAX_DURATION_DAYS = 180
CHECKPOINT_DAYS = 9                    # x = duration / 9 → the "9-day report to stakeholders"
SPRINT_DAYS = 15                       # 90 days = exactly 6 sprints (the hiring manager's framing)


# ── Task classes (the shared spine: agent, trust, evals, breakeven key off this) ──
# baseline_minutes = analyst minutes to do the task by hand (value CREATED when the
#   agent's output is verified-correct).
# review_minutes  = analyst minutes to review one agent output (value CONSUMED while
#   the class is in SHADOW or GATED — the "cost of onboarding").
# audit_minutes   = light post-hoc audit minutes per task once AUTONOMOUS.
# pass_rate       = eval pass-rate on this class required to unlock GATED autonomy.
# min_verified    = verified GATED tasks required before AUTONOMOUS is offered.
TASK_CLASSES = {
    "runbook_qa": {
        "label": "Runbook Q&A",
        "desc": "Answer 'how do we do X here' from team runbooks, with citations.",
        "baseline_minutes": 12, "review_minutes": 4, "audit_minutes": 1,
        "pass_rate": 0.90, "min_verified": 8,
    },
    "ticket_triage": {
        "label": "Data-incident triage",
        "desc": "Classify & route an incoming data-quality incident ticket.",
        "baseline_minutes": 25, "review_minutes": 6, "audit_minutes": 2,
        "pass_rate": 0.85, "min_verified": 6,
    },
    "dq_rule_authoring": {
        "label": "DQ rule authoring",
        "desc": "Draft a data-quality rule + threshold for a critical data element.",
        "baseline_minutes": 240, "review_minutes": 35, "audit_minutes": 10,
        "pass_rate": 0.90, "min_verified": 4,
    },
    "recon_check": {
        "label": "Reconciliation variance check",
        "desc": "Explain a reconciliation break between two risk feeds.",
        "baseline_minutes": 180, "review_minutes": 25, "audit_minutes": 8,
        "pass_rate": 0.88, "min_verified": 4,
    },
}


# ── Trust states (Watkins ch.7: trust is a threshold issue — earned, per-class) ──
SHADOW = "SHADOW"          # drafts only, 100% reviewed, zero autonomy
GATED = "GATED"            # may act, but every output needs human approval
AUTONOMOUS = "AUTONOMOUS"  # acts within the class; light post-hoc audit sample
TRUST_STATES = (SHADOW, GATED, AUTONOMOUS)
AUDIT_SAMPLE_RATE = 0.20   # fraction of AUTONOMOUS tasks still audited


# ── The label contract (river_fish/explain.py pattern) ────────────────────────
# Every surfaced agent output carries one of these, so a reviewer always knows
# whether they are looking at a deterministic backbone or an LLM suggestion.
LABEL_LLM = "AI SUGGESTION — needs sign-off (not audit-grade)"
LABEL_DETERMINISTIC = "DETERMINISTIC — rule/retrieval backbone (audit-grade)"
LABEL_ABSTAIN = "ABSTAINED — not enough grounding; escalated to a human"


# ── ACL / least-privilege (v2.0 — the charter's resource scopes, ENFORCED) ────
# Arjuna's badge is not the master key: questions touching these topics are refused
# with a scope message and escalated to a human — never answered, never guessed.
ACL_BLOCKED_TOPICS = ["salary", "compensation", "pay band", "bonus",
                      "appraisal", "performance rating"]


# ── Watkins attribution (rendered in README + in-app footer) ──────────────────
WATKINS_CREDIT = (
    "Onboarding framework adapted from Michael D. Watkins, "
    "*The First 90 Days* (Harvard Business School Press, 2003). "
    "Frameworks paraphrased with attribution; no book text reproduced."
)
