import streamlit as st

from utils.calculations import calculate_mde_for_proportion


st.set_page_config(page_title="Калькулятор MDE", page_icon="📏")

st.title("Калькулятор MDE")
st.subheader(
    "Калькулятор помогает понять, какой минимальный эффект можно детектировать при текущей базе и длительности теста."
)

with st.form("mde_calculator_form"):
    experiment_type = st.selectbox(
        "Тип эксперимента",
        (
            "Лендинг / регистрация",
            "Пресеты / посадка в продукт",
            "Покупки",
        ),
    )

    if experiment_type == "Лендинг / регистрация":
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
        ret_l3 = None
        buyers = None
    elif experiment_type == "Пресеты / посадка в продукт":
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
        sessions = None
        buyers = None
    else:
        regs = st.number_input(
            "Регистрации в месяц",
            min_value=1,
            value=3000,
            step=100,
        )
        buyers = st.number_input(
            "Покупатели в месяц",
            min_value=0,
            value=300,
            step=10,
        )
        sessions = None
        ret_l3 = None

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

    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть в диапазоне (0, 1).")
    if not 0 < power < 1:
        errors.append("Параметр power должен быть в диапазоне (0, 1).")
    if test_months <= 0:
        errors.append("Длительность теста должна быть больше 0.")

    if experiment_type == "Лендинг / регистрация":
        if sessions <= 0:
            errors.append("Сессии в месяц должны быть больше 0.")
        if regs <= 0:
            errors.append("Регистрации в месяц должны быть больше 0.")
        if regs > sessions:
            errors.append("Регистрации в месяц не могут превышать число сессий в месяц.")

        baseline_rate = regs / sessions if sessions else 0
        base_per_month = sessions
        baseline_label = "Текущая конверсия в регистрацию"
        base_label = "База для теста в месяц"
        explanation = (
            "Для лендинговых тестов основной метрикой планирования является конверсия "
            "в регистрацию. Retention можно анализировать дополнительно как downstream-метрику."
        )
    elif experiment_type == "Пресеты / посадка в продукт":
        if regs <= 0:
            errors.append("Регистрации в месяц должны быть больше 0.")
        if ret_l3 < 0:
            errors.append("Retention ret3+ в месяц не может быть отрицательным.")
        if ret_l3 > regs:
            errors.append("Retention ret3+ в месяц не может превышать число регистраций в месяц.")

        baseline_rate = ret_l3 / regs if regs else 0
        base_per_month = regs
        baseline_label = "Текущий retention (ret3+)"
        base_label = "База для теста в месяц"
        explanation = (
            "Для тестов пресетов / посадки в продукт основной метрикой планирования "
            "является retention ret3+, так как изменения влияют на продуктовую посадку пользователя."
        )
    else:
        if regs <= 0:
            errors.append("Регистрации в месяц должны быть больше 0.")
        if buyers < 0:
            errors.append("Покупатели в месяц не могут быть отрицательными.")
        if buyers > regs:
            errors.append("Покупатели в месяц не могут превышать число регистраций в месяц.")

        baseline_rate = buyers / regs if regs else 0
        base_per_month = regs
        baseline_label = "Текущая конверсия в покупку"
        base_label = "База для теста в месяц (registrations)"
        explanation = (
            "Для тестов покупок расчет MDE строится по конверсии в покупку "
            "(покупатели / регистрации)."
        )

    n_total = base_per_month * test_months
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

        col1.metric(baseline_label, f"{baseline_rate:.2%}")
        col2.metric(base_label, f"{base_per_month:,}".replace(",", " "))
        col3.metric("Наблюдений на группу", f"{n_per_group:,.0f}".replace(",", " "))
        col4.metric("MDE (в п.п.)", f"{mde * 100:.2f}")
        col5.metric("Relative uplift (%)", f"{uplift_pct:.2f}%")
        col6.metric(
            "Детектируемый рост метрики",
            f"{baseline_rate:.2%} → {detectable_rate:.2%}",
        )

        st.caption("Расчет выполнен для двух равных групп 50/50.")
        st.info(explanation)
