import math

# --- Коэффициенты режима обработки (Вариант 10) ---
K_WOOD: float = 0.008    # древесина
K_CERAMICS: float = 0.004    # керамика
K_CORN: float = 0.012    # зерно

# --- Допустимые диапазоны входных данных ---
M_MIN: float = 1.0
M_MAX: float = 5000.0
W1_MIN: float = 5.0
W1_MAX: float = 60.0
W2_MIN: float = 0.0
W2_MAX: float = 30.0
T_MIN: float = 40.0
T_MAX: float = 250.0

# --- Пороговые значения для классификации tau ---
TAU_SMALL_LIMIT: float = 2.0     # tau < 2 — быстрая сушка
TAU_LARGE_LIMIT: float = 12.0    # tau > 12 - длительная сушка

# --- Число пи ---
PI: float = math.pi

# --- Файл журнала ошибок ---
LOG_FILE: str = "Lab4_Semenova_input_error.log"