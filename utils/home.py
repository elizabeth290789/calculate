import streamlit as st

from utils.tool_catalog import TOOL_CARDS, ToolCard


def render_home_page() -> None:
    """Render editorial-like landing page with tool cards."""
    hide_sidebar_for_showcase()

    st.markdown("<main class='home-shell'>", unsafe_allow_html=True)
    render_hero()
    st.markdown("<div class='home-divider'></div>", unsafe_allow_html=True)
    render_tools_grid(TOOL_CARDS)
    st.markdown("</main>", unsafe_allow_html=True)


def hide_sidebar_for_showcase() -> None:
    """Keep home page focused on storefront cards instead of sidebar nav."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }
        .block-container { margin-left: auto; margin-right: auto; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
          <p class="hero-eyebrow">Инструменты для A/B экспериментов</p>
          <h1 class="hero-title">Считайте уверенно.<br/>Тестируйте правильно.</h1>
          <p class="hero-subtitle">
            Калькуляторы и аналитические инструменты для планирования,
            проверки и уверенного чтения результатов A/B-тестов.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_tools_grid(cards: tuple[ToolCard, ...]) -> None:
    st.markdown("<h2 class='section-head'>Инструменты</h2>", unsafe_allow_html=True)

    for start_idx in range(0, len(cards), 3):
        row_cards = cards[start_idx : start_idx + 3]
        columns = st.columns(len(row_cards), gap="large")

        for column, card in zip(columns, row_cards, strict=False):
            with column:
                render_tool_card(card)


def render_tool_card(card: ToolCard) -> None:
    st.markdown(
        f"""
        <article class="tool-card">
            <div>
                <div class="tool-card-top">
                    <span class="tool-number">Инструмент {card.number}</span>
                    <span class="tool-status">{card.status}</span>
                </div>
                <h3 class="tool-title">{card.title}</h3>
                <p class="tool-description">{card.description}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(card.page, label="Открыть", icon=card.icon)
    st.markdown("</article>", unsafe_allow_html=True)
