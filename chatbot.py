import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_ai_response(user_question, score, breakdown):
    
    score_context = f"""
    You are FinNova, an AI financial health advisor for IDBI Bank.
    
    The user's Financial Health Score is {score}/100.
    Score breakdown:
    - Income stability: {breakdown.get('Income stability', 0)}/100
    - Savings ratio: {breakdown.get('Savings ratio', 0)}/100
    - Spending habit: {breakdown.get('Spending habit', 0)}/100
    - Debt load: {breakdown.get('Debt load', 0)}/100
    - UPI behaviour: {breakdown.get('UPI behaviour', 0)}/100
    - Payment history: {breakdown.get('Payment history', 0)}/100
    
    Based on this data, answer the user's question in a friendly, 
    simple, and helpful way. Give specific actionable advice.
    Keep your response under 100 words.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": score_context},
                {"role": "user", "content": user_question}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return fallback_response(user_question, score, breakdown)


def fallback_response(question, score, breakdown):
    question = question.lower()
    
    if "savings" in question or "save" in question:
        savings_score = breakdown.get('Savings ratio', 0)
        if savings_score < 50:
            return "Your savings ratio is below target. Try saving at least 20% of your income every month."
        else:
            return "Your savings habit is good! Consider investing in IDBI Tax-Saver FD or SIP."
    
    elif "emi" in question or "debt" in question or "loan" in question:
        debt_score = breakdown.get('Debt load', 0)
        if debt_score < 50:
            return "Your EMI burden is high. Try to prepay smaller loans first to reduce monthly obligations."
        else:
            return "Your debt load is manageable. Keep maintaining timely payments."
    
    elif "score" in
