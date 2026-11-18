"""
Расчёты: масса удаляемой воды m_w, время сушки tau, класс
"""

from typing import Annotated

from connstans import PI, TAU_SMALL_LIMIT, TAU_LARGE_LIMIT

import math

def mass_removed(
    m: Annotated[float, "Масса влажного материала, кг"],
    w1: Annotated[float, "Начальная влажность, в %"],
    w2: Annotated[float, "Конечная влажность, в %"]) -> float:
    """
    Рассчитать массу удаляемой воды m_w = m · (w1-w2) / (100-w2), кг

    Args:
        m: масса влажного материала, кг
        w1: начальная влажность, в %
        w2: конечная влажность, в %

    Returns:
        масса удаляемой воды, в кг.
    """
    return m * (w1-w2) / (100-w2)


def drying_time(
    k: Annotated[float, "Коэффициент режима"],
    w1: Annotated[float, "Начальная влажность, в %"],
    w2: Annotated[float, "Конечная влажность, в %"]
) -> float:
    """
    Время сушки тау = (1/k) * ln(w1 / w2).

    Args:
        k: коэффициент режима,
        w1: начальная влажность, в %
        w2: конечная влажность, в %

    Returns:
        Время сушки, ч
    """
    return (1 / k) * math.log(w1 / w2)


def tau_class(
    t: Annotated[float, "Время сушки, ч"],
) -> str:
    """
    Классифицировать время сушки через if-elif-else.

    TAU < 2 — быстрая сушка;
    2 ≤ TAU ≤ 12 — нормальная сушка;
    TAU > 12 — длительная сушка.

    Args:
        t: время сушки, ч

    Returns:
        Строка с названием класса времени сушки.
    """
    if t < TAU_SMALL_LIMIT:
        return "быстрая сушка"
    elif t <= TAU_LARGE_LIMIT:
        return "нормальная сушка"
    else:
        return "длительная сушка"