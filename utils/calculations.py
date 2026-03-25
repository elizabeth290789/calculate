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


def calculate_mde_for_proportion(
    baseline_rate: float,
    n_per_group: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> tuple[float, float, float]:
    z_alpha = norm.ppf(1 - alpha / 2)
    z_power = norm.ppf(power)

    mde = (z_alpha + z_power) * math.sqrt(
        2 * baseline_rate * (1 - baseline_rate) / n_per_group
    )
    detectable_rate = baseline_rate + mde
    uplift_pct = (mde / baseline_rate) * 100

    return mde, detectable_rate, uplift_pct


def calculate_two_proportion_z_test(
    n_a: int,
    success_a: int,
    n_b: int,
    success_b: int,
    alpha: float,
) -> dict[str, float]:
    p_a = success_a / n_a
    p_b = success_b / n_b
    diff = p_b - p_a

    p_pool = (success_a + success_b) / (n_a + n_b)
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    if se_pool == 0:
        raise ValueError(
            "Стандартная ошибка по pooled-оценке равна 0. Z-статистику невозможно вычислить."
        )

    z_stat = diff / se_pool
    p_value = 2 * (1 - norm.cdf(abs(z_stat)))

    z_crit = norm.ppf(1 - alpha / 2)
    se_unpooled = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    ci_low = diff - z_crit * se_unpooled
    ci_high = diff + z_crit * se_unpooled

    return {
        "p_a": p_a,
        "p_b": p_b,
        "diff": diff,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_low": ci_low,
        "ci_high": ci_high,
    }
