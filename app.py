import streamlit as st

from utils.ui import TOOLS, configure_page, render_tool_cards


configure_page(title="A/B Test Toolkit", icon="📊")

st.markdown(
    """
    <section class="hub-hero">
        <h1 class="hub-title">Считайте правильно.<br>Тестируйте уверенно.</h1>
        <p class="hub-subtitle">Инструменты для A/B-тестирования, проверки гипотез и планирования экспериментов.</p>
        <p class="hub-note">Калькуляторы и проверки для продуктовых, маркетинговых и CRO-экспериментов.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

render_tool_cards("Планирование эксперимента", TOOLS["planning"])
render_tool_cards("Анализ результатов", TOOLS["analysis"])
render_tool_cards("Проверка качества эксперимента", TOOLS["quality"])

st.caption("Используйте каталог выше как основную точку входа в toolkit.")
