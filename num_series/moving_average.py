from typing import List, Sequence

# Функция валидации из задания
def _check_window(window: int, n: int) -> None:
    """Проверяет, что окно является целым числом >= 1 и не превышает длину ряда."""
    if window < 1:
        raise ValueError(f"Размер окна должен быть >= 1 (получено: {window})")
    if window > n:
        raise ValueError(f"Окно больше ряда: window={window}, n={n}")


# ОБЯЗАТЕЛЬНОЕ ЗАДАНИЕ (через бегущую сумму O(n))
def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простая скользящая средняя (SMA).
    Оптимизирована через бегущую сумму, сложность O(n)."""
    n = len(data)
    _check_window(window, n)

    running = sum(data[:window])
    result = [running / window]
    
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
        
    return result


# САМОСТОЯТЕЛЬНОЕ ЗАДАНИЕ 1
def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированная скользящая средняя (CMA).
    Окно должно быть нечётным, выход выровнен по центру."""
    n = len(data)
    _check_window(window, n)
    
    if window % 2 == 0:
        raise ValueError("Для центрированного MA окно должно быть нечётным")

    half = window // 2
    result = []
    
    # Идём по точкам, для которых есть полное окно слева и справа
    for i in range(half, n - half):
        current_window = data[i - half : i + half + 1]
        result.append(sum(current_window) / window)
        
    return result


# САМОСТОЯТЕЛЬНОЕ ЗАДАНИЕ 2
def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Экспоненциальная скользящая средняя (EMA).
    Формула: EMA[i] = alpha * data[i] + (1 - alpha) * EMA[i-1]"""
    if not data:
        return []
        
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должна быть в диапазоне (0, 1] (получено: {alpha})")

    result = [data[0]] # EMA[0] = data[0]
    
    for i in range(1, len(data)):
        ema_current = alpha * data[i] + (1 - alpha) * result[i - 1]
        result.append(ema_current)
        
    return result