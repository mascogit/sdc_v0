import json
from pathlib import Path

# Always resolve project root (one level above /sdc)
ROOT = Path(__file__).resolve().parent.parent

rules_path = ROOT / "data" / "rules.json"
fr_path = ROOT / "data" / "i18n_fr.json"

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8-sig"))

R = load_json(rules_path)
FR = load_json(fr_path)

rule_flags = {f.get("id", "").lower(): f for f in R.get("flags", [])}
fr_flags = FR.get("flags", {})

missing = [k for k in rule_flags.keys() if k and k not in fr_flags]

print("Missing flag ids in FR:", missing)

print("---")
for k in missing:
    f = rf[k]
    print(f'"{k}": {{')
    print(f'  "title": "{f.get("title","")}",')
    why = f.get("why", []) or []
    for i, line in enumerate(why, 1):
        print(f'  "why_{i}": "{line}",')
    print("},\n")
