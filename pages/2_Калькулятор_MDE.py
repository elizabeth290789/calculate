import streamlit as st

from utils.calculations import calculate_mde


st.set_page_config(page_title="Калькулятор MDE", page_icon="📏")

METRIC_OPTIONS = {
    "Конверсия в регистрацию": {
        "metric_name": "Конверсия в регистрацию",
        "denominator_name": "sessions",
    },
    "Конверсия в retention (ret3+)": {
        "metric_name": "Конверсия в retention (ret3+)",
        "denominator_name": "regs",
    },
}


st.title("Калькулятор MDE")
st.subheader(
    "Калькулятор помогает понять, какой минимальный эффект можно детектировать при текущем трафике и длительности теста."
)

with st.form("mde_form"):
    metric = st.selectbox("Метрика", options=list(METRIC_OPTIONS.keys()))
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
        errors.append("Параметр sessions должен быть больше 0.")
    if regs <= 0:
        errors.append("Параметр regs должен быть больше 0.")
    if ret_l3 < 0:
        errors.append("Параметр retL3 не может быть отрицательным.")
    if regs > sessions:
        errors.append("Количество регистраций не может превышать количество сессий.")
    if ret_l3 > regs:
        errors.append("Retention ret3+ не может превышать количество регистраций.")
    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть больше 0 и меньше 1.")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть больше 0 и меньше 1.")
    if test_months <= 0:
        errors.append("Длительность теста должна быть больше 0.")

    regs_conv = regs / sessions
    ret_l3_regs_conv = ret_l3 / regs

    if metric == "Конверсия в регистрацию":
        p = regs_conv
        base_per_month = sessions
    else:
        p = ret_l3_regs_conv
        base_per_month = regs

    metric_config = METRIC_OPTIONS[metric]
    metric_name = metric_config["metric_name"]
    denominator_name = metric_config["denominator_name"]

    n_total = base_per_month * test_months
    n_per_group = n_total / 2

    if p <= 0:
        errors.append("Текущая конверсия выбранной метрики должна быть больше 0.")
    if n_per_group <= 0:
        errors.append("Количество наблюдений на группу должно быть больше 0.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        results = calculate_mde(
            p=p,
            base_per_month=base_per_month,
            test_months=test_months,
            alpha=alpha,
            power=power,
        )

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        col1.metric(f"Текущая конверсия: {metric_name}", f"{p:.2%}")
        col2.metric(
            f"База для теста в месяц ({denominator_name})",
            f"{base_per_month:,}".replace(",", " "),
        )
        col3.metric(
            "Наблюдений на группу",
            f"{results['n_per_group']:,.0f}".replace(",", " "),
        )
        col4.metric("MDE (в п.п.)", f"{results['mde'] * 100:.2f}")
        col5.metric("Relative uplift (%)", f"{results['uplift_pct']:.2f}%")
        col6.metric(
            "Детектируемый рост метрики",
            f"{p:.2%} → {results['p_detectable']:.2%}",
        )

        st.caption(
            f"При текущем трафике и длительности теста вы сможете надежно детектировать эффекты не меньше чем {results['mde'] * 100:.2f} п.п."
        )
