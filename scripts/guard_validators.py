"""guard_validators.py — fail if any required validator stops running in build.py --check.

The list lives in loops/required-validators.txt. Removing a name there, or a call in
build.py, shows up in review; this script makes the second one fail CI.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
need = [l.strip() for l in (ROOT / "loops/required-validators.txt").read_text().splitlines() if l.strip() and not l.startswith("#")]
src = (ROOT / "scripts/build.py").read_text(encoding="utf-8")
lines = [l for l in src.splitlines() if l.strip().startswith(("problems = broken_links(files)", "problems += broken_links(files)"))]
missing = [v for v in need if not lines or any(v + "(" not in l for l in lines)]
print("validators guarded:", len(need), "missing:", missing or "none")
sys.exit(1 if missing or len(lines) < 2 else 0)
