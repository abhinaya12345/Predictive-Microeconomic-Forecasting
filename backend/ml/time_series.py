# backend/ml/time_series.py
import math
from .utils import seeded_random

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def predict_inflation_series(lat: float, lng: float, score: float):
    """
    Returns 12-month inflation series (values in %).
    """
    seed = int(lat * 1000 + lng * 1000)
    base_infl = 2.2 + score * 2.4 + seeded_random(seed + 9) * 0.6

    values = []
    for i in range(12):
        drift = (i / 11) * (0.9 + score * 1.1)
        wobble = math.sin((i + 1) * 0.9) * (0.18 + score * 0.12)
        values.append(base_infl + drift + wobble)

    return {"months": MONTHS, "values": values}
