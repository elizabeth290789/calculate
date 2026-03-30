import streamlit as st

from utils.ui import apply_base_styles


st.set_page_config(
    page_title="A/B Test Toolkit",
    page_icon="📊",
)

apply_base_styles()

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 4vw, 2.85rem);
        line-height: 1.15;
    }

    .hero .sub {
        font-size: 1.06rem;
        color: #374151;
        margin: 1rem 0 0.35rem;
        max-width: 760px;
    }

    .hero .desc {
        font-size: 0.98rem;
        color: #6b7280;
        margin: 0;
    }

    .section-title {
        margin: 1.4rem 0 0.75rem;
        color: #111827;
        font-size: 1.12rem;
        font-weight: 650;
    }

    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1rem 0.95rem;
        min-height: 206px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
        border-color: #d1d5db;
    }

    .badge {
        display: inline-block;
        font-size: 0.75rem;
        color: #1d4ed8;
        background: #eff6ff;
        border: 1px solid #dbeafe;
        border-radius: 999px;
        padding: 0.18rem 0.5rem;
        margin-bottom: 0.75rem;
    }

    .card h4 {
        margin: 0 0 0.5rem;
        font-size: 1rem;
        line-height: 1.3;
    }

    .card p {
        color: #4b5563;
        font-size: 0.92rem;
        min-height: 72px;
        margin: 0 0 0.7rem;
    }

    .status {
        font-size: 0.78rem;
        color: #166534;
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        border-radius: 999px;
        padding: 0.15rem 0.46rem;
        display: inline-block;
        margin-bottom: 0.55rem;
    }

    .open-link {
        margin-top: 0.1rem;
    }

    .open-link a {
        color: #1d4ed8;
        font-weight: 600;
        text-decoration: none;
    }
    .open-link a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <h1>Считайте правильно.<br>Тестируйте уверенно.</h1>
      <p class="sub">Набор инструментов для A/B-тестирования, проверки гипотез и планирования экспериментов.</p>
      <p class="desc">Калькуляторы и проверки для продуктовых, маркетинговых и CRO-экспериментов.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

catalog = [
    (
        "Планирование эксперимента",
        [
            {
                "badge": "01",
                "title": "Калькулятор размера выборки",
                "description": "Сценарный расчет объема выборки и длительности A/B-теста для двух групп.",
                "status": "Готово",
                "page": "pages/1_Калькулятор_размера_выборки.py",
                "icon": "📐",
            },
            {
                "badge": "02",
                "title": "Калькулятор MDE",
                "description": "Оценка минимально детектируемого эффекта по размеру выборки и параметрам теста.",
                "status": "Готово",
                "page": "pages/2_Калькулятор_MDE.py",
                "icon": "📏",
            },
            {
                "badge": "03",
                "title": "Размер выборки для A/B/C с Bonferroni",
                "description": "Расчет выборки для трех групп с поправкой на множественные сравнения.",
                "status": "Готово",
                "page": "pages/6_Размер_выборки_A_B_C_Bonferroni.py",
                "icon": "🧮",
            },
        ],
    ),
    (
        "Анализ результатов",
        [
            {
                "badge": "04",
                "title": "Статкритерий для конверсий",
                "description": "Проверка статистической значимости различий конверсии между группами.",
                "status": "Готово",
                "page": "pages/3_Статкритерий_для_конверсии.py",
                "icon": "📊",
            },
            {
                "badge": "05",
                "title": "Статкритерий для ARPU",
                "description": "Welch t-test по агрегированным данным (n, mean, std) для ARPU-метрики.",
                "status": "Готово",
                "page": "pages/4_Статкритерий_ARPU.py",
                "icon": "📈",
            },
        ],
    ),
    (
        "Проверка качества эксперимента",
        [
            {
                "badge": "06",
                "title": "Проверка SRM",
                "description": "Контроль корректности сплита через chi-square goodness-of-fit test.",
                "status": "Готово",
                "page": "pages/5_Проверка_SRM.py",
                "icon": "✅",
            },
        ],
    ),
]

for section_title, tools in catalog:
    st.markdown(f"<div class='section-title'>{section_title}</div>", unsafe_allow_html=True)
    columns_count = 3 if len(tools) >= 3 else 2
    cols = st.columns(columns_count)

    for idx, tool in enumerate(tools):
        with cols[idx % columns_count]:
            st.markdown(
                f"""
                <div class="card">
                    <span class="badge">#{tool['badge']}</span>
                    <h4>{tool['title']}</h4>
                    <p>{tool['description']}</p>
                    <span class="status">{tool['status']}</span>
                    <div class="open-link"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(tool["page"], label="Открыть", icon=tool["icon"])
