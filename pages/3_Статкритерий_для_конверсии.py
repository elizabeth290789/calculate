import streamlit as st

from utils.calculations import calculate_two_proportion_z_test
from utils.ui import configure_page, render_tool_header


configure_page(title="Статкритерий для конверсий", icon="🧪")
render_tool_header(
    "Статкритерий для конверсий",
    "Сравнение двух групп с помощью двустороннего z-теста для двух пропорций.",
)

METRIC_CONFIG = {
    "Конверсия в регистрацию": {
        "title": "конверсии в регистрацию",
        "n_a_label": "Сессий в control",
        "success_a_label": "Регистраций в control",
        "n_b_label": "Сессий в test",
        "success_b_label": "Регистраций в test",
    },
    "Retention (ret3+)": {
        "title": "retention (ret3+)",
        "n_a_label": "Регистраций в control",
        "success_a_label": "Retention ret3+ в control",
        "n_b_label": "Регистраций в test",
        "success_b_label": "Retention ret3+ в test",
    },
    "Конверсия в покупку": {
        "title": "конверсии в покупку",
        "n_a_label": "Регистраций в control",
        "success_a_label": "Покупателей в control",
        "n_b_label": "Регистраций в test",
        "success_b_label": "Покупателей в test",
    },
}

left, right = st.columns([1.1, 1], gap="large")

with left:
    conversion_type = st.selectbox("Тип конверсии", options=list(METRIC_CONFIG.keys()))
    selected_metric = METRIC_CONFIG[conversion_type]

    with st.form("conversion_z_test_form"):
        st.markdown("#### Control")
        n_a = st.number_input(
            selected_metric["n_a_label"],
            min_value=1,
            value=15000,
            step=100,
        )
        success_a = st.number_input(
            selected_metric["success_a_label"],
            min_value=0,
            value=1500,
            step=10,
        )

        st.markdown("#### Test")
        n_b = st.number_input(
            selected_metric["n_b_label"],
            min_value=1,
            value=15000,
            step=100,
        )
        success_b = st.number_input(
            selected_metric["success_b_label"],
            min_value=0,
            value=1650,
            step=10,
        )

        st.markdown("#### Параметры")
        alpha = st.number_input(
            "alpha",
            min_value=0.0001,
            max_value=0.9999,
            value=0.05,
            step=0.01,
            format="%g",
        )

        submitted = st.form_submit_button("Рассчитать", use_container_width=True)

with right:
    st.markdown("#### Результаты")

if submitted:
    errors = []

    if n_a <= 0:
        errors.append(f"{selected_metric['n_a_label']} должно быть больше 0.")
    if n_b <= 0:
        errors.append(f"{selected_metric['n_b_label']} должно быть больше 0.")
    if success_a < 0:
        errors.append(f"{selected_metric['success_a_label']} не может быть отрицательным.")
    if success_b < 0:
        errors.append(f"{selected_metric['success_b_label']} не может быть отрицательным.")
    if success_a > n_a:
        errors.append(
            f"{selected_metric['success_a_label']} не может превышать {selected_metric['n_a_label'].lower()}."
        )
    if success_b > n_b:
        errors.append(
            f"{selected_metric['success_b_label']} не может превышать {selected_metric['n_b_label'].lower()}."
        )
    if not 0 < alpha < 1:
        errors.append("Параметр alpha должен быть в диапазоне (0, 1).")

    with right:
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

                st.markdown('<div class="result-panel">', unsafe_allow_html=True)
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
                st.markdown("</div>", unsafe_allow_html=True)

                is_significant = (p_value < alpha) and not (ci_low <= 0 <= ci_high)

                if is_significant and diff > 0:
                    st.success(
                        f"Разница статистически значима: test показывает более высокую {selected_metric['title']}, чем control."
                    )
                elif is_significant and diff < 0:
                    st.warning(
                        f"Разница статистически значима: test показывает более низкую {selected_metric['title']}, чем control."
                    )
                else:
                    st.info(
                        f"Статистически значимого различия по {selected_metric['title']} между группами не обнаружено."
                    )

                st.caption(
                    "Для бинарных метрик используется двусторонний z-тест для двух пропорций."
                )
else:
    with right:
        st.info("Заполните форму слева и нажмите «Рассчитать».")
