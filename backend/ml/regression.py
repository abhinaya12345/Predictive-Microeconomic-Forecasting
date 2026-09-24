# backend/ml/regression.py
from .utils import location_score, clamp

def predict_profit_loss(lat: float, lng: float, mode: str = "yearly"):
    """
    Returns: revenue, expenses, profit, breakeven_months
    Mode: 'monthly' or 'yearly'
    """
    score = location_score(lat, lng)
    scale = 12 if mode == "yearly" else 1

    # basic simulated economics
    base_revenue_m = 35000 + score * 85000
    base_expenses_m = 21000 + score * 52000

    revenue = base_revenue_m * scale
    expenses = base_expenses_m * scale
    profit = max(0, revenue - expenses)

    fixed_cost = 240000 if mode == "yearly" else 60000
    monthly_profit = max(1000, profit / scale)
    breakeven_months = clamp(round(fixed_cost / monthly_profit), 2, 18)

    return {
        "score": score,
        "mode": mode,
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "breakeven_months": breakeven_months
    }
