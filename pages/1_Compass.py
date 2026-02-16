import streamlit as st
import plotly.graph_objects as go

from sdc.i18n import t, opt
from sdc.load import load_json
from sdc.schema import Scenario
from sdc.engine import evaluate
from sdc.ui import flag_box

# -----------------------------
# Global language toggle
# -----------------------------
lang = st.sidebar.radio("Langue / Language", ["FR", "EN"], index=0)

RULES = load_json("data/rules.json")
PRESETS = load_json("data/presets.json")

# --- NEW: normalize default scenario name + display helper ---
CUSTOM_NAME = "(custom)"

def normalize_scenario_name():
    s = st.session_state.scenario
    if (not s.get("name")) or (s.get("name") == "Untitled scenario"):
        s["name"] = CUSTOM_NAME
    st.session_state.scenario = s

def display_scenario_name() -> str:
    name = st.session_state.scenario.get("name", CUSTOM_NAME)
    if name in PRESETS:
        return opt(lang, "options.presets", name)
    return opt(lang, "options.presets", CUSTOM_NAME)
# --- END NEW ---

st.title(t(lang, "app.compass_title"))
st.caption(
    t(
        lang,
        "ui.compass_caption_v0",
        default="V0: rule-based positioning (no model). Hover points to see state and parameters.",
    )
)

# -----------------------------
# Session state
# -----------------------------
if "scenario" not in st.session_state:
    st.session_state.scenario = Scenario().model_dump()

# NEW: normalize name right after init (prevents "Untitled scenario")
normalize_scenario_name()

# Force default/reset view to show reference only (no route/target)
if "reference_view" not in st.session_state:
    st.session_state.reference_view = True


def apply_preset(name: str):
    cfg = PRESETS[name]
    s = st.session_state.scenario
    s["name"] = name
    for k, v in cfg.items():
        s[k] = v
    st.session_state.scenario = s
    st.session_state.reference_view = False  # show route + target


def reset_scenario():
    st.session_state.scenario = Scenario().model_dump()
    normalize_scenario_name()              # NEW
    st.session_state.reference_view = True  # hide route + target



# --- Reset coordination (MUST be before widgets that use these keys) ---
if "do_reset" not in st.session_state:
    st.session_state.do_reset = False

# Apply reset BEFORE widgets are instantiated
PRESET_NONE = "__NONE__"
if st.session_state.do_reset:
    reset_scenario()
    st.session_state.preset_select = PRESET_NONE
    st.session_state.last_preset = PRESET_NONE
    st.session_state.do_reset = False



# Convenient order lists (stable)
PATHS = ["A_REPAY", "B_RESTRUCTURE"]
TIMINGS = ["IMMEDIATE", "GRADUAL", "DELAYED"]
PERIMETERS = ["EXTERNAL_ONLY", "EXTERNAL_PLUS_CFA_PARTIAL"]
FISCALS = ["MODERATE", "HIGH", "EXTREME"]
FIN_MIX = ["CONCESSIONAL_HEAVY", "UEMOA_HEAVY", "HIGH_INTEREST"]
SOCIALS = ["PROTECT", "NEUTRAL", "COMPRESS"]

# -----------------------------
# TOP ROW: Preset + Reset (auto-apply, no Apply button)
# -----------------------------
top1, top2 = st.columns([4, 1], gap="small")

# NOTE: use a stable internal token to avoid collisions with real preset names
PRESET_NONE = "__NONE__"
preset_options = [PRESET_NONE] + list(PRESETS.keys())

with top1:
    preset_name = st.selectbox(
        t(lang, "ui.scenario_preset"),
        preset_options,
        index=0,
        key="preset_select",
        format_func=lambda k: (
            t(lang, "ui.scenario_preset_none", default="— Choose a preset —")
            if k == PRESET_NONE
            else opt(lang, "options.presets", k)
        ),
    )

with top2:
    if st.button(t(lang, "ui.reset"), use_container_width=True):
        st.session_state.do_reset = True
        st.rerun()


