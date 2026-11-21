"""Модуль базовых статистических показателей и коэффициента вариации."""

from __future__ import annotations

import math
from typing import Dict, Sequence


# ---------------------------------------------------------------------------
# Валидация (единая точка отказа - fail fast)
# ---------------------------------------------------------------------------
def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


# ---------------------------------------------------------------------------
# Базовые и дополнительные показатели (Вариант 10: CV = stdev / mean)
# ---------------------------------------------------------------------------
def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0


def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))


def stdev(data: Sequence[float]) -> float:
    """Выборочное среднее квадратическое отклонение (СКО, знаменатель n - 1)."""
    _ensure_not_empty(data)
    n = len(data)
    if n < 2:
        return 0.0
    m = mean(data)
    sq_diff_sum = sum((float(x) - m) ** 2 for x in data)
    return math.sqrt(sq_diff_sum / (n - 1))


def coefficient_of_variation(data: Sequence[float]) -> float:
    """Коэффициент вариации CV = stdev / mean.

    При mean == 0 возвращает math.inf.
    """
    _ensure_not_empty(data)
    m = mean(data)
    if m == 0.0:
        return math.inf
    return stdev(data) / m


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max, stdev, cv."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
        "stdev": stdev(data),
        "cv": coefficient_of_variation(data),
    }


__all__ = [
    "mean",
    "median",
    "spread",
    "stdev",
    "coefficient_of_variation",
    "summarize",
]