import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import calculate_score, get_risk_flags, get_product_suggestions
from chatbot import get_ai_response

st.set_page_config(page_title="FinNova - Financial Health Score", page_icon="🏦", layout="wide")

st.markdown("<h1 style='color:#1a3a5c;'>🏦 FinNova — Financial Health Score</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:gray;'>IDBI Innovate 2026 | AI-powered Financial Health Analysis</p>", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.header("📋 Enter Your Financial Data")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=30000)
    savings = st.number_input("Monthly Savings (₹)", min_value=0, value=8000)
    emi = st.number_input("Total EMI per Month (₹)", min_value=0, value=12000)
    upi_txns = st.number_input("UPI Transactions (last month)", min_value=0, value=45)
    missed_payments = st.number_input("Missed Payments (last 6 months)", min_value=0, value=0)
    analyze = st.button("🔍 Calculate My Score", use_container_width=True)

if analyze:
    user_data = {
        "income": income, "expenses": expenses,
        "savings": savings, "emi": emi,
        "upi_txns": upi_txns, "missed_payments": missed_payments
    }

    score, breakdown = calculate_score(user_data)
    flags = get_risk_flags(user_data, score)
    products = get_product_suggestions(score)

    col1, col2, col3 = st.columns(3)
    with col1:
        color = "green" if score >= 70 else "orange" if score >= 40 else "red"
        st.markdown(f"<h2 style='color:{color};'>Score: {score}/100</h2>", unsafe_allow_html=True)
        tag = "Good 🟢" if score >= 70 else "Average 🟡" if score >= 40 else "Poor 🔴"
        st.markdown(f"**Status: {tag}**")

    with col2:
        st.markdown("**📊 Score Breakdown**")
        for k, v in breakdown.items():
            st.progress(v/100, text=f"{k}: {v}/100")

    with col3:
        st.markdown("**⚠️ Risk Flags**")
        for f in flags:
            st.warning(f) if "High" in f or "Low" in f else st.success(f)

    st.divider()
    st.markdown("**🏦 Recommended IDBI Products**")
    for p in products:
        st.info(p)

    st.divider()
    st.markdown("### 🤖 Ask FinNova AI")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Hi! Your Financial Health Score is {score}/100. How can I help you improve it?"
        })

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask about your financial health..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = get_ai_response(prompt, score, breakdown)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

else:
    st.info("👈 Enter your financial details in the sidebar and click 'Calculate My Score'")
