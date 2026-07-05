"""D9X-8 — The probation review: eval harness + promotion gates.

Adapts the river_fish/eval.py pattern (hand-authored golden truth, guardrail
checks, honest PASS/FAIL reporting) to grade the AI teammate per task class.
A class's gate must be green before GATED work is unlocked, and green + enough
verified outputs before AUTONOMOUS is even offered. Evals, not vibes.

Two golden cases are deliberately CULTURE-dependent (the Thursday rule; the 2%
convention): they FAIL until an SME coaches the unwritten-rules Skill into the
corpus — the demo's core teaching moment. So a fresh, uncoached run reports two
classes below their gates BY DESIGN; a coached run must be all green.

Run:  python evals.py            (report current state; exit 1 if any gate red)
      python evals.py --coached  (coach the Skill first; all gates must be green)
"""
from __future__ import annotations

import json
import sys

import config


def _load_golden() -> dict:
    return json.loads((config.DATA_DIR / "golden_set.json").read_text(encoding="utf-8"))


def _grade_qa(teammate, case) -> tuple[bool, str]:
    out = teammate.answer(case["q"])
    if case.get("abstain"):
        return (out.abstained, "abstained as required" if out.abstained
                else "answered an out-of-scope question (hallucination risk)")
    if out.abstained:
        return False, "abstained on an answerable question"
    text_ok = all(tok.lower() in out.text.lower() for tok in case["must_include"])
    cite_ok = any(case["must_cite"] in c for c in out.citations)
    if text_ok and cite_ok:
        return True, ""
    return False, ("missing tokens " + str(case["must_include"]) if not text_ok
                   else f"did not cite {case['must_cite']}")


def _grade_task(teammate, cls, case) -> tuple[bool, str]:
    task = dict(case, cls=cls, id=case.get("break_id", "eval"))
    out = teammate.attempt(task)
    truth = case["truth"]
    if truth.get("escalate"):
        return (bool(out.escalation), "escalated as required" if out.escalation
                else "guessed instead of escalating on an unknown system")
    if out.escalation:
        return False, "escalated on a case it should handle"
    if "verdict" in truth:
        ok = truth["verdict"] in out.text
        return ok, "" if ok else f"expected verdict {truth['verdict']}"
    missing = [t for t in truth.get("must_include", [])
               if t.lower() not in out.text.lower()]
    if "severity" in truth:
        missing += [t for t in (truth["severity"], truth["route"]) if t not in out.text]
    return (not missing, "" if not missing else f"missing {missing}")


def run_evals(teammate) -> dict:
    """Grade every class. Returns cls -> {passed, total, rate, gate, green, details}."""
    golden = _load_golden()
    results = {}
    for cls, cases in golden.items():
        details = []
        for case in cases:
            ok, note = (_grade_qa(teammate, case) if cls == "runbook_qa"
                        else _grade_task(teammate, cls, case))
            desc = case.get("q") or case.get("detail") or case.get("break_id") \
                or f"{case.get('cde')}/{case.get('dimension')}"
            details.append({"case": desc, "ok": ok, "note": note,
                            "culture": case.get("culture", False)})
        passed = sum(d["ok"] for d in details)
        gate = config.TASK_CLASSES[cls]["pass_rate"]
        rate = passed / len(details)
        results[cls] = {"passed": passed, "total": len(details), "rate": rate,
                        "gate": gate, "green": rate >= gate, "details": details}
    return results


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    import generate_data
    import rag
    from agent import Teammate
    generate_data.ensure_generated()

    coached = "--coached" in sys.argv
    index = rag.Index().build()
    if coached:
        import board
        skills = board.coach_unwritten_rules(index)
        print(f"Coached Skills in corpus: {skills}\n")

    results = run_evals(Teammate(index))
    all_green = True
    for cls, r in results.items():
        mark = "GREEN" if r["green"] else "RED"
        all_green &= r["green"]
        print(f"[{mark}] {config.TASK_CLASSES[cls]['label']}: "
              f"{r['passed']}/{r['total']} = {r['rate']:.0%} (gate {r['gate']:.0%})")
        for d in r["details"]:
            if not d["ok"]:
                tag = "  (culture case — coach the Skill)" if d["culture"] else ""
                print(f"       FAIL: {d['case']} — {d['note']}{tag}")
    print("\nProbation review:", "ALL GATES GREEN — promotion may be offered."
          if all_green else "gates red — hold; coach Skills / keep reviewing.")
    return 0 if all_green else 1


if __name__ == "__main__":
    sys.exit(main())
