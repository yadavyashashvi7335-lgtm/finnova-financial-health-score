import os

def get_ai_response(user_question, score, breakdown):
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        score_context = f"""You are FinNova, an AI financial health advisor for IDBI Bank.
The user's Financial Health Score is {score}/100.
Score breakdown:
- Income stability: {breakdown.get('Income stability', 0)}/100
- Savings ratio: {breakdown.get('Savings ratio', 0)}/100
- Spending habit: {breakdown.get('Spending habit', 0)}/100
- Debt load: {breakdown.get('Debt load', 0)}/100
- UPI behaviour: {breakdown.get('UPI behaviour', 0)}/100
- Payment history: {breakdown.get('Payment history', 0)}/100
Answer the user's question in a friendly, simple, helpful way. Under 100 words."""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": score_context},
                {"role": "user", "content": user_question}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    except Exception:
        return fallback_response(user_question, score, breakdown)


def fallback_response(question, score, breakdown):
    question = question.lower()

    if "savings" in question or "save" in question:
        if breakdown.get('Savings ratio', 0) < 50:
            return "Your savings ratio is below target. Try saving at least 20% of your income every month."
        return "Your savings habit is good! Consider investing in IDBI Tax-Saver FD or SIP."

    elif "emi" in question or "debt" in question or "loan" in question:
        if breakdown.get('Debt load', 0) < 50:
            return "Your EMI burden is high. Try to prepay smaller loans first to reduce monthly obligations."
        return "Your debt load is manageable. Keep maintaining timely payments."

    elif "score" in question or "improve" in question:
        if score < 40:
            return f"Your score is {score}/100. Focus on reducing EMIs and increasing monthly savings."
        elif score < 70:
            return f"Your score is {score}/100. Improving savings and reducing spending can push you to 70+."
        return f"Great job! Your score is {score}/100. Keep maintaining your financial habits!"

    elif "spend" in question or "expense" in question:
        return "Keep discretionary spending under 30% of income. Food delivery and subscriptions are easy areas to cut."

    return f"Your Financial Health Score is {score}/100. Ask me about savings, EMIs, or how to improve!"
