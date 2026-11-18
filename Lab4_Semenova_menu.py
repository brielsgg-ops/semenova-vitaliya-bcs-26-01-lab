"""
Меню выбора материала через match-case.
"""

from __future__ import annotations

from connstans import K_WOOD, K_CERAMICS, K_CORN


def show_menu() -> None:
    """Вывести меню режимов."""
    print("\n Выберите материал:")
    print("  1 — древесина (k = 0.008)")
    print("  2 — керамика      (k = 0.004)")
    print("  3 — зерно          (k = 0.012)")
    print("  0 — выход")


def select_mode() -> float | None:
    """
    Циклически запрашивать материал и возвращать коэффициент k.

    Использует match-case для маршрутизации.
    Возвращает None, если выбран выход (0).
    """
    while True:
        choice = input("Введите номер режима (от 0 до 3): ").strip()
        match choice:
            case "1":
                return K_WOOD
            case "2":
                return K_CERAMICS
            case "3":
                return K_CORN
            case "0":
                return None
            case _:
                print("Ошибка: неверный пункт меню. Повторите ввод.")


def mode_name(k: float) -> str:
    """Вернуть название режима по коэффициенту k."""
    match k:
        case 0.008:
            return "древесина"
        case 0.004:
            return "керамика"
        case 0.012:
            return "зерно"
        case _:
            return "неизвестный"