"""Пакет алгоритмической обработки числовых рядов (Вариант 10)."""

from .generator import random_series, sine_series, trend_series
from .stats import (
    mean,
    median,
    spread,
    stdev,
    coefficient_of_variation,
    summarize,
)
from .moving_average import (
    simple_moving_average,
    simple_moving_average_deque,
    centered_moving_average,
    exponential_moving_average,
    benchmark_moving_average,
)
from .deque_average import (
    centered_moving_average_deque,
    exponential_moving_average_deque,
)
from .io_json import save_series_json, load_series_json
from .io_file import (
    load_series_stdin,
    load_series_txt,
    load_series_csv,
    load_series_auto,
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
    "stdev",
    "coefficient_of_variation",
    "summarize",
    # скользящие средние и бенчмарк
    "simple_moving_average",
    "simple_moving_average_deque",
    "centered_moving_average",
    "centered_moving_average_deque",
    "exponential_moving_average",
    "exponential_moving_average_deque",
    "benchmark_moving_average",
    # ввод-вывод
    "save_series_json",
    "load_series_json",
    "load_series_stdin",
    "load_series_txt",
    "load_series_csv",
    "load_series_auto",
]

__version__ = "1.1.1"