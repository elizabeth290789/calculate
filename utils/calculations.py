import math

import numpy as np
from scipy.stats import norm


MDE_RANGE_PP = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]


def calculate_sample_size_per_group(
    p1: float,
    mde_pp: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> tuple[int, float]:
    p2 = p1 + mde_pp / 100
    p_bar = (p1 + p2) / 2

    z_alpha = norm.ppf(1 - alpha / 2)
    z_power = norm.ppf(power)

    numerator = (
        z_alpha * np.sqrt(2 * p_bar * (1 - p_bar))
        + z_power * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    ) ** 2
    denominator = (p2 - p1) ** 2

    n = numerator / denominator
    return math.ceil(n), p2
