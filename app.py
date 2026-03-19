import math

import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm


st.set_page_config(
    page_title="Калькулятор размера выборки для A/B-теста регистрации",
    page_icon="📊",
)


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


st.title("Калькулятор размера выборки для A/B-теста регистрации")
st.subheader(
    "Калькулятор расчёта выборки для а/б теста с конверсией в регистрацию при равных группах 50/50"
)

with st.form("sample_size_form"):
    p1_input = st.number_input(
        "Базовая конверсия в регистрацию (%)",
        min_value=0.0,
        max_value=100.0,
        value=7.0,
        step=0.1,
        format="%g",
    )
    p1 = p1_input / 100
    mde_pp = st.number_input(
        "MDE в процентных пунктах, mde_pp",
        min_value=0.0001,
        value=0.5,
        step=0.1,
        format="%g",
    )
    alpha = st.number_input(
        "alpha",
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
        step=0.01,
        format="%g",
    )
    users_per_day = st.number_input(
        "Среднее число пользователей в день",
        min_value=1,
        value=1000,
        step=100,
    )
    traffic_share = st.number_input(
        "Доля трафика, идущая в эксперимент",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05,
        format="%g",
    )

    submitted = st.form_submit_button("Рассчитать", use_container_width=True)

if submitted:
    errors = []

    if not 0 <= p1_input <= 100:
        errors.append("Базовая конверсия должна быть в диапазоне от 0 до 100%.")
    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть больше 0 и меньше 1.")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть больше 0 и меньше 1.")
    if mde_pp <= 0:
        errors.append("Параметр mde_pp должен быть больше 0.")
    if users_per_day <= 0:
        errors.append("Среднее число пользователей в день должно быть больше 0.")
    if not 0 < traffic_share <= 1:
        errors.append("Доля трафика, идущая в эксперимент, должна быть больше 0 и не превышать 1.")

    p2 = p1 + mde_pp / 100
    if p2 > 1:
        errors.append(
            "Конверсия treatment (p2 = p1 + MDE) не должна превышать 1. Уменьшите p1 или MDE."
        )

    if errors:
        for error in errors:
            st.error(error)
    else:
        sample_size_per_group, p2 = calculate_sample_size_per_group(
            p1=p1,
            mde_pp=mde_pp,
            alpha=alpha,
            power=power,
        )
        total_sample_size = sample_size_per_group * 2
        uplift_pct = ((p2 - p1) / p1) * 100 if p1 > 0 else float("inf")
        daily_experiment_traffic = users_per_day * traffic_share
        daily_per_group = daily_experiment_traffic / 2
        duration_days = math.ceil(sample_size_per_group / daily_per_group)

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        col1.metric("Конверсия control", f"{p1:.2%}")
        col2.metric("Конверсия treatment", f"{p2:.2%}")
        col3.metric(
            "Relative uplift (%)",
            "∞" if math.isinf(uplift_pct) else f"{uplift_pct:.2f}%",
        )
        col4.metric(
            "Размер выборки на группу",
            f"{sample_size_per_group:,}".replace(",", " "),
        )
        col5.metric(
            "Общий размер выборки",
            f"{total_sample_size:,}".replace(",", " "),
        )
        col6.metric("Оценочная длительность теста (дни)", f"{duration_days}")

        st.caption(
            "Расчет выполнен для двух равных групп 50/50 и бинарной метрики регистрации."
        )

        mde_chart_data = pd.DataFrame(
            [
                {
                    "MDE (п.п.)": current_mde_pp,
                    "Размер выборки на группу": calculate_sample_size_per_group(
                        p1=p1,
                        mde_pp=current_mde_pp,
                        alpha=alpha,
                        power=power,
                    )[0],
                }
                for current_mde_pp in MDE_RANGE_PP
                if p1 + current_mde_pp / 100 <= 1
            ]
        )
        st.subheader("Как меняется размер выборки при разных MDE")

        mde_chart_data = mde_chart_data.sort_values("MDE (п.п.)")
        st.dataframe(
            mde_chart_data[["MDE (п.п.)", "Размер выборки на группу"]],
            use_container_width=True,
            hide_index=True,
        )
