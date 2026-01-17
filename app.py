import streamlit as st
from engine import screening_agent, risk_band_agent
from reasoning_agent import reasoning_agent
from audit_agent import log_screening
import firebase_admin
from firebase_admin import firestore

# ===============================
# PAGE CONFIG (ONCE)
# ===============================
st.set_page_config(
    page_title="RakshakPay",
    page_icon="🛡️",
    layout="wide"
)

# ===============================
# FIREBASE INIT
# ===============================
if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()

# ===============================
# HEADER (NATIVE — WILL NOT DISAPPEAR)
# ===============================
st.title("🛡️ RakshakPay")
st.caption("Pre-Payment Risk Shield for MSMEs")
st.divider()

# ===============================
# TABS
# ===============================
tab_dashboard, tab_screening, tab_history = st.tabs(
    ["📊 Dashboard", "🔍 Vendor Screening", "📁 Transaction History"]
)

# ===============================
# DASHBOARD
# ===============================
with tab_dashboard:
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Safe Transactions", 15)
    col2.metric("Amber Alerts", 7)
    col3.metric("High Risk Flags", 3)

    st.markdown(
        "➡ Go to the **Vendor Screening** tab to screen a new payment."
    )

# ===============================
# VENDOR SCREENING
# ===============================
with tab_screening:
    st.subheader("Vendor Payment Screening")

    beneficiary = st.text_input("Beneficiary / Vendor Name")
    country = st.text_input("Country")
    purpose = st.text_area("Payment Purpose")

    if st.button("Screen Payment"):
        matches = screening_agent(beneficiary, country)
        band, score = risk_band_agent(matches)
        explanation = reasoning_agent(matches, band)

        log_screening({
            "beneficiary": beneficiary,
            "country": country,
            "risk_band": band,
            "matches": matches,
            "explanation": explanation
        })

        if band == "GREEN":
            st.success("🟢 Safe to Pay")
        elif band == "AMBER":
            st.warning("🟠 Risk Alert – Verification Required")
        else:
            st.error("🔴 High Risk – Payment Should Be Held")

        st.markdown("### Match Details")
        st.json(matches)

        st.markdown("### AI Agent Explanation")

        st.write("**Reasoning Summary**")
        for line in explanation["reasoning_summary"]:
            st.write("•", line)

        st.write("**Decision Rationale**")
        st.write(explanation["decision_rationale"])

        st.write("**Confidence Assessment**")
        st.write(explanation["confidence_assessment"])

        st.write("**Recommended Actions**")
        for action in explanation["recommended_actions"]:
            st.write("•", action)

        st.write("**Counterfactual Analysis**")
        st.write(explanation["counterfactual_analysis"])

# ===============================
# TRANSACTION HISTORY
# ===============================
with tab_history:
    st.subheader("Transaction Screening History")

    records = db.collection("screenings").limit(20).stream()

    rows = []
    for r in records:
        d = r.to_dict()
        rows.append({
            "Vendor": d.get("beneficiary"),
            "Country": d.get("country"),
            "Risk": d.get("risk_band")
        })

    st.dataframe(rows, use_container_width=True)
