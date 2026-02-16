from __future__ import annotations
from typing import Any, Dict, List, Tuple
from .schema import Scenario

def _match_when(s: Scenario, when: Dict[str, str]) -> bool:
    for k, v in when.items():
        if getattr(s, k) != v:
            return False
    return True

def compute_scores(s: Scenario, rules: Dict[str, Any]) -> Tuple[int, int]:
    base = rules["scoring"]["base"]
    weights = rules["scoring"]["weights"]

    fiscal = int(base["fiscal_stress"])
    social = int(base["social_stress"])

    # apply each dimension
    fiscal += weights["path"][s.path]["fiscal_stress"]
    social += weights["path"][s.path]["social_stress"]

    fiscal += weights["timing"][s.timing]["fiscal_stress"]
    social += weights["timing"][s.timing]["social_stress"]

    fiscal += weights["perimeter"][s.perimeter]["fiscal_stress"]
    social += weights["perimeter"][s.perimeter]["social_stress"]

    fiscal += weights["fiscal_intensity"][s.fiscal_intensity]["fiscal_stress"]
    social += weights["fiscal_intensity"][s.fiscal_intensity]["social_stress"]

    fiscal += weights["financing_mix"][s.financing_mix]["fiscal_stress"]
    social += weights["financing_mix"][s.financing_mix]["social_stress"]

    fiscal += weights["social_priority"][s.social_priority]["fiscal_stress"]
    social += weights["social_priority"][s.social_priority]["social_stress"]

    # clamp 0..100 for UI simplicity
    fiscal = max(0, min(100, fiscal))
    social = max(0, min(100, social))
    return fiscal, social

def compute_zone(fiscal: int, social: int, rules: Dict[str, Any]) -> str:
    z = rules["zones"]
    if fiscal <= z["green"]["max_fiscal"] and social <= z["green"]["max_social"]:
        return "GREEN"
    if fiscal <= z["amber"]["max_fiscal"] and social <= z["amber"]["max_social"]:
        return "AMBER"
    return "RED"

def triggered_flags(s: Scenario, rules: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    for f in rules.get("flags", []):
        if _match_when(s, f["when"]):
            out.append(f)
    # sort: RED first, then AMBER
    order = {"RED": 0, "AMBER": 1, "GREEN": 2}
    out.sort(key=lambda x: order.get(x["level"], 9))
    return out

def _has_flag(flags: List[Dict[str, Any]], flag_id: str) -> bool:
    return any(f["id"] == flag_id for f in flags)

def compute_outcomes(s: Scenario, flags: List[Dict[str, Any]], rules: Dict[str, Any]) -> Dict[str, str]:
    outcomes = {}
    for spec in rules.get("outcome_rules", []):
        outcome_name = spec["outcome"]
        label = None
        for rule in spec["logic"]:
            if "if_flag" in rule and _has_flag(flags, rule["if_flag"]):
                label = rule["label"]; break
            if "if" in rule:
                if all(getattr(s, k) == v for k, v in rule["if"].items()):
                    label = rule["label"]; break
            if "default" in rule:
                label = rule["default"]
        outcomes[outcome_name] = label or "N/A"
    return outcomes

def evaluate(s: Scenario, rules: Dict[str, Any]) -> Dict[str, Any]:
    fiscal, social = compute_scores(s, rules)
    zone = compute_zone(fiscal, social, rules)
    flags = triggered_flags(s, rules)
    outcomes = compute_outcomes(s, flags, rules)
    return {
        "fiscal_stress": fiscal,
        "social_stress": social,
        "zone": zone,
        "flags": flags,
        "outcomes": outcomes,
    }
