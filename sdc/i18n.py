from __future__ import annotations
from typing import Any, Dict
from .load import load_json

_CACHE: Dict[str, Dict[str, Any]] = {}

def get_dict(lang: str) -> Dict[str, Any]:
    lang = (lang or "FR").upper()
    if lang not in _CACHE:
        if lang == "EN":
            _CACHE[lang] = load_json("data/i18n_en.json")
        else:
            _CACHE[lang] = load_json("data/i18n_fr.json")
    return _CACHE[lang]

def t(lang: str, key: str, default: str | None = None) -> str:
    d = get_dict(lang)
    cur: Any = d
    for part in key.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default if default is not None else key
    return str(cur)

def opt(lang: str, group: str, code: str) -> str:
    # group examples: options.path, options.timing...
    return t(lang, f"{group}.{code}", default=code)