# Auto-apply preset
if preset_name != PRESET_NONE and st.session_state.get("last_preset") != preset_name:
    st.session_state.last_preset = preset_name
    apply_preset(preset_name)
    st.rerun()

# Show active scenario name (display only, no input in V0)
st.caption(
    f"{t(lang,'ui.scenario_active')}: **{display_scenario_name()}**"
)

st.divider()

# -----------------------------
# SECOND ROW: Levers (horizontal)
# -----------------------------
c1, c2, c3, c4, c5, c6 = st.columns([1.4, 1.0, 1.2, 1.3, 1.3, 1.1], gap="small")
sdict = st.session_state.scenario

with c1:
    new_val = st.selectbox(
        t(lang, "ui.path"),
        PATHS,
        index=PATHS.index(sdict["path"]),
        format_func=lambda x: opt(lang, "options.path", x),
        key="lever_path",
    )
    if new_val != sdict["path"]:
        st.session_state.reference_view = False
    sdict["path"] = new_val

with c2:
    new_val = st.selectbox(
        t(lang, "ui.timing"),
        TIMINGS,
        index=TIMINGS.index(sdict["timing"]),
        format_func=lambda x: opt(lang, "options.timing", x),
        key="lever_timing",
    )
    if new_val != sdict["timing"]:
        st.session_state.reference_view = False
    sdict["timing"] = new_val

with c3:
    new_val = st.selectbox(
        t(lang, "ui.perimeter"),
        PERIMETERS,
        index=PERIMETERS.index(sdict["perimeter"]),
        format_func=lambda x: opt(lang, "options.perimeter", x),
        key="lever_perimeter",
    )
    if new_val != sdict["perimeter"]:
        st.session_state.reference_view = False
    sdict["perimeter"] = new_val

with c4:
    new_val = st.selectbox(
        t(lang, "ui.fiscal_intensity"),
        FISCALS,
        index=FISCALS.index(sdict["fiscal_intensity"]),
        format_func=lambda x: opt(lang, "options.fiscal_intensity", x),
        key="lever_fiscal",
    )
    if new_val != sdict["fiscal_intensity"]:
        st.session_state.reference_view = False
    sdict["fiscal_intensity"] = new_val

with c5:
    new_val = st.selectbox(
        t(lang, "ui.financing_mix"),
        FIN_MIX,
        index=FIN_MIX.index(sdict["financing_mix"]),
        format_func=lambda x: opt(lang, "options.financing_mix", x),
        key="lever_finmix",
    )
    if new_val != sdict["financing_mix"]:
        st.session_state.reference_view = False
    sdict["financing_mix"] = new_val

with c6:
    new_val = st.selectbox(
        t(lang, "ui.social_priority"),
        SOCIALS,
        index=SOCIALS.index(sdict["social_priority"]),
        format_func=lambda x: opt(lang, "options.social_priority", x),
        key="lever_social",
    )
    if new_val != sdict["social_priority"]:
        st.session_state.reference_view = False
    sdict["social_priority"] = new_val

st.session_state.scenario = sdict

# -----------------------------
# Build Scenario object + Evaluate
# -----------------------------
scenario = Scenario(
    name=st.session_state.scenario["name"],
    path=st.session_state.scenario["path"],
    timing=st.session_state.scenario["timing"],
    perimeter=st.session_state.scenario["perimeter"],
    fiscal_intensity=st.session_state.scenario["fiscal_intensity"],
    financing_mix=st.session_state.scenario["financing_mix"],
    social_priority=st.session_state.scenario["social_priority"],
)

res = evaluate(scenario, RULES)
fiscal = int(res["fiscal_stress"])
social = int(res["social_stress"])
zone = res["zone"]
zone_text = t(lang, "zones." + zone, default=zone)

# -----------------------------
# V0 translation helpers (UI-side, no engine changes)
# -----------------------------
def tr_flag_title(title: str) -> str:
    FLAG_TITLES = {
        "No-restructuring 'narrow corridor' (fragile feasibility)": "flags.narrow_corridor.title",
        "UEMOA systemic risk (doom loop / contagion)": "flags.uemoa_doom_loop.title",
    }
    key = FLAG_TITLES.get(title)
    return t(lang, key, default=title) if key else title


