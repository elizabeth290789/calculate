from __future__ import annotations

import streamlit as st


TOOLS = {
    "planning": [
        {
            "id": "01",
            "title": "Калькулятор размера выборки",
            "description": "Сценарный расчет выборки и длительности A/B-теста для двух групп.",
            "status": "готово",
            "path": "pages/1_Калькулятор_размера_выборки.py",
        },
        {
            "id": "02",
            "title": "Калькулятор MDE",
            "description": "Оценка минимально детектируемого эффекта при текущем объеме данных.",
            "status": "готово",
            "path": "pages/2_Калькулятор_MDE.py",
        },
        {
            "id": "03",
            "title": "Размер выборки для A/B/C с Bonferroni",
            "description": "Расчет выборки для трех групп с поправкой на множественные сравнения.",
            "status": "beta",
            "path": "pages/6_Размер_выборки_A_B_C_Bonferroni.py",
        },
    ],
    "analysis": [
        {
            "id": "04",
            "title": "Статкритерий для конверсий",
            "description": "Двусторонний z-тест для сравнения двух пропорций.",
            "status": "готово",
            "path": "pages/3_Статкритерий_для_конверсии.py",
        },
        {
            "id": "05",
            "title": "Статкритерий для ARPU",
            "description": "Welch t-test по агрегированным данным (n, mean, std).",
            "status": "готово",
            "path": "pages/4_Статкритерий_ARPU.py",
        },
    ],
    "quality": [
        {
            "id": "06",
            "title": "Проверка SRM",
            "description": "Chi-square goodness-of-fit test для проверки корректности сплита.",
            "status": "готово",
            "path": "pages/5_Проверка_SRM.py",
        }
    ],
}


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6f8fb;
            --surface: #ffffff;
            --text: #0f172a;
            --muted: #52607a;
            --line: #dbe1ea;
            --accent: #2253d9;
            --badge: #eef2ff;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: #f9fbff;
            border-right: 1px solid var(--line);
        }

        .hub-hero {
            background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 2.2rem;
            margin-bottom: 1.8rem;
        }

        .hub-title {
            font-size: clamp(1.9rem, 2.7vw, 2.9rem);
            line-height: 1.1;
            margin: 0;
            color: var(--text);
            letter-spacing: -0.02em;
        }

        .hub-subtitle {
            color: #334155;
            font-size: 1.08rem;
            margin: 0.9rem 0 0.4rem;
        }

        .hub-note {
            color: var(--muted);
            margin: 0;
            font-size: 0.98rem;
        }

        .tool-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1rem 1rem 0.4rem;
            margin-bottom: 1rem;
            min-height: 210px;
            transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
        }

        .tool-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08);
            border-color: #c9d4e3;
        }

        .tool-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.7rem;
        }

        .tool-id {
            font-size: 0.76rem;
            color: #475569;
            background: #f1f5f9;
            padding: 0.26rem 0.5rem;
            border-radius: 999px;
            font-weight: 600;
        }

        .tool-status {
            font-size: 0.74rem;
            color: #1e3a8a;
            background: var(--badge);
            padding: 0.26rem 0.5rem;
            border-radius: 999px;
            font-weight: 600;
        }

        .tool-title {
            margin: 0;
            color: var(--text);
            font-size: 1.02rem;
        }

        .tool-description {
            color: var(--muted);
            margin: 0.55rem 0 0.9rem;
            min-height: 64px;
            font-size: 0.92rem;
        }

        .section-title {
            margin-top: 0.8rem;
            margin-bottom: 0.7rem;
            color: #0f172a;
            font-size: 1.1rem;
            letter-spacing: -0.01em;
        }

        .tool-header {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        .tool-header h1 {
            margin: 0;
            font-size: 1.5rem;
            color: #0f172a;
        }

        .tool-header p {
            margin: 0.45rem 0 0;
            color: var(--muted);
        }

        .result-panel {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### A/B Toolkit")
        st.caption("Каталог инструментов для экспериментов")

        st.page_link("app.py", label="🏠 Главная", icon="")
        st.markdown("---")
        st.markdown("**Планирование**")
        st.page_link("pages/1_Калькулятор_размера_выборки.py", label="Размер выборки")
        st.page_link("pages/2_Калькулятор_MDE.py", label="Калькулятор MDE")
        st.page_link("pages/6_Размер_выборки_A_B_C_Bonferroni.py", label="A/B/C Bonferroni")

        st.markdown("**Анализ результатов**")
        st.page_link("pages/3_Статкритерий_для_конверсии.py", label="Статкритерий конверсий")
        st.page_link("pages/4_Статкритерий_ARPU.py", label="Статкритерий ARPU")

        st.markdown("**Качество эксперимента**")
        st.page_link("pages/5_Проверка_SRM.py", label="Проверка SRM")


def configure_page(*, title: str, icon: str) -> None:
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    apply_global_styles()
    render_sidebar()


def render_tool_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="tool-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tool_cards(section_title: str, cards: list[dict]) -> None:
    st.markdown(f"<h3 class='section-title'>{section_title}</h3>", unsafe_allow_html=True)

    for i in range(0, len(cards), 3):
        row = cards[i : i + 3]
        cols = st.columns(3)
        for col, card in zip(cols, row):
            with col:
                st.markdown(
                    f"""
                    <div class="tool-card">
                        <div class="tool-meta">
                            <span class="tool-id">{card['id']}</span>
                            <span class="tool-status">{card['status']}</span>
                        </div>
                        <h4 class="tool-title">{card['title']}</h4>
                        <p class="tool-description">{card['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Открыть", key=f"open_{card['id']}", use_container_width=True):
                    st.switch_page(card["path"])
