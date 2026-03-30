import numpy as np
import streamlit as st

from utils.ui import apply_base_styles

from utils.calculations import welch_ttest_from_stats


st.set_page_config(page_title="Статкритерий для ARPU", page_icon="💰")

apply_base_styles()

st.title("Статкритерий для ARPU")
st.subheader(
    "Сравнение ARPU в control и test с помощью Welch t-test по агрегированным данным."
)

with st.form("arpu_welch_ttest_form"):
    st.markdown("### Control")
    n_a = st.number_input(
        "Регистрации в control",
        min_value=2,
        value=15000,
        step=100,
    )
    mean_a = st.number_input(
        "ARPU в control",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%g",
    )
    std_a = st.number_input(
        "Std ARPU в control",
        min_value=0.0,
        value=300.0,
        step=1.0,
        format="%g",
    )

    st.markdown("### Test")
    n_b = st.number_input(
        "Регистрации в test",
        min_value=2,
        value=15000,
        step=100,
    )
    mean_b = st.number_input(
        "ARPU в test",
        min_value=0.0,
        value=110.0,
        step=1.0,
        format="%g",
    )
    std_b = st.number_input(
        "Std ARPU в test",
        min_value=0.0,
        value=310.0,
        step=1.0,
        format="%g",
    )

    st.markdown("### Параметры")
    alpha = st.number_input(
        "alpha",
        min_value=0.0001,
        max_value=0.9999,
        value=0.05,
        step=0.01,
        format="%g",
    )

    submitted = st.form_submit_button("Рассчитать", use_container_width=True)

st.caption(
    "Используйте ARPU, рассчитанный как revenue / registrations. Стандартное отклонение "
    "тоже должно быть рассчитано на уровне регистраций, то есть с нулевой выручкой "
    "для тех регистраций, которые не купили."
)

if submitted:
    errors = []

    if n_a <= 1:
        errors.append("Регистрации в control должны быть больше 1.")
    if n_b <= 1:
        errors.append("Регистрации в test должны быть больше 1.")
    if mean_a < 0:
        errors.append("ARPU в control не может быть отрицательным.")
    if mean_b < 0:
        errors.append("ARPU в test не может быть отрицательным.")
    if std_a < 0:
        errors.append("Std ARPU в control не может быть отрицательным.")
    if std_b < 0:
        errors.append("Std ARPU в test не может быть отрицательным.")
    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть в диапазоне (0, 1).")

    if errors:
        for error in errors:
            st.error(error)
    else:
        try:
            results = welch_ttest_from_stats(
                mean_a=mean_a,
                std_a=std_a,
                n_a=n_a,
                mean_b=mean_b,
                std_b=std_b,
                n_b=n_b,
                alpha=alpha,
            )
        except ValueError as exc:
            st.error(str(exc))
        else:
            diff = results["diff"]
            uplift_pct = results["uplift_pct"]
            t_stat = results["t_stat"]
            p_value = results["p_value"]
            ci_low = results["ci_low"]
            ci_high = results["ci_high"]

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            col5, col6 = st.columns(2)
            col7, _ = st.columns(2)

            col1.metric("ARPU control", f"{mean_a:,.2f}".replace(",", " "))
            col2.metric("ARPU test", f"{mean_b:,.2f}".replace(",", " "))
            col3.metric("Разница (test - control)", f"{diff:,.2f}".replace(",", " "))

            if np.isnan(uplift_pct):
                col4.metric("Relative uplift (%)", "—")
                st.info(
                    "Relative uplift не рассчитан, так как ARPU в control равен 0."
                )
            else:
                col4.metric("Relative uplift (%)", f"{uplift_pct:.2f}%")

            col5.metric("t-statistic", f"{t_stat:.4f}")
            col6.metric("p-value", f"{p_value:.6f}")
            col7.metric(
                "Доверительный интервал для разницы ARPU",
                f"[{ci_low:.4f}, {ci_high:.4f}]",
            )

            is_significant = (p_value < alpha) and not (ci_low <= 0 <= ci_high)

            if is_significant and diff > 0:
                st.success(
                    "Разница статистически значима: ARPU в test выше, чем в control."
                )
            elif is_significant and diff < 0:
                st.warning(
                    "Разница статистически значима: ARPU в test ниже, чем в control."
                )
            else:
                st.info(
                    "Статистически значимого различия по ARPU между группами не обнаружено."
                )

            st.caption(
                "Используется Welch t-test по агрегированным статистикам "
                "(размер группы, среднее и стандартное отклонение)."
            )
