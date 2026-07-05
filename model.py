def calculate_score(data):
    income = data["income"]
    expenses = data["expenses"]
    savings = data["savings"]
    emi = data["emi"]
    upi_txns = data["upi_txns"]
    missed_payments = data["missed_payments"]

    # 1. Income stability (20 pts)
    income_score = min(20, int((income / 100000) * 20))

    # 2. Savings ratio (25 pts)
    savings_ratio = savings / income if income > 0 else 0
    savings_score = min(25, int(savings_ratio * 100))

    # 3. Spending habit (20 pts)
    expense_ratio = expenses / income if income > 0 else 1
    spending_score = min(20, int((1 - expense_ratio) * 20))

    # 4. Debt load / EMI burden (20 pts)
    emi_ratio = emi / income if income > 0 else 1
    debt_score = min(20, int((1 - emi_ratio) * 20))

    # 5. UPI behaviour (10 pts)
    upi_score = min(10, int(upi_txns / 5))

    # 6. Payment history (5 pts)
    payment_score = max(0, 5 - (missed_payments * 2))

    total = income_score + savings_score + spending_score + debt_score + upi_score + payment_score
    total = max(0, min(100, total))

    breakdown = {
        "Income stability": income_score * 5,
        "Savings ratio": savings_score * 4,
        "Spending habit": spending_score * 5,
        "Debt load": debt_score * 5,
        "UPI behaviour": upi_score * 10,
        "Payment history": payment_score * 20
    }

    return total, breakdown


def get_risk_flags(data, score):
    flags = []
    income = data["income"]
    emi = data["emi"]
    savings = data["savings"]
    missed_payments = data["missed_payments"]

    if emi / income > 0.4:
        flags.append("⚠ High EMI burden — EMIs exceed 40% of income")
    else:
        flags.append("✅ EMI burden is within safe limits")

    if savings / income < 0.2:
        flags.append("⚠ Low savings rate — below recommended 20%")
    else:
        flags.append("✅ Savings rate is healthy")

    if missed_payments > 0:
        flags.append(f"⚠ {missed_payments} missed payment(s) detected")
    else:
        flags.append("✅ No missed payments in last 6 months")

    return flags


def get_product_suggestions(score):
    if score >= 70:
        return [
            "🏦 IDBI Tax-Saver FD — Grow your savings + save tax under Section 80C",
            "📈 IDBI Mutual Fund SIP — Start investing for long-term wealth creation",
            "💳 IDBI Platinum Credit Card — Rewards for your healthy financial profile"
        ]
    elif score >= 40:
        return [
            "💰 IDBI Suvidha Savings Plan — Auto-save feature to boost savings ratio",
            "🔄 EMI Restructuring Loan — Reduce monthly EMI burden at lower interest",
            "📊 IDBI Financial Advisory — Free consultation to improve your score"
        ]
    else:
        return [
            "🆘 IDBI Debt Consolidation Loan — Combine all debts into one manageable EMI",
            "📞 IDBI Financial Wellness Program — Personalized recovery plan",
            "💳 IDBI Secured Credit Card — Rebuild credit with a fixed deposit backed card"
        ]
