"""ai_act_check.py — where does Maestro-1 sit under the EU AI Act's
general-purpose AI (GPAI) rules? A planning aid, NOT legal advice.

Facts used: GPAI obligations apply from 2 August 2025; a model is
presumed to have systemic risk above 1e25 FLOPs of cumulative training
compute (rebuttable; the Commission can also designate models). Training
compute uses 6 x active params x tokens (Part 3); post-training adds a
little. Scale-up scenarios are hypothetical.
"""
THRESHOLD = 1e25
RUNS = {  # name: (active params, tokens)
    "Maestro-1 pre-training": (11.7e9, 10e12),
    "post-training + loop cycles (our estimate)": (11.7e9, 0.3e12),
}
BASE = ["technical documentation for the AI Office and downstream providers",
        "information and documentation for downstream providers integrating the model",
        "a policy to comply with EU copyright law, including opt-outs",
        "a public summary of the content used for training (Commission template)"]
SYSTEMIC = ["model evaluations including adversarial testing", "assess and mitigate systemic risks",
            "track and report serious incidents", "adequate cybersecurity protection"]

def main():
    total = 0
    for name, (n, d) in RUNS.items():
        f = 6 * n * d; total += f
        print(f"{name:44s} {f:.2e} FLOPs")
    print(f"{'cumulative':44s} {total:.2e} FLOPs = {total/THRESHOLD:.1%} of the 1e25 presumption threshold")
    print("obligations as a GPAI provider placing the model on the EU market:")
    for o in BASE: print("  -", o)
    for mult in (5, 10, 15):
        f = total * mult
        print(f"if a future run used {mult:2d}x the compute: {f:.1e} FLOPs -> "
              f"{'presumed systemic risk: add ' + str(len(SYSTEMIC)) + ' more duties and notify the Commission' if f > THRESHOLD else 'still below the threshold'}")

if __name__ == "__main__":
    main()
