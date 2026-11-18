"""
Валидация пользовательского ввода.
- Проверка границ через if-elif-else.
- Циклический ввод до корректного значения.
"""

from __future__ import annotations

from connstans import M_MAX, M_MAX, W1_MIN, W1_MAX, W2_MIN, W2_MAX, T_MIN, T_MAX
from logger import log_error


def validate_range(value: float, low: float, high: float) -> tuple[bool, str]:
    """
    Проверка попадания value в [low, high] через if-elif-else.
    :return: (True, "") или (False, сообщение)
    """
    if value < low:
        return False, f"Ошибка: значение меньше нижней границы ({low})."
    elif value > high:
        return False, f"Ошибка: значение больше верхней границы ({high})."
    else:
        return True, ""


def input_number(prompt: str, low: float, high: float) -> float:
    """
    Циклически запрашивать число, пока не будет корректного.
    Проверяет тип (float) через try/except ValueError и границы.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError as e:
            msg = str(e.args[0]) if e.args else str(e)
            msg = f"Ошибка: введено не число ('{raw}'). {msg}"
            print(msg)
            log_error(msg)
            continue

        ok, msg = validate_range(value, low, high)
        if ok:
            return value
        print(msg + " Повторите ввод.")
        log_error(msg)


def input_mass() -> float:
    """Циклический ввод m, допустимо 1..5000."""
    return input_number(
        "Введите массу влажного материала m в кг (1..5000): ",
        M_MAX, M_MAX
    )


def input_humidity1() -> float:
    """Циклический ввод начальной влажности w1 в процентах, допустимо 5..60."""
    return input_number(
        "Введите начальную влажность w1 в процентах, (5..60): ",
        W1_MIN, W1_MAX,
    )


def input_humidity2() -> float:
    """Циклический ввод начальной влажности w2 в процентах, допустимо 0..30."""
    return input_number(
        "Введите начальную влажность w2 в процентах, (0..30): ",
        W2_MIN, W2_MAX,
    )

def input_temp() -> float:
    """Циклический ввод температуры в градусах Цельсия, допустимо 40..250."""
    return input_number(
        "Введите температуру в градусах Цельсия, (0..250): ",
        T_MIN, T_MAX,
    )
