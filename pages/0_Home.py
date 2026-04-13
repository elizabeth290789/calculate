import streamlit as st

st.title("A/B Test Toolkit")

st.write(
    "Инструменты для планирования и анализа A/B-тестов: "
    "оценка размера выборки, MDE, проверка SRM и статистические критерии."
)

st.subheader("Доступные калькуляторы")

st.markdown("- [Калькулятор размера выборки](/sample-size)")
st.markdown("- [MDE](/mde)")
st.markdown("- [SRM](/srm)")
st.markdown("- [Статкритерий](/stat-test)")
st.markdown("- [Bonferroni](/bonferroni)")
st.markdown("- [Статкритерий ARPU](/stat-test-arpu)")
