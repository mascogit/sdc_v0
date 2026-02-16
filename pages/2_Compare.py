import streamlit as st

from sdc.i18n import t, opt
from sdc.load import load_json
from sdc.schema import Scenario
from sdc.engine import evaluate

# Global language toggle
lang = st.sidebar.radio("Langue / Language", ["FR", "EN"], index=0)

RULES = load_json("data/rules.json")
PRESETS = load_json("data/presets.json")

st.title(t(lang, "app.compare_title"))
st.caption(t(lang, "app.compare_caption"))

# ✅ Remove English default — key must exist in both FR/EN
st.info(t(lang, "compare.disclaimer"))

names = list(PRESETS.keys())
if len(names) < 2:
    # ✅ Use existing ui key you already have in FR/EN (you used it elsewhere)
    st.error(t(lang, "ui.compare_need_two_presets"))
    st.stop()

# -----------------------------
# Translation helpers (UI-side) — reuse Compass logic
# -----------------------------
def tr_outcome(field: str, val: str) -> str:
    OUTCOME_VALS = {
        "debt_sustainability": {
            "Borderline": "outcome_vals.debt_sustainability.borderline",
            "Unsustainable": "outcome_vals.debt_sustainability.unsustainable",
            "Likely sustainable (conditional)": "outcome_vals.debt_sustainability.likely_sustainable_conditional",
        },
        "fiscal_realism": {
            "Challenging": "outcome_vals.fiscal_realism.challenging",
            "Politically fragile / historically rare": "outcome_vals.fiscal_realism.fragile_rare",
        },
        "social_risk": {
            "High": "outcome_vals.social_risk.high",
            "Contained (conditional)": "outcome_vals.social_risk.contained_conditional",
        },
        "financial_stability": {
            "Systemic": "outcome_vals.financial_stability.systemic",
            "Contained (conditional)": "outcome_vals.financial_stability.contained_conditional",
        },
    }
    key = OUTCOME_VALS.get(field, {}).get(val)
    return t(lang, key, default=val) if key else val


def localize_flags(flags: list[dict]) -> list[dict]:
    out = []
    for f in flags or []:
        ff = dict(f)
        fid = (ff.get("id") or "").lower()
        if fid:
            ff["title"] = t(lang, f"flags.{fid}.title", default=ff.get("title", ""))
            why = ff.get("why", []) or []
            ff["why"] = [
                t(lang, f"flags.{fid}.why_{i+1}", default=line)
                for i, line in enumerate(why)
            ]
        out.append(ff)
    return out


# -----------------------------
# Top selector row — enforce A != B
# -----------------------------
if "compare_left" not in st.session_state:
    st.session_state.compare_left = names[0]
if "compare_right" not in st.session_state:
    st.session_state.compare_right = names[1] if len(names) > 1 else names[0]

left_options = names
right_options = [n for n in names if n != st.session_state.compare_left]
if not right_options:
    right_options = names

sA_name, sB_name = st.columns([1, 1], gap="small")

with sA_name:
    left_name = st.selectbox(
        t(lang, "ui.compare_selector_a"),
        left_options,
        index=left_options.index(st.session_state.compare_left),
        key="compare_left",
        format_func=lambda k: opt(lang, "options.presets", k),
    )

with sB_name:
    if st.session_state.compare_right == left_name:
        st.session_state.compare_right = next(n for n in names if n != left_name)

    right_options = [n for n in names if n != left_name]
    right_name = st.selectbox(
        t(lang, "ui.compare_selector_b"),
        right_options,
        index=right_options.index(st.session_state.compare_right),
        key="compare_right",
        format_func=lambda k: opt(lang, "options.presets", k),
    )

# -----------------------------
# Build scenarios + evaluate
# -----------------------------
sA = Scenario(name=left_name, **PRESETS[left_name])
sB = Scenario(name=right_name, **PRESETS[right_name])

rA = evaluate(sA, RULES)
rB = evaluate(sB, RULES)

# Localize flags once (important: no English in FR)
rA_flags = localize_flags(rA.get("flags", []))
rB_flags = localize_flags(rB.get("flags", []))

st.divider()

