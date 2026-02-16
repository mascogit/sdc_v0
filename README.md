# 🧭 Strategic Debt Compass (SDC) — Expert Validation Prototype (V0)

🔗 **Live application**  
https://strategic-debt-compass.streamlit.app/

---

## Overview

The **Strategic Debt Compass (SDC)** is a decision-oriented interface derived strictly from:

**Ndiaye, A. & Kessler, M. (2026)**  
*Une boussole stratégique pour traverser la crise de la dette du Sénégal*  
Finance for Development Lab, Note d’analyse n°31 (January 2026)

📄 **Full report (PDF)**  
http://findevlab.org/wp-content/uploads/2026/01/FDL_Note-31_Une-boussole-strategique-pour-naviguer-dans-la-crise-de-la-dette-du-Senegal_Janv26.pdf

This prototype translates the report’s strategic reasoning into an interactive decision space.

> **V0 is designed for expert validation — not forecasting.**

---

## Purpose

SDC converts the report’s analytical framework into a structured governance interface that:

- Encodes the two strategic paths discussed in the note
- Makes explicit the key policy levers
- Highlights structural constraints (UEMOA/WAEMU, refinancing pressure, feasibility limits)
- Maps policy combinations into a fiscal/social stress decision space
- Provides traceable “Why?” explanations grounded in report logic

All outputs are **rule-based interpretations** derived strictly from the report.  
No additional modeling assumptions are introduced.

---

## What SDC Does (V0)

- Formalizes strategic options into navigable decision paths
- Makes constraint logic explicit
- Anchors rules to report sections and citations
- Supports scenario comparison
- Enhances transparency through traceability

---

## What SDC Does NOT Do (V0)

- It does not simulate macroeconomic trajectories
- It does not estimate new debt paths
- It does not forecast GDP, debt, or fiscal balances
- It does not introduce assumptions beyond the report

> This is a governance communication tool — not a predictive model.

---

## Validation Focus

V0 is designed to test:

- Whether strategic paths are correctly represented
- Whether levers are appropriately structured
- Whether constraint flags are faithful to the report
- Whether the decision-space representation is defensible
- Whether traceability (rule → section → citation) is sufficiently rigorous

---

## Navigation

Use the left sidebar to explore:

- 🧭 **Compass** — Main decision console
- ⚖️ **Compare** — Side-by-side scenario analysis
- 🔎 **Report Foundations** — Traceability layer (rule → section → citation)

---

## Architecture (Rule-Based)

The system is fully rule-based.

No new econometric or simulation models are used.

### Editable configuration files

- data/presets.json        # Scenario presets
- data/rules.json          # Scoring and constraint flags
- data/traceability.json   # Report anchors and citation layer

---

## Run Locally


- pip install -r requirements.txt
- streamlit run app.py

---

### Positioning

SDC is an experimental governance interface exploring how complex policy reasoning can be:
- Structured
- Made transparent
- Rendered navigable
- Anchored to published analysis
It represents an interpretive layer over a policy note — not an independent analytical model.

---

### Author

Interface prototype (V0) developed by
Dr El Hadji Moudo Macina (2026)
- PhD in Public Administration (University of Lausanne)
- Graduate in Public Policy & Development Economics (Toulouse School of Economics)
- Experience: World Health Organization, Gavi
- Focus: Governance-oriented decision systems and Public Policy 

