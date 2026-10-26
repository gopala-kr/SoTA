"""release_check.py — the release gate for a model version.

Every item must exist and be signed before Maestro-1 ships to anyone.
The manifest below is the SCENARIO state at the first review: two items
are missing, so the answer is no.
"""
REQUIRED = {
    "model_card": "model card: intended use, limits, evaluation results with CIs",
    "eval_report": "evaluation report from the harness (Part 12), contamination checked",
    "safety_report": "safety evaluation and red-team summary (Part 13)",
    "data_summary": "public training-content summary (EU template) and data manifest",
    "copyright_policy": "copyright and opt-out policy",
    "gate_log": "loop gate decisions since the last release (Part 11)",
    "incident_process": "incident contact, severity levels, response times",
    "partner_signoff": "design partners reviewed on their own data",
    "rollback_plan": "previous version kept serving; rollback tested",
}
MANIFEST = {
    "model_card": {"done": True, "signed": "Gopala"},
    "eval_report": {"done": True, "signed": "Gopala"},
    "safety_report": {"done": True, "signed": "external red team + Gopala"},
    "data_summary": {"done": False, "signed": ""},
    "copyright_policy": {"done": True, "signed": "counsel"},
    "gate_log": {"done": True, "signed": "Gopala"},
    "incident_process": {"done": True, "signed": "Gopala"},
    "partner_signoff": {"done": True, "signed": ""},
    "rollback_plan": {"done": True, "signed": "Gopala"},
}

def main():
    missing = []
    for k, desc in REQUIRED.items():
        m = MANIFEST.get(k, {})
        ok = m.get("done") and m.get("signed")
        print(f"{'OK  ' if ok else 'MISS'} {desc}" + ("" if ok else f"  ({'not done' if not m.get('done') else 'not signed'})"))
        if not ok: missing.append(k)
    print("RELEASE: " + ("GO" if not missing else f"NO-GO, {len(missing)} item(s) open: {', '.join(missing)}"))

if __name__ == "__main__":
    main()
