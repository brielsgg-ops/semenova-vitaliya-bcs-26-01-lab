"""Пакет алгоритмической обработки числовых рядов.

Публичный API пакета:
- Генерация ряда: random_series, sine_series, trend_series
- Статистика: mean, median, spread, summarize
- Скользящие средние: simple_moving_average, simple_moving_average_deque,
                      centered_moving_average, exponential_moving_average,
                      benchmark_moving_average
"""

from .generator import random_series, sine_series, trend_series
from .stats import mean, median, spread, summarize
from .moving_average import (
    simple_moving_average,
    simple_moving_average_deque,
    centered_moving_average,
    exponential_moving_average,
    benchmark_moving_average,
)

__all__ = [
    # генерация
    "random_series",
    "sine_series",
    "trend_series",
    # статистика
    "mean",
    "median",
    "spread",
    "summarize",
    # скользящие средние
    "simple_moving_average",
    "simple_moving_average_deque",
    "centered_moving_average",
    "exponential_moving_average",
    "benchmark_moving_average",
]

__version__ = "1.0.1"