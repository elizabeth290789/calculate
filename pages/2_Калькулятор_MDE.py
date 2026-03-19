import math

import streamlit as st
from scipy.stats import norm


st.set_page_config(page_title="Калькулятор MDE", page_icon="📏")

st.title("Калькулятор MDE")
st.subheader(
    "Калькулятор помогает понять, какой минимальный эффект можно детектировать при текущем трафике и длительности теста."
)

with st.form("mde_calculator_form"):
    metric = st.selectbox(
        "Метрика",
        (
            "Конверсия в регистрацию",
            "Конверсия в retention (ret3+)",
        ),
    )
    sessions = st.number_input(
        "Сессии в месяц",
        min_value=1,
        value=30000,
        step=1000,
    )
    regs = st.number_input(
        "Регистрации в месяц",
        min_value=1,
        value=3000,
        step=100,
    )
    ret_l3 = st.number_input(
        "Retention ret3+ в месяц",
        min_value=0,
        value=300,
        step=10,
    )
    test_months = st.number_input(
        "Длительность теста (в месяцах)",
        min_value=1,
        value=1,
        step=1,
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

    submitted = st.form_submit_button("Рассчитать", use_container_width=True)

if submitted:
    errors = []

    if sessions <= 0:
        errors.append("Сессии в месяц должны быть больше 0.")
    if regs <= 0:
        errors.append("Регистрации в месяц должны быть больше 0.")
    if ret_l3 < 0:
        errors.append("Retention ret3+ в месяц не может быть отрицательным.")
    if regs > sessions:
        errors.append("Регистрации в месяц не могут превышать число сессий в месяц.")
    if ret_l3 > regs:
        errors.append("Retention ret3+ в месяц не может превышать число регистраций в месяц.")
    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть в диапазоне (0, 1).")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть в диапазоне (0, 1).")
    if test_months <= 0:
        errors.append("Длительность теста должна быть больше 0.")

    regs_conv = regs / sessions if sessions else 0
    ret_l3_regs_conv = ret_l3 / regs if regs else 0

    if metric == "Конверсия в регистрацию":
        p = regs_conv
        base_per_month = sessions
        metric_name = "Конверсия в регистрацию"
    else:
        p = ret_l3_regs_conv
        base_per_month = regs
        metric_name = "Конверсия в retention (ret3+)"

    n_total = base_per_month * test_months
    n_per_group = n_total / 2

    if p <= 0:
        errors.append("Текущая конверсия метрики должна быть больше 0.")
    if n_per_group <= 0:
        errors.append("Число наблюдений на группу должно быть больше 0.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        z_alpha = norm.ppf(1 - alpha / 2)
        z_power = norm.ppf(power)
        mde = (z_alpha + z_power) * math.sqrt(2 * p * (1 - p) / n_per_group)

        uplift_pct = (mde / p) * 100
        p_detectable = p + mde

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        col1.metric("Текущая конверсия метрики", f"{p:.2%}")
        col2.metric("База для теста в месяц", f"{base_per_month:,}".replace(",", " "))
        col3.metric("Наблюдений на группу", f"{n_per_group:,.0f}".replace(",", " "))
        col4.metric("MDE (в п.п.)", f"{mde * 100:.2f}")
        col5.metric("Relative uplift (%)", f"{uplift_pct:.2f}%")
        col6.metric(
            "Детектируемый рост метрики",
            f"{p:.2%} → {p_detectable:.2%}",
        )

        st.caption(
            f"Выбранная метрика: {metric_name}. Расчет выполнен для двух равных групп 50/50."
        )
        st.success(
            "При текущем трафике и длительности теста вы сможете надежно "
            f"детектировать эффекты не меньше чем {mde * 100:.2f} п.п."
        )
