import streamlit as st
from typing import Dict, Any, List

def pill(label: str, kind: str = "neutral"):
    colors = {
        "neutral": "#E5E7EB",
        "green": "#DCFCE7",
        "amber": "#FEF3C7",
        "red": "#FEE2E2",
    }
    st.markdown(
        f"<span style='background:{colors.get(kind, colors['neutral'])};"
        f"padding:4px 10px;border-radius:999px;font-size:12px;'>{label}</span>",
        unsafe_allow_html=True
    )

def flag_box(flags: List[Dict[str, Any]]):
    if not flags:
        st.success("No major risk flags triggered in the V0 rule-set.")
        return
    for f in flags:
        if f["level"] == "RED":
            st.error(f"🔴 {f['title']}")
        else:
            st.warning(f"🟠 {f['title']}")
        with st.expander("Why (report logic)"):
            for line in f.get("why", []):
                st.markdown(f"- {line}")

def outcome_card(title: str, value: str, why_lines: List[str] | None = None):
    st.markdown(f"**{title}**")
    st.write(value)
    if why_lines:
        with st.expander("Why?"):
            for line in why_lines:
                st.markdown(f"- {line}")
    st.divider()
