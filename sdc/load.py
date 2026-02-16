import json
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]

def load_json(rel_path: str) -> Dict[str, Any]:
    p = ROOT / rel_path
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
