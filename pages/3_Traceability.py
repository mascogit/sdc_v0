import streamlit as st

from sdc.i18n import t
from sdc.load import load_json

# -----------------------------
# Global language toggle
# -----------------------------
lang = st.sidebar.radio("Langue / Language", ["FR", "EN"], index=0)

TRACE = load_json("data/traceability.json")

# -----------------------------
# Page header
# -----------------------------
st.title(t(lang, "app.trace_title", default="🔎 Report foundations"))
st.caption(
    t(
        lang,
        "app.trace_caption",
        default="Why the Compass logic is defensible (V0: section-level references; V1: citation-grade excerpts).",
    )
)

# -----------------------------
# Intro (single block, no duplicates)
# -----------------------------
st.markdown(
    f"""
{t(lang, "trace.intro", default="This page is a transparency layer: it shows where each Compass rule comes from in the report.")}

**{t(lang, "trace.citation_label", default="Source")}**  
Ndiaye, A. and Kessler, M. (2026), *A Strategic Compass for Navigating Senegal's Debt Crisis*, Finance for Development Lab, Policy Note 31 (January 2026).

- **{t(lang, "trace.left_label", default="Left")}**: {t(lang, "trace.left_desc", default="Relevant report sections (what to read)")}
- **{t(lang, "trace.right_label", default="Right")}**: {t(lang, "trace.right_desc", default="Internal logic key used to link rules ↔ explanations (technical, for maintainers)")}

_{t(lang, "trace.note", default="Note: The report is in French; we keep section titles verbatim to preserve citation fidelity.")}_
"""
)

st.divider()

# -----------------------------
# Display mode toggle (V0 vs V1)
# -----------------------------
mode = st.radio(
    t(lang, "trace.mode_label", default="Mode d’affichage" if lang == "FR" else "Display mode"),
    [
        t(lang, "trace.mode_v0", default="V0 — Sections (quoi relire)" if lang == "FR" else "V0 — Sections (what to read)"),
        t(lang, "trace.mode_v1", default="V1 — Citations (page + extrait)" if lang == "FR" else "V1 — Citations (page + excerpt)"),
    ],
    index=0,
    horizontal=True,
)


st.divider()

# -----------------------------
# Anchors cards
# -----------------------------
anchors = TRACE.get("anchors", [])

for a in anchors:
    with st.container(border=True):
        left, right = st.columns([3, 1], gap="large")

        with left:
            st.subheader(a.get("title", ""))

            # V0: section-level references
            if mode.startswith("V0") or "Sections" in mode or "sections" in mode:
                refs = a.get("report_refs", [])
                if refs:
                    st.markdown(f"**{t(lang, 'trace.sections_label', default='Report sections (V0)')}**")
                    for r in refs:
                        st.markdown(f"- {r}")
                else:
                    st.info(t(lang, "trace.no_refs", default="No references listed yet (V0)."))

            # V1: citation-grade excerpts
            else:
                cits = a.get("citations", [])
                if cits:
                    st.markdown(f"**{t(lang, 'trace.citations_label', default='Citations (V1)')}**")

                    for i, c in enumerate(cits, start=1):
                        page = c.get("page", "?")
                        quote_fr = (c.get("quote_fr", "") or "").strip()

                        # Optional EN support if you later add quote_en
                        quote_en = (c.get("quote_en", "") or "").strip()
                        quote = quote_fr if lang == "FR" else (quote_en or quote_fr)

                        label = t(
                            lang,
                            "trace.citation_item",
                            default=f"Citation {i} — p. {page}",
                        )
                        with st.expander(f"{label}"):
                            st.markdown(f"_{quote}_")
                else:
                    st.warning(
                        t(
                            lang,
                            "trace.no_citations",
                            default="No citations available yet (V1). Add page + verbatim excerpts in traceability.json.",
                        )
                    )

        with right:
            st.markdown(f"**{t(lang, 'trace.logic_key_label', default='Compass logic key')}**")
            st.code(a.get("id", ""), language="text")

            tags = a.get("tags", [])
            if tags:
                st.markdown(f"**{t(lang, 'trace.tags_label', default='Tags')}**")
                st.write(" · ".join(tags))

st.divider()

# -----------------------------
# Footer
# -----------------------------
st.caption(
    t(
        lang,
        "trace.footer",
        default=f"{len(anchors)} item(s). V0 shows sections; V1 shows citation-grade excerpts when available.",
    )
)
