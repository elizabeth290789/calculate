import streamlit as st

from utils.calculations import calculate_two_proportion_z_test


st.set_page_config(page_title="Статкритерий для конверсий", page_icon="🧪")

st.title("Статкритерий для конверсий")
st.subheader(
    "Сравнение двух конверсий с помощью двустороннего z-теста для двух пропорций."
)

with st.form("conversion_z_test_form"):
    st.markdown("### Control")
    n_a = st.number_input(
        "Пользователей в control",
        min_value=1,
        value=15000,
        step=100,
    )
    success_a = st.number_input(
        "Конверсий в control",
        min_value=0,
        value=1500,
        step=10,
    )

    st.markdown("### Test")
    n_b = st.number_input(
        "Пользователей в test",
        min_value=1,
        value=15000,
        step=100,
    )
    success_b = st.number_input(
        "Конверсий в test",
        min_value=0,
        value=1650,
        step=10,
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

if submitted:
    errors = []

    if n_a <= 0:
        errors.append("Число пользователей в control должно быть больше 0.")
    if n_b <= 0:
        errors.append("Число пользователей в test должно быть больше 0.")
    if success_a < 0:
        errors.append("Число конверсий в control не может быть отрицательным.")
    if success_b < 0:
        errors.append("Число конверсий в test не может быть отрицательным.")
    if success_a > n_a:
        errors.append("Число конверсий в control не может превышать число пользователей в control.")
    if success_b > n_b:
        errors.append("Число конверсий в test не может превышать число пользователей в test.")
    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть в диапазоне (0, 1).")

    if errors:
        for error in errors:
            st.error(error)
    else:
        try:
            results = calculate_two_proportion_z_test(
                n_a=n_a,
                success_a=success_a,
                n_b=n_b,
                success_b=success_b,
                alpha=alpha,
            )
        except ValueError as exc:
            st.error(str(exc))
        else:
            p_a = results["p_a"]
            p_b = results["p_b"]
            diff = results["diff"]
            z_stat = results["z_stat"]
            p_value = results["p_value"]
            ci_low = results["ci_low"]
            ci_high = results["ci_high"]

            uplift_text = "—"
            if p_a == 0:
                st.info(
                    "Relative uplift не рассчитан, так как конверсия control равна 0."
                )
            else:
                uplift_pct = (diff / p_a) * 100
                uplift_text = f"{uplift_pct:.2f}%"

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            col5, col6 = st.columns(2)
            col7, _ = st.columns(2)

            col1.metric(
                "Конверсия control",
                f"{p_a:.2%}",
                help=f"{success_a:,} / {n_a:,}".replace(",", " "),
            )
            col2.metric(
                "Конверсия test",
                f"{p_b:.2%}",
                help=f"{success_b:,} / {n_b:,}".replace(",", " "),
            )
            col3.metric("Разница (B - A), п.п.", f"{diff * 100:.2f}")
            col4.metric("Relative uplift (%)", uplift_text)
            col5.metric("z-statistic", f"{z_stat:.4f}")
            col6.metric("p-value", f"{p_value:.6f}")
            col7.metric(
                "95% CI для разницы (B - A), п.п.",
                f"[{ci_low * 100:.2f}; {ci_high * 100:.2f}]",
            )

            is_significant = (p_value < alpha) and not (ci_low <= 0 <= ci_high)

            if is_significant and diff > 0:
                st.success(
                    "Разница статистически значима: test показывает более высокую конверсию, чем control."
                )
            elif is_significant and diff < 0:
                st.warning(
                    "Разница статистически значима: test показывает более низкую конверсию, чем control."
                )
            else:
                st.info(
                    "Статистически значимого различия между группами не обнаружено."
                )

            st.caption(
                "Используется двусторонний z-тест для сравнения двух пропорций. "
                "Доверительный интервал рассчитан для разницы конверсий (test - control)."
            )