# -----------------------------
# Helper UI blocks
# -----------------------------
def zone_badge(zone: str) -> str:
    return t(lang, "zones." + zone, default=zone)


def outcome_grid(outcomes: dict):
    c1, c2 = st.columns(2, gap="small")
    c3, c4 = st.columns(2, gap="small")

    with c1:
        with st.container(border=True):
            st.markdown(f"**{t(lang, 'outcomes.debt_sustainability')}**")
            st.write(tr_outcome("debt_sustainability", outcomes.get("debt_sustainability", "N/A")))

    with c2:
        with st.container(border=True):
            st.markdown(f"**{t(lang, 'outcomes.fiscal_realism')}**")
            st.write(tr_outcome("fiscal_realism", outcomes.get("fiscal_realism", "N/A")))

    with c3:
        with st.container(border=True):
            st.markdown(f"**{t(lang, 'outcomes.social_risk')}**")
            st.write(tr_outcome("social_risk", outcomes.get("social_risk", "N/A")))

    with c4:
        with st.container(border=True):
            st.markdown(f"**{t(lang, 'outcomes.financial_stability')}**")
            st.write(tr_outcome("financial_stability", outcomes.get("financial_stability", "N/A")))


def flags_block(flags: list[dict]):
    if not flags:
        st.success(t(lang, "ui.no_major_flags"))
        return

    def strip_prefix(s: str) -> str:
        for p in ["🟠 ", "🔴 ", "⚠️ "]:
            if s.startswith(p):
                return s[len(p):]
        return s

    for f in flags:
        level = f.get("level", "AMBER")
        title = strip_prefix(f.get("title", "Flag"))

        prefix = "🔴" if level == "RED" else "🟠"

        # One-click: title + severity on the expander itself
        with st.expander(f"{prefix} {title}", expanded=False):
            st.markdown(f"**{t(lang, 'ui.why_report_logic')}**")
            for line in (f.get("why", []) or []):
                st.markdown(f"- {line}")



# -----------------------------
# Two-column comparison
# -----------------------------
left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.subheader(f"A — {opt(lang,'options.presets', left_name)}")
    st.markdown(f"**{t(lang,'ui.zone')}:** {zone_badge(rA['zone'])}")

    # ✅ Remove EN default; use your existing ui.compare_position_fmt
    st.caption(
        f"{t(lang,'ui.compare_position')}: "
        + t(lang, "ui.compare_position_fmt").format(fiscal=rA["fiscal_stress"], social=rA["social_stress"])
    )

    st.markdown(f"### {t(lang, 'ui.outcomes')}")
    outcome_grid(rA["outcomes"])

    st.markdown(f"### {t(lang, 'ui.risk_flags')}")
    flags_block(rA_flags)

with right_col:
    st.subheader(f"B — {opt(lang,'options.presets', right_name)}")
    st.markdown(f"**{t(lang,'ui.zone')}:** {zone_badge(rB['zone'])}")

    st.caption(
        f"{t(lang,'ui.compare_position')}: "
        + t(lang, "ui.compare_position_fmt").format(fiscal=rB["fiscal_stress"], social=rB["social_stress"])
    )

    st.markdown(f"### {t(lang, 'ui.outcomes')}")
    outcome_grid(rB["outcomes"])

    st.markdown(f"### {t(lang, 'ui.risk_flags')}")
    flags_block(rB_flags)

st.divider()

# -----------------------------
# Meeting prompts
# -----------------------------
st.subheader(t(lang, "ui.assumptions_risks"))
st.caption(t(lang, "ui.placeholders_note"))

p1, p2 = st.columns(2, gap="large")

with p1:
    with st.container(border=True):
        st.markdown(f"**{t(lang,'ui.compare_selector_a')}: {opt(lang,'options.presets', left_name)}**")
        st.markdown(f"- {t(lang,'compare.prompt_true')}")
        st.markdown(f"- {t(lang,'compare.prompt_risk')}")

with p2:
    with st.container(border=True):
        st.markdown(f"**{t(lang,'ui.compare_selector_b')}: {opt(lang,'options.presets', right_name)}**")
        st.markdown(f"- {t(lang,'compare.prompt_true')}")
        st.markdown(f"- {t(lang,'compare.prompt_risk')}")
