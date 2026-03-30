import numpy as np
import streamlit as st
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

from utils.ui import apply_base_styles


st.set_page_config(
    page_title="Размер выборки для A/B/C теста (Bonferroni)",
    page_icon="📊",
)

apply_base_styles()


def sample_size_three_variants_bonferroni(
    baseline_conversion_pct: float,
    mde_value_pct: float,
    mde_type: str,
    alpha_global: float,
    power: float,
    n_comparisons: int = 2,
) -> tuple[float, float, float, float, float, int, int, int]:
    p1 = baseline_conversion_pct / 100

    if mde_type == "процентные пункты":
        p2 = p1 + (mde_value_pct / 100)
    else:
        uplift = mde_value_pct / 100
        p2 = p1 * (1 + uplift)

    alpha_local = alpha_global / n_comparisons
    effect_size = proportion_effectsize(p1, p2)

    analysis = NormalIndPower()
    n = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha_local,
        power=power,
        ratio=1,
        alternative="two-sided",
    )

    n_group = int(np.ceil(n))
    n_per_comparison = n_group * 2
    n_total_three_groups = n_group * 3

    return (
        p1,
        p2,
        alpha_global,
        alpha_local,
        power,
        n_group,
        n_total_three_groups,
        n_per_comparison,
    )


st.title("Калькулятор размера выборки для A/B/C теста")
st.subheader(
    "Расчёт размера выборки для бинарной метрики при трёх вариантах (A/B/C) "
    "с поправкой Бонферрони для двух сравнений: A-B и A-C."
)
st.caption(
    "Глобальный уровень значимости делится на число сравнений (Bonferroni correction)."
)

baseline_conversion = st.number_input(
    "Базовая конверсия (%)",
    min_value=0.0,
    max_value=100.0,
    value=7.0,
    step=0.1,
    format="%g",
)

mde_type = st.radio(
    "Тип MDE",
    options=("процентные пункты", "относительный uplift"),
    index=0,
)

mde_label = "MDE (п.п.)" if mde_type == "процентные пункты" else "MDE uplift (%)"
mde_value = st.number_input(
    mde_label,
    min_value=0.0001,
    value=0.5,
    step=0.1,
    format="%g",
)

alpha_global = st.number_input(
    "alpha_global",
    min_value=0.0001,
    max_value=0.9999,
    value=0.05,
    step=0.01,
    format="%g",
)

power = st.number_input(
    "power",
    min_value=0.0001,
    max_value=0.9999,
    value=0.8,
    step=0.05,
    format="%g",
)

n_comparisons = st.number_input(
    "Количество сравнений",
    min_value=1,
    value=2,
    step=1,
)

submitted = st.button("Рассчитать", use_container_width=True)

if submitted:
    errors = []

    if not 0 <= baseline_conversion <= 100:
        errors.append("Базовая конверсия должна быть в диапазоне от 0 до 100%.")
    if baseline_conversion <= 0:
        errors.append("Базовая конверсия должна быть больше 0%.")

    if not 0 < alpha_global < 1:
        errors.append("Параметр alpha_global должен быть больше 0 и меньше 1.")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть больше 0 и меньше 1.")
    if n_comparisons < 1:
        errors.append("Количество сравнений должно быть не меньше 1.")

    p1 = baseline_conversion / 100
    if mde_type == "процентные пункты":
        p2 = p1 + mde_value / 100
    else:
        p2 = p1 * (1 + mde_value / 100)

    if p2 >= 1:
        errors.append(
            "Target conversion (p2) должна быть меньше 100%. Уменьшите baseline или MDE."
        )

    if errors:
        for error in errors:
            st.error(error)
    else:
        (
            p1,
            p2,
            alpha_global,
            alpha_local,
            power,
            n_group,
            n_total_three_groups,
            n_per_comparison,
        ) = sample_size_three_variants_bonferroni(
            baseline_conversion_pct=baseline_conversion,
            mde_value_pct=mde_value,
            mde_type=mde_type,
            alpha_global=alpha_global,
            power=power,
            n_comparisons=int(n_comparisons),
        )

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        col1.metric("Baseline conversion", f"{p1:.2%}")
        col2.metric("Target conversion", f"{p2:.2%}")
        col3.metric("Corrected alpha", f"{alpha_local:.4f}")
        col4.metric("Sample size per group", f"{n_group:,}".replace(",", " "))
        col5.metric(
            "Sample size per comparison (2 группы)",
            f"{n_per_comparison:,}".replace(",", " "),
        )
        col6.metric(
            "Total sample size for 3 groups",
            f"{n_total_three_groups:,}".replace(",", " "),
        )

        st.write("Расчёт предполагает равные размеры групп и бинарную метрику (конверсию).")
        st.write("Используется поправка Бонферрони для двух сравнений: A-B и A-C.")
