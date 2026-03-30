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
    .landing-wrap {
        display: grid;
        gap: 1.1rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(1200px 300px at 10% -30%, rgba(59, 130, 246, 0.18), transparent 50%),
            radial-gradient(1000px 260px at 90% -20%, rgba(99, 102, 241, 0.16), transparent 50%),
            linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #dbe3f3;
        border-radius: 24px;
        padding: clamp(1.4rem, 4vw, 2.8rem);
        box-shadow: 0 16px 36px rgba(15, 23, 42, 0.08);
        margin-bottom: 0.35rem;
    }

    .hero-title {
        margin: 0;
        max-width: 740px;
        font-size: clamp(2rem, 5vw, 3.25rem);
        line-height: 1.04;
        letter-spacing: -0.03em;
        color: #0b1324;
    }

    .hero-subtitle {
        margin: 1rem 0 0.45rem;
        max-width: 760px;
        font-size: clamp(1rem, 2.2vw, 1.25rem);
        line-height: 1.42;
        color: #1f2937;
    }

    .hero-support {
        margin: 0;
        max-width: 700px;
        font-size: 1rem;
        line-height: 1.5;
        color: #4b5563;
    }

    .group {
        border-top: 1px solid #dce3ef;
        padding-top: 1rem;
        margin-top: 0.35rem;
    }

    .group h3 {
        margin: 0 0 0.8rem;
        font-size: 1.08rem;
        color: #0f172a;
        letter-spacing: -0.01em;
    }

    .tool-card {
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border: 1px solid #d9e2f0;
        border-radius: 16px;
        padding: 0.95rem 0.95rem 0.8rem;
        min-height: 232px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
        margin-bottom: 0.8rem;
    }

    .tool-card:hover {
        transform: translateY(-4px);
        border-color: #bfccdf;
        box-shadow: 0 16px 32px rgba(15, 23, 42, 0.1);
    }

    .tool-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.72rem;
    }

    .tool-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: 1.55rem;
        min-width: 1.9rem;
        padding: 0 0.45rem;
        border-radius: 999px;
        border: 1px solid #bfdbfe;
        background: #eff6ff;
        color: #1d4ed8;
        font-weight: 700;
        font-size: 0.78rem;
    }

    .tool-status {
        display: inline-flex;
        align-items: center;
        padding: 0.14rem 0.52rem;
        border-radius: 999px;
        border: 1px solid #bbf7d0;
        background: #f0fdf4;
        color: #166534;
        font-size: 0.76rem;
        font-weight: 600;
    }

    .tool-title {
        margin: 0 0 0.45rem;
        min-height: 2.6rem;
        font-size: 1rem;
        line-height: 1.3;
        color: #111827;
    }

    .tool-desc {
        margin: 0 0 0.9rem;
        min-height: 3.8rem;
        color: #4b5563;
        font-size: 0.92rem;
        line-height: 1.45;
    }

    [data-testid="stPageLink"] a {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #111827;
        color: #ffffff !important;
        border: 1px solid #0f172a;
        border-radius: 10px;
        padding: 0.34rem 0.66rem;
        font-size: 0.86rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: transform 0.12s ease, background 0.12s ease;
    }

    [data-testid="stPageLink"] a:hover {
        background: #1f2937;
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='landing-wrap'>", unsafe_allow_html=True)
st.markdown(
    """
    <section class="hero">
      <h1 class="hero-title">Считайте правильно.<br>Тестируйте уверенно.</h1>
      <p class="hero-subtitle">Инструменты для A/B-тестирования, проверки гипотез и планирования экспериментов.</p>
      <p class="hero-support">Калькуляторы и проверки для продуктовых, маркетинговых и CRO-экспериментов.</p>
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
    st.markdown(f"<section class='group'><h3>{section_title}</h3>", unsafe_allow_html=True)
    columns_count = min(3, max(2, len(tools)))
    cols = st.columns(columns_count)

    for idx, tool in enumerate(tools):
        with cols[idx % columns_count]:
            st.markdown(
                f"""
                <article class="tool-card">
                    <div class="tool-meta">
                        <span class="tool-badge">#{tool['badge']}</span>
                        <span class="tool-status">{tool['status']}</span>
                    </div>
                    <h4 class="tool-title">{tool['title']}</h4>
                    <p class="tool-desc">{tool['description']}</p>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(tool["page"], label="Открыть", icon=tool["icon"])
            st.markdown("</article>", unsafe_allow_html=True)

    st.markdown("</section>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
