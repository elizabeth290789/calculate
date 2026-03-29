import math

import streamlit as st

from utils.calculations import calculate_sample_size_per_group


st.set_page_config(
    page_title="Калькулятор размера выборки",
    page_icon="📊",
)

st.title("Калькулятор размера выборки")
st.subheader(
    "Калькулятор расчёта выборки и длительности A/B-теста для двух равных групп 50/50"
)

with st.form("sample_size_form"):
    experiment_type = st.selectbox(
        "Тип эксперимента",
        (
            "Лендинг / регистрация",
            "Пресеты / посадка в продукт",
            "Покупки",
        ),
    )

    if experiment_type == "Лендинг / регистрация":
        baseline_input = st.number_input(
            "Базовая конверсия в регистрацию (%)",
            min_value=0.0,
            max_value=100.0,
            value=7.0,
            step=0.1,
            format="%g",
        )
        daily_base = st.number_input(
            "Среднее число пользователей в день",
            min_value=1,
            value=1000,
            step=100,
        )
        control_label = "Конверсия control"
        treatment_label = "Конверсия treatment"
        explanation = "Для лендинговых тестов расчет выборки строится по конверсии в регистрацию."
    elif experiment_type == "Пресеты / посадка в продукт":
        baseline_input = st.number_input(
            "Базовый retention ret3+ (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.1,
            format="%g",
        )
        daily_base = st.number_input(
            "Среднее число регистраций в день",
            min_value=1,
            value=100,
            step=10,
        )
        control_label = "Retention control"
        treatment_label = "Retention treatment"
        explanation = "Для тестов пресетов / посадки в продукт расчет выборки строится по retention ret3+."
    else:
        baseline_input = st.number_input(
            "Базовая конверсия в покупку (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.1,
            format="%g",
        )
        daily_base = st.number_input(
            "Среднее число регистраций в день",
            min_value=1,
            value=100,
            step=10,
        )
        control_label = "Конверсия control"
        treatment_label = "Конверсия treatment"
        explanation = (
            "Для тестов покупок расчет выборки строится по конверсии в покупку "
            "(покупатели / регистрации)."
        )

    p1 = baseline_input / 100
    mde_pp = st.number_input(
        "MDE (п.п.)",
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

    if experiment_type == "Покупки":
        if not 0 < p1 < 1:
            errors.append(
                "Базовая конверсия в покупку должна быть больше 0% и меньше 100%."
            )
    elif not 0 <= baseline_input <= 100:
        errors.append("Базовая метрика должна быть в диапазоне от 0 до 100%.")

    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть больше 0 и меньше 1.")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть больше 0 и меньше 1.")
    if mde_pp <= 0:
        errors.append("Параметр MDE должен быть больше 0.")
    if daily_base <= 0:
        errors.append("Среднее дневное число наблюдений должно быть больше 0.")
    if not 0 < traffic_share <= 1:
        errors.append("Доля трафика, идущая в эксперимент, должна быть больше 0 и не превышать 1.")

    p2 = p1 + mde_pp / 100
    if p2 >= 1:
        errors.append(
            "Метрика treatment (p2 = p1 + MDE) должна быть меньше 100%. Уменьшите p1 или MDE."
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
        daily_experiment_traffic = daily_base * traffic_share
        daily_per_group = daily_experiment_traffic / 2
        duration_days = math.ceil(sample_size_per_group / daily_per_group)

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        col1.metric(control_label, f"{p1:.2%}")
        col2.metric(treatment_label, f"{p2:.2%}")
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

        st.caption("Расчет выполнен для двух равных групп 50/50.")
        st.info(explanation)