def tr_flag_why(line: str) -> str:
    FLAG_WHY = {
        "Avoiding restructuring requires unusually high and sustained fiscal effort plus favorable financing.": "flags.narrow_corridor.why_1",
        "Such combinations are historically rare and politically fragile.": "flags.narrow_corridor.why_2",
        "UEMOA-heavy refinancing increases crowding-out and bank–sovereign linkages.": "flags.uemoa_doom_loop.why_1",
        "Including CFA debt in restructuring raises contagion concerns (first-order constraint in report logic).": "flags.uemoa_doom_loop.why_2",
    }
    key = FLAG_WHY.get(line)
    return t(lang, key, default=line) if key else line


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

        fid = (ff.get("id") or "").lower()  # ✅ normalize ids

        if fid:
            ff["title"] = t(lang, f"flags.{fid}.title", default=ff.get("title", ""))
            why = ff.get("why", []) or []
            ff["why"] = [
                t(lang, f"flags.{fid}.why_{i+1}", default=line)
                for i, line in enumerate(why)
            ]

        out.append(ff)
    return out





flags_local = localize_flags(res.get("flags", []))

# -----------------------------
# HERO: Compass map (Plotly, interactive)
# -----------------------------
st.subheader(t(lang, "ui.compass_map", default="Compass map (decision space)"))
st.markdown(f"**{zone_text}**")
st.caption(
    t(
        lang,
        "ui.compass_caption_v0",
        default="V0: rule-based positioning (no model). Hover points to see state and parameters.",
    )
)

curr_xy = (fiscal, social)

# Thresholds from rules
z_rules = RULES["zones"]
gxf = z_rules["green"]["max_fiscal"]
gys = z_rules["green"]["max_social"]
axf = z_rules["amber"]["max_fiscal"]
ays = z_rules["amber"]["max_social"]

fig = go.Figure()


def shade(x0, y0, x1, y1, color):
    fig.add_shape(
        type="rect",
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        line=dict(width=0),
        fillcolor=color,
        layer="below",
    )


shade(0, 0, gxf, gys, "rgba(46, 204, 113, 0.14)")
shade(gxf, 0, axf, gys, "rgba(241, 196, 15, 0.12)")
shade(0, gys, gxf, ays, "rgba(241, 196, 15, 0.12)")
shade(gxf, gys, axf, ays, "rgba(241, 196, 15, 0.12)")
shade(axf, 0, 100, 100, "rgba(230, 126, 34, 0.10)")
shade(0, ays, 100, 100, "rgba(230, 126, 34, 0.10)")
shade(axf, ays, 100, 100, "rgba(231, 76, 60, 0.12)")

grid_style = dict(width=2, color="rgba(60,60,60,0.65)", dash="dash")
fig.add_shape(type="line", x0=gxf, y0=0, x1=gxf, y1=100, line=grid_style)
fig.add_shape(type="line", x0=axf, y0=0, x1=axf, y1=100, line=grid_style)
fig.add_shape(type="line", x0=0, y0=gys, x1=100, y1=gys, line=grid_style)
fig.add_shape(type="line", x0=0, y0=ays, x1=100, y1=ays, line=grid_style)


def midpt(a, b):
    return (a + b) / 2


xL, xM, xH = midpt(0, gxf), midpt(gxf, axf), midpt(axf, 100)
yL, yM, yH = midpt(0, gys), midpt(gys, ays), midpt(ays, 100)

