import pandas as pd
import numpy as np

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    
    data = {
        "customer_id": range(1, n_samples + 1),
        "monthly_income": np.random.randint(20000, 200000, n_samples),
        "monthly_expenses": np.random.randint(10000, 150000, n_samples),
        "monthly_savings": np.random.randint(0, 50000, n_samples),
        "emi_amount": np.random.randint(0, 80000, n_samples),
        "upi_transactions": np.random.randint(5, 150, n_samples),
        "missed_payments": np.random.randint(0, 6, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate health score
    df["savings_ratio"] = df["monthly_savings"] / df["monthly_income"]
    df["emi_ratio"] = df["emi_amount"] / df["monthly_income"]
    df["expense_ratio"] = df["monthly_expenses"] / df["monthly_income"]
    
    df["health_score"] = (
        (df["savings_ratio"] * 25) +
        ((1 - df["emi_ratio"]) * 20) +
        ((1 - df["expense_ratio"]) * 20) +
        (df["monthly_income"] / 200000 * 20) +
        (df["upi_transactions"] / 150 * 10) +
        (df["missed_payments"].apply(lambda x: max(0, 5 - x*2)))
    ).clip(0, 100).astype(int)
    
    # Category
    df["category"] = pd.cut(
        df["health_score"],
        bins=[0, 40, 70, 100],
        labels=["Poor", "Average", "Good"]
    )
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(1000)
    df.to_csv("synthetic_financial_data.csv", index=False)
    print(f"✅ Generated {len(df)} records")
    print(df[["customer_id","monthly_income","health_score","category"]].head(10))
