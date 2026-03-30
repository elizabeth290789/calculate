from dataclasses import dataclass


@dataclass(frozen=True)
class ToolCard:
    number: str
    title: str
    description: str
    status: str
    page: str
    icon: str


TOOL_CARDS: tuple[ToolCard, ...] = (
    ToolCard(
        number="01",
        title="Калькулятор размера выборки",
        description="Сценарный расчёт размера выборки и длительности A/B-теста для двух групп.",
        status="Доступно",
        page="pages/1_Калькулятор_размера_выборки.py",
        icon="📐",
    ),
    ToolCard(
        number="02",
        title="Калькулятор MDE",
        description="Оценка минимально детектируемого эффекта по параметрам эксперимента.",
        status="Доступно",
        page="pages/2_Калькулятор_MDE.py",
        icon="📏",
    ),
    ToolCard(
        number="03",
        title="Статкритерий для конверсии",
        description="Проверка статистической значимости различий конверсии между группами.",
        status="Доступно",
        page="pages/3_Статкритерий_для_конверсии.py",
        icon="📊",
    ),
    ToolCard(
        number="04",
        title="Статкритерий для ARPU",
        description="Welch t-test по агрегированным данным (n, mean, std) для ARPU-метрики.",
        status="Доступно",
        page="pages/4_Статкритерий_ARPU.py",
        icon="📈",
    ),
    ToolCard(
        number="05",
        title="Проверка SRM",
        description="Контроль корректности сплита через chi-square goodness-of-fit test.",
        status="Доступно",
        page="pages/5_Проверка_SRM.py",
        icon="✅",
    ),
    ToolCard(
        number="06",
        title="Размер выборки A/B/C test Bonferroni",
        description="Расчёт выборки для трёх групп с поправкой на множественные сравнения.",
        status="Доступно",
        page="pages/6_Размер_выборки_A_B_C_Bonferroni.py",
        icon="🧮",
    ),
)