grid_labels = [
    (xL, yL, ("grid.viable", "Viable")),
    (xM, yL, ("grid.austerity", "Austerity")),
    (xH, yL, ("grid.fiscal_stress", "Fiscal stress")),
    (xL, yM, ("grid.social_tension", "Social tension")),
    (xM, yM, ("grid.fragile", "Fragile")),
    (xH, yM, ("grid.high_risk", "High risk")),
    (xL, yH, ("grid.social_stress", "Social stress")),
    (xM, yH, ("grid.slowdown", "Slowdown")),
    (xH, yH, ("grid.crisis", "Crisis zone")),
]
for x, y, (key, dflt) in grid_labels:
    fig.add_annotation(
        x=x,
        y=y,
        text=t(lang, key, default=dflt),
        showarrow=False,
        font=dict(size=13, color="rgba(20,20,20,0.90)"),
        opacity=0.95,
    )

# -----------------------------
# Baseline pin + compass target (ONLY when not in reference view)
# -----------------------------
b = RULES.get("baseline", {})
base_xy = (int(b.get("fiscal_stress", 50)), int(b.get("social_stress", 50)))

base_label = t(lang, b.get("label_key", "baseline.label"), default="Baseline")
base_assumption = t(lang, b.get("assumption_key", "baseline.assumption"), default="")

axis_f = t(lang, "axis.fiscal", default="Fiscal stress")
axis_s = t(lang, "axis.social", default="Social/growth stress")

# Force reference view to show baseline point only (fix default + reset)
if st.session_state.get("reference_view", False):
    curr_xy = base_xy

show_delta = (curr_xy != base_xy)

# Baseline: single red pin icon (no dot duplication, avoids overlap)
fig.add_trace(
    go.Scatter(
        x=[base_xy[0]],
        y=[base_xy[1]],
        mode="text",
        text=["📍"],
        textfont=dict(size=22, color="rgba(200,30,30,0.95)"),
        hovertemplate=(
            f"<b>{base_label}</b><br>"
            f"{axis_f}: {base_xy[0]}/100<br>"
            f"{axis_s}: {base_xy[1]}/100<br>"
            f"<i>{base_assumption}</i>"
            "<extra></extra>"
        ),
        name="Baseline",
    )
)

if show_delta:
    # Route line (no arrowhead)
    fig.add_trace(
        go.Scatter(
            x=[base_xy[0], curr_xy[0]],
            y=[base_xy[1], curr_xy[1]],
            mode="lines",
            line=dict(width=4, color="rgba(50,50,50,0.85)"),
            hoverinfo="skip",
            name="Route",
        )
    )

    hover = (
        f"<b>{opt(lang,'options.presets', scenario.name)}</b><br>"
        f"{axis_f}: {curr_xy[0]}/100<br>"
        f"{axis_s}: {curr_xy[1]}/100<br>"
        f"{zone_text}<br><br>"
        f"{t(lang,'ui.path',default='Path')}: {opt(lang,'options.path',scenario.path)}<br>"
        f"{t(lang,'ui.timing',default='Timing')}: {opt(lang,'options.timing',scenario.timing)}<br>"
        f"{t(lang,'ui.perimeter',default='Perimeter')}: {opt(lang,'options.perimeter',scenario.perimeter)}<br>"
        f"{t(lang,'ui.financing_mix',default='Financing')}: {opt(lang,'options.financing_mix',scenario.financing_mix)}<br>"
        f"{t(lang,'ui.social_priority',default='Social priority')}: {opt(lang,'options.social_priority',scenario.social_priority)}"
    )

    # Target: compass icon only (no extra marker/text)
    fig.add_trace(
        go.Scatter(
            x=[curr_xy[0]],
            y=[curr_xy[1]],
            mode="text",
            text=["🧭"],
            textfont=dict(size=24, color="rgba(20,20,20,0.95)"),
            hovertemplate=hover + "<extra></extra>",
            name="Target",
        )
    )

