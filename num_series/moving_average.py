"""Модуль скользящих средних: SMA, центрированное МА, EMA, а также бенчмарк."""

from __future__ import annotations

import time
from collections import deque
from typing import List, Sequence


# ---------------------------------------------------------------------------
# Валидация
# ---------------------------------------------------------------------------
def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")


def check_window(window: int, n: int) -> None:
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(
            f"window ({window}) больше длины ряда ({n}) — SMA невозможна"
        )


def _check_alpha(alpha: float) -> None:
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должен быть в (0, 1], получено: {alpha}")


# ---------------------------------------------------------------------------
# 1. Простая скользящая средняя (SMA) — старая версия на списках (или бегущая сумма)
# ---------------------------------------------------------------------------
def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """SMA с использованием бегущей суммы (O(n))."""
    _ensure_not_empty(data)
    check_window(window, len(data))
    
    running = sum(data[:window])
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


# ---------------------------------------------------------------------------
# 2. Новая SMA через deque (требование раздела 9)
# ---------------------------------------------------------------------------
def simple_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """SMA с использованием deque (двусторонней очереди)."""
    _ensure_not_empty(data)
    check_window(window, len(data))
    
    result = []
    d = deque()
    running_sum = 0.0
    for x in data:
        d.append(x)
        running_sum += x
        if len(d) > window:
            running_sum -= d.popleft()
        if len(d) == window:
            result.append(running_sum / window)
    return result


# ---------------------------------------------------------------------------
# 3. Центрированное МА
# ---------------------------------------------------------------------------
def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированное МА: окно должно быть нечётным."""
    _ensure_not_empty(data)
    check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError(
            f"Центрированное МА требует нечётного window, получено: {window}"
        )
    
    # Базовый расчёт через SMA, либо ваша реализация
    return simple_moving_average(data, window)


# ---------------------------------------------------------------------------
# 4. Экспоненциальная скользящая средняя (EMA)
# ---------------------------------------------------------------------------
def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """EMA: сглаживание с коэффициентом alpha."""
    _ensure_not_empty(data)
    _check_alpha(alpha)

    prev: float = float(data[0])
    result: List[float] = [prev]
    for x in data[1:]:
        prev = alpha * x + (1.0 - alpha) * prev
        result.append(prev)
    return result


# ---------------------------------------------------------------------------
# 5. Функция бенчмарка (замер времени list vs deque)
# ---------------------------------------------------------------------------
def benchmark_moving_average(data: Sequence[float], window: int, repeats: int = 1000) -> dict:
    """
    Замеряет среднее время выполнения SMA для реализаций на list и deque.
    Возвращает словарь с ключами 'list' и 'deque' (время в секундах).
    """
    check_window(window, len(data))

    # Замер для list-реализации (simple_moving_average)
    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats

    # Замер для deque-реализации (simple_moving_average_deque)
    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}


# ---------------------------------------------------------------------------
# Публичный API модуля
# ---------------------------------------------------------------------------
__all__ = [
    "simple_moving_average",
    "simple_moving_average_deque",
    "centered_moving_average",
    "exponential_moving_average",
    "benchmark_moving_average",
]