import streamlit as st

from utils.ui import apply_base_styles

from utils.calculations import calculate_mde_for_proportion


st.set_page_config(page_title="Калькулятор MDE", page_icon="📏")

apply_base_styles()

st.title("Калькулятор MDE")
st.subheader(
    "Калькулятор помогает понять, какой минимальный эффект можно детектировать при текущей базе и длительности теста."
)

EXPERIMENT_CONFIG = {
    "Лендинг / регистрация": {
        "base_label": "Сессии в месяц",
        "base_default": 30000,
        "base_step": 1000,
        "success_label": "Регистрации в месяц",
        "success_default": 3000,
        "success_step": 100,
        "baseline_label": "Текущая конверсия в регистрацию",
        "base_metric_label": "База для теста в месяц",
        "explanation": (
            "Для лендинговых тестов основной метрикой планирования является конверсия "
            "в регистрацию."
        ),
        "success_error_negative": "Регистрации в месяц должны быть больше 0.",
        "success_error_over": "Регистрации в месяц не могут превышать число сессий в месяц.",
    },
    "Пресеты / посадка в продукт": {
        "base_label": "Регистрации в месяц",
        "base_default": 3000,
        "base_step": 100,
        "success_label": "Retention ret3+ в месяц",
        "success_default": 300,
        "success_step": 10,
        "baseline_label": "Текущий retention (ret3+)",
        "base_metric_label": "База для теста в месяц",
        "explanation": (
            "Для тестов пресетов / посадки в продукт основной метрикой планирования "
            "является retention ret3+."
        ),
        "success_error_negative": "Retention ret3+ в месяц не может быть отрицательным.",
        "success_error_over": "Retention ret3+ в месяц не может превышать число регистраций в месяц.",
    },
    "Покупки": {
        "base_label": "Регистрации в месяц",
        "base_default": 3000,
        "base_step": 100,
        "success_label": "Покупатели в месяц",
        "success_default": 300,
        "success_step": 10,
        "baseline_label": "Текущая конверсия в покупку",
        "base_metric_label": "База для теста в месяц",
        "explanation": (
            "Для тестов покупок расчет MDE строится по конверсии в покупку "
            "(покупатели / регистрации)."
        ),
        "success_error_negative": "Покупатели в месяц не могут быть отрицательными.",
        "success_error_over": "Покупатели в месяц не могут превышать число регистраций в месяц.",
    },
}

experiment_type = st.selectbox("Тип эксперимента", tuple(EXPERIMENT_CONFIG.keys()))

if experiment_type == "Лендинг / регистрация":
    config = EXPERIMENT_CONFIG["Лендинг / регистрация"]
elif experiment_type == "Пресеты / посадка в продукт":
    config = EXPERIMENT_CONFIG["Пресеты / посадка в продукт"]
else:
    config = EXPERIMENT_CONFIG["Покупки"]

base_count = st.number_input(
    config["base_label"],
    min_value=1,
    value=config["base_default"],
    step=config["base_step"],
)
success_count = st.number_input(
    config["success_label"],
    min_value=0,
    value=config["success_default"],
    step=config["success_step"],
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

submitted = st.button("Рассчитать", use_container_width=True)

if submitted:
    errors = []

    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть в диапазоне (0, 1).")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть в диапазоне (0, 1).")
    if test_months <= 0:
        errors.append("Длительность теста должна быть больше 0.")

    if base_count <= 0:
        errors.append(f"{config['base_label']} должны быть больше 0.")

    if experiment_type == "Лендинг / регистрация":
        if success_count <= 0:
            errors.append(config["success_error_negative"])
    else:
        if success_count < 0:
            errors.append(config["success_error_negative"])

    if success_count > base_count:
        errors.append(config["success_error_over"])

    baseline_rate = success_count / base_count if base_count else 0
    n_total = base_count * test_months
    n_per_group = n_total / 2

    if baseline_rate <= 0:
        errors.append("Базовая метрика должна быть больше 0.")
    if n_per_group <= 0:
        errors.append("Число наблюдений на группу должно быть больше 0.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        mde, detectable_rate, uplift_pct = calculate_mde_for_proportion(
            baseline_rate=baseline_rate,
            n_per_group=n_per_group,
            alpha=alpha,
            power=power,
        )

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        col1.metric(config["baseline_label"], f"{baseline_rate:.2%}")
        col2.metric(config["base_metric_label"], f"{base_count:,}".replace(",", " "))
        col3.metric("Наблюдений на группу", f"{n_per_group:,.0f}".replace(",", " "))
        col4.metric("MDE (в п.п.)", f"{mde * 100:.2f}")
        col5.metric("Relative uplift (%)", f"{uplift_pct:.2f}%")
        col6.metric(
            "Детектируемый рост метрики",
            f"{baseline_rate:.2%} → {detectable_rate:.2%}",
        )

        st.caption("Расчет выполнен для двух равных групп 50/50.")
        st.info(config["explanation"])