fig.update_layout(
    height=600,
    margin=dict(l=45, r=45, t=10, b=45),
    xaxis=dict(range=[0, 100], title=axis_f, zeroline=False),
    yaxis=dict(range=[0, 100], title=axis_s, zeroline=False),
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

# Flags under the map (compact) — render here to guarantee full i18n
with st.expander(t(lang, "ui.risk_flags"), expanded=(len(flags_local) > 0)):
    if not flags_local:
        st.success(t(lang, "ui.no_major_flags"))
    else:
        for f in flags_local:
            lvl = f.get("level", "AMBER")
            title = f.get("title", "Flag")

            # Don't add emoji here — titles already contain 🟠/🔴 in i18n
            if lvl == "RED":
                st.error(title)
            else:
                st.warning(title)

            with st.expander(t(lang, "ui.why_report_logic")):
                for line in (f.get("why", []) or []):
                    st.markdown(f"- {line}")



st.divider()

# -----------------------------
# DECISION LOGIC (V0): compact explanation panel
# -----------------------------
st.subheader(t(lang, "ui.decision_logic", default="Decision logic (V0)"))

with st.container(border=True):
    st.markdown(f"**{t(lang,'ui.your_choices',default='Your choices')}**")

    chips = [
        (t(lang, "ui.path", default="Path"), opt(lang, "options.path", scenario.path)),
        (t(lang, "ui.timing", default="Timing"), opt(lang, "options.timing", scenario.timing)),
        (t(lang, "ui.perimeter", default="Perimeter"), opt(lang, "options.perimeter", scenario.perimeter)),
        (t(lang, "ui.fiscal_intensity", default="Fiscal intensity"), opt(lang, "options.fiscal_intensity", scenario.fiscal_intensity)),
        (t(lang, "ui.financing_mix", default="Financing"), opt(lang, "options.financing_mix", scenario.financing_mix)),
        (t(lang, "ui.social_priority", default="Social priority"), opt(lang, "options.social_priority", scenario.social_priority)),
    ]

    cc1, cc2, cc3 = st.columns(3, gap="small")
    cols = [cc1, cc2, cc3]
    for i, (k, v) in enumerate(chips):
        with cols[i % 3]:
            st.markdown(f"- **{k}:** {v}")

    st.divider()

    st.divider()

# 2) Triggered flags
st.markdown(f"**{t(lang,'ui.triggered_constraints')}**")

if not flags_local:
    st.success(t(lang, "ui.no_major_flags"))
else:
    for f in flags_local:
        lvl = f.get("level", "AMBER")
        title = f.get("title", "Flag")

        if lvl == "RED":
            st.error(title)
        else:
            st.warning(title)

        with st.expander(t(lang, "ui.why_report_logic")):
            for line in (f.get("why", []) or []):
                st.markdown(f"- {line}")



    st.divider()

    st.markdown(f"**{t(lang,'ui.result',default='Result')}**")
    st.markdown(f"- **{t(lang,'ui.zone',default='Zone')}:** {zone_text}")
    st.markdown(
        f"- **{t(lang,'axis.fiscal',default='Fiscal stress')}:** {fiscal}/100"
        f" · **{t(lang,'axis.social',default='Social/growth stress')}:** {social}/100"
    )

    outcomes = res.get("outcomes", {})
    ds = tr_outcome("debt_sustainability", outcomes.get("debt_sustainability", "N/A"))
    fr = tr_outcome("fiscal_realism", outcomes.get("fiscal_realism", "N/A"))

    st.markdown(f"- **{t(lang,'outcomes.debt_sustainability',default='Debt sustainability')}:** {ds}")
    st.markdown(f"- **{t(lang,'outcomes.fiscal_realism',default='Fiscal realism')}:** {fr}")

    st.divider()

    st.markdown(f"**{t(lang,'ui.what_to_change',default='What would change the result (V0 guidance)')}**")

    tips = []
    if scenario.timing == "DELAYED":
        tips.append(t(lang, "tips.timing", default="Try an earlier timing (Immediate/Gradual) to reduce refinancing cliff risk."))
    if scenario.financing_mix in ["UEMOA_HEAVY", "HIGH_INTEREST"]:
        tips.append(t(lang, "tips.financing", default="Shift financing toward concessional-heavy to reduce stress and risk flags."))
    if scenario.fiscal_intensity == "EXTREME":
        tips.append(t(lang, "tips.fiscal", default="Reduce fiscal intensity (High/Moderate) to lower feasibility and social stress."))
    if scenario.social_priority == "COMPRESS":
        tips.append(t(lang, "tips.social", default="Protect social priority to reduce social risk and legitimacy stress."))
    if scenario.perimeter == "EXTERNAL_PLUS_CFA_PARTIAL":
        tips.append(t(lang, "tips.perimeter", default="Avoid including CFA-denominated debt if contagion risk is a binding constraint."))

    if not tips:
        tips.append(t(lang, "tips.none", default="Current configuration is internally coherent in V0. Compare against the alternative path to see trade-offs."))

    for tip in tips[:4]:
        st.markdown(f"- {tip}")

# -----------------------------
# OUTCOMES: 4 cards across bottom
# -----------------------------
st.subheader(t(lang, "ui.outcomes", default="Outcomes"))

outcomes = res["outcomes"]


def tr_why_line(line: str) -> str:
    WHY_MAP = {
        "Derived from path choice, timing, financing mix, and major risk flags.": "why.debt_sustainability.1",
        "V0 reflects report logic (e.g., 'narrow corridor' for no-restructuring; higher risk with delay and expensive borrowing).": "why.debt_sustainability.2",
        "Extreme adjustment is historically rare and politically fragile (report logic).": "why.fiscal_realism.1",
        "Moderate/high are conditional on financing availability and credibility restoration.": "why.fiscal_realism.2",
        "Compression of social protection increases social risk.": "why.social_risk.1",
        "Extreme fiscal effort increases pro-cyclicality risk and pressure on public investment.": "why.social_risk.2",
        "UEMOA-heavy refinancing increases crowding-out and bank–sovereign linkages.": "why.financial_stability.1",
        "Including CFA debt in restructuring raises contagion concerns (first-order constraint in report logic).": "why.financial_stability.2",
    }
    key = WHY_MAP.get(line)
    return t(lang, key, default=line) if key else line


def outcome_card(title: str, value: str, why_lines: list[str]):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(value)
        exp_title = t(lang, "ui.why_report_logic", default=t(lang, "ui.why", default="Why?"))
        with st.expander(exp_title):
            for line in why_lines:
                st.markdown(f"- {tr_why_line(line)}")


WHY = {
    "Debt sustainability": [
        "Derived from path choice, timing, financing mix, and major risk flags.",
        "V0 reflects report logic (e.g., 'narrow corridor' for no-restructuring; higher risk with delay and expensive borrowing).",
    ],
    "Fiscal realism": [
        "Extreme adjustment is historically rare and politically fragile (report logic).",
        "Moderate/high are conditional on financing availability and credibility restoration.",
    ],
    "Growth & social risk": [
        "Compression of social protection increases social risk.",
        "Extreme fiscal effort increases pro-cyclicality risk and pressure on public investment.",
    ],
    "Financial stability (Senegal + UEMOA)": [
        "UEMOA-heavy refinancing increases crowding-out and bank–sovereign linkages.",
        "Including CFA debt in restructuring raises contagion concerns (first-order constraint in report logic).",
    ],
}

o1, o2, o3, o4 = st.columns(4, gap="small")

with o1:
    outcome_card(
        t(lang, "outcomes.debt_sustainability", default="Debt sustainability"),
        tr_outcome("debt_sustainability", outcomes.get("debt_sustainability", "N/A")),
        WHY["Debt sustainability"],
    )
with o2:
    outcome_card(
        t(lang, "outcomes.fiscal_realism", default="Fiscal realism"),
        tr_outcome("fiscal_realism", outcomes.get("fiscal_realism", "N/A")),
        WHY["Fiscal realism"],
    )
with o3:
    outcome_card(
        t(lang, "outcomes.social_risk", default="Growth & social risk"),
        tr_outcome("social_risk", outcomes.get("social_risk", "N/A")),
        WHY["Growth & social risk"],
    )
with o4:
    outcome_card(
        t(lang, "outcomes.financial_stability", default="Financial stability (Senegal + UEMOA)"),
        tr_outcome("financial_stability", outcomes.get("financial_stability", "N/A")),
        WHY["Financial stability (Senegal + UEMOA)"],
    )
