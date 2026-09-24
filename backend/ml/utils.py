# backend/ml/utils.py
import math

def clamp(n, a, b):
    return max(a, min(b, n))

def seeded_random(seed: int) -> float:
    x = math.sin(seed) * 10000
    return x - math.floor(x)

def location_score(lat: float, lng: float) -> float:
    seed = int(lat * 1000 + lng * 1000)
    a = seeded_random(seed + 11)
    b = seeded_random(seed + 77)
    c = seeded_random(seed + 123)
    return clamp(a * 0.55 + b * 0.30 + c * 0.15, 0, 1)
