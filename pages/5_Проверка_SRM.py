import pandas as pd
import streamlit as st

from utils.calculations import calculate_srm_chi_square
from utils.ui import configure_page, render_tool_header


configure_page(title="Проверка SRM", icon="⚖️")
render_tool_header(
    "Проверка SRM",
    "Проверка соответствия фактического распределения пользователей ожидаемому сплиту эксперимента.",
)

if "srm_observed" not in st.session_state:
    st.session_state.srm_observed = [1000, 1000]
if "srm_expected_shares" not in st.session_state:
    st.session_state.srm_expected_shares = [0.5, 0.5]


def add_group() -> None:
    current_groups = len(st.session_state.srm_observed)
    new_groups = current_groups + 1
    equal_share = 1 / new_groups

    st.session_state.srm_observed = st.session_state.srm_observed + [1000]
    st.session_state.srm_expected_shares = [equal_share] * new_groups


left, right = st.columns([1.15, 1], gap="large")

with left:
    st.button("Добавить группу", on_click=add_group, use_container_width=True)

    with st.form("srm_form"):
        observed_values = []
        expected_share_values = []

        for idx in range(len(st.session_state.srm_observed)):
            col1, col2 = st.columns(2)

            observed = col1.number_input(
                f"Наблюдаемая выборка #{idx + 1}",
                min_value=0,
                value=int(st.session_state.srm_observed[idx]),
                step=1,
                key=f"srm_observed_{idx}",
            )
            expected_share = col2.number_input(
                f"Ожидаемое соотношение #{idx + 1}",
                min_value=0.0,
                value=float(st.session_state.srm_expected_shares[idx]),
                step=0.01,
                format="%g",
                key=f"srm_expected_share_{idx}",
            )

            observed_values.append(int(observed))
            expected_share_values.append(float(expected_share))

        alpha = st.number_input(
            "alpha",
            min_value=0.0001,
            max_value=0.9999,
            value=0.05,
            step=0.01,
            format="%g",
        )

        submitted = st.form_submit_button("Проверить SRM", use_container_width=True)

with right:
    st.markdown("#### Результаты")

if submitted:
    st.session_state.srm_observed = observed_values
    st.session_state.srm_expected_shares = expected_share_values

    errors = []
    groups_count = len(observed_values)

    if groups_count < 2:
        errors.append("Количество групп должно быть не меньше 2.")
    if any(observed < 0 for observed in observed_values):
        errors.append("Наблюдаемый размер группы не может быть отрицательным.")
    if any(share <= 0 for share in expected_share_values):
        errors.append("Все ожидаемые доли должны быть больше 0.")

    expected_share_sum = sum(expected_share_values)
    if abs(expected_share_sum - 1.0) > 1e-6:
        errors.append(
            "Сумма ожидаемых долей должна быть равна 1. Исправьте ввод и повторите расчет."
        )

    if sum(observed_values) == 0:
        errors.append("Общий размер выборки равен 0. Невозможно выполнить проверку SRM.")

    with right:
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                result = calculate_srm_chi_square(
                    observed=observed_values,
                    expected_shares=expected_share_values,
                )
            except ValueError as exc:
                st.error(str(exc))
            else:
                sample_size = result["sample_size"]
                chi2_stat = result["chi2_stat"]
                p_value = result["p_value"]
                degrees_of_freedom = result["degrees_of_freedom"]
                expected_sizes = result["expected_sizes"]
                diffs = result["diffs"]

                st.markdown('<div class="result-panel">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)

                col1.metric("Общий размер выборки", f"{sample_size:,}".replace(",", " "))
                col2.metric("Chi-square statistic", f"{chi2_stat:.6f}")
                col3.metric("p-value", f"{p_value:.6f}")
                col4.metric("Число степеней свободы", f"{degrees_of_freedom}")

                result_table = pd.DataFrame(
                    {
                        "Группа": [f"#{idx + 1}" for idx in range(groups_count)],
                        "Наблюдаемая выборка": observed_values,
                        "Ожидаемая доля": expected_share_values,
                        "Ожидаемый размер выборки": expected_sizes,
                        "Разница (observed - expected)": diffs,
                    }
                )
                st.dataframe(result_table, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                if p_value < alpha:
                    st.warning(
                        "Есть признаки SRM: фактическое распределение по группам статистически "
                        "значимо отличается от ожидаемого. Возможны проблемы с рандомизацией, "
                        "трекингом или качеством данных."
                    )
                else:
                    st.success(
                        "Статистически значимого несоответствия выборочных соотношений не "
                        "обнаружено. Распределение по группам согласуется с ожидаемым сплитом."
                    )
else:
    with right:
        st.info("Укажите параметры слева и запустите проверку.")

st.caption(
    "Для проверки используется chi-square goodness-of-fit test по наблюдаемым размерам "
    "групп и ожидаемым долям."
)
