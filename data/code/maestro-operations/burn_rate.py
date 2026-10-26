"""burn_rate.py — SLO error budgets and multi-window burn-rate alerts.

SLO: 99.5% of agent requests succeed (non-5xx, under the latency limit)
over 30 days. Burn rate = error rate / allowed error rate. The Google SRE
Workbook suggests paging when the budget burns fast in both a long and a
short window (e.g. 14.4x over 1 h and 5 min). Error rates are SIMULATED.
"""
SLO = 0.995
ALLOWED = 1 - SLO
RULES = [("page", 14.4, "1h", "5m"), ("page", 6.0, "6h", "30m"), ("ticket", 1.0, "3d", "6h")]
WINDOWS = {  # scenario error rates per window during an incident
    "5m": 0.09, "30m": 0.05, "1h": 0.08, "6h": 0.02, "3d": 0.004,
}

def main():
    print(f"30-day budget: {ALLOWED:.1%} of requests = {ALLOWED*30*24*60:.0f} minutes of full outage")
    for sev, factor, long_w, short_w in RULES:
        bl = WINDOWS[long_w] / ALLOWED; bs = WINDOWS[short_w] / ALLOWED
        fire = bl >= factor and bs >= factor
        print(f"{sev:6s} if burn >= {factor:4.1f}x over {long_w:>3s} and {short_w:>3s}: "
              f"{bl:5.1f}x / {bs:5.1f}x -> {'FIRE' if fire else 'quiet'}")
    hours_left = 30 * 24 * ALLOWED / WINDOWS["1h"]
    print(f"at the current 1 h error rate the whole month's budget lasts {hours_left:.1f} hours")

if __name__ == "__main__":
    main()
