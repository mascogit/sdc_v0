import streamlit as st

from sdc.i18n import t
from sdc.load import load_json

# -----------------------------
# Global language toggle
# -----------------------------
lang = st.sidebar.radio("Langue / Language", ["FR", "EN"], index=0)

# -----------------------------
# Landing page
# -----------------------------
st.title(t(lang, "app.home_title"))
st.caption(t(lang, "app.home_caption"))

st.markdown(f"### {t(lang, 'app.home_info_title')}")

st.markdown(f"**{t(lang, 'app.home_purpose_title')}**")
st.markdown(t(lang, "app.home_purpose_p1"))
st.markdown(t(lang, "app.home_purpose_p2"))
st.markdown(t(lang, "app.home_purpose_p3"))
st.markdown(t(lang, "app.home_purpose_p4"))

st.markdown(f"**{t(lang, 'app.home_does_title')}**")
st.markdown(f"- {t(lang,'app.home_does_1')}")
st.markdown(f"- {t(lang,'app.home_does_2')}")
st.markdown(f"- {t(lang,'app.home_does_3')}")
st.markdown(f"- {t(lang,'app.home_does_4')}")
st.markdown(f"- {t(lang,'app.home_does_5')}")

st.markdown(f"**{t(lang, 'app.home_doesnot_title')}**")
st.markdown(f"- {t(lang,'app.home_doesnot_1')}")
st.markdown(f"- {t(lang,'app.home_doesnot_2')}")
st.markdown(f"- {t(lang,'app.home_doesnot_3')}")
st.markdown(f"- {t(lang,'app.home_doesnot_4')}")

st.markdown(f"**{t(lang, 'app.home_validation_title')}**")
st.markdown(t(lang, "app.home_validation_intro"))
st.markdown(f"- {t(lang,'app.home_validation_1')}")
st.markdown(f"- {t(lang,'app.home_validation_2')}")
st.markdown(f"- {t(lang,'app.home_validation_3')}")
st.markdown(f"- {t(lang,'app.home_validation_4')}")

st.markdown(f"**{t(lang, 'app.home_nav_title')}**")
st.markdown(t(lang, "app.home_nav_intro"))
st.markdown(f"- {t(lang,'app.home_nav_1')}")
st.markdown(f"- {t(lang,'app.home_nav_2')}")
st.markdown(f"- {t(lang,'app.home_nav_3')}")

st.info(t(lang, "app.home_footer"))
st.markdown(t(lang, "app.home_cta"))
