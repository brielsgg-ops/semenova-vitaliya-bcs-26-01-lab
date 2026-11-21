"""Точка входа: обработка числовых рядов (Вариант 10).

Примеры запуска:
python main.py --input data/series.txt --window 10 --alpha 0.3
python main.py --input - --window 10
python main.py --kind sine --n 1000 --window 10 --benchmark
"""

from __future__ import annotations

import argparse
import csv
import sys
from typing import List, Optional, Tuple

from num_series import (
    random_series,
    sine_series,
    trend_series,
    summarize,
    simple_moving_average,
    simple_moving_average_deque,
    exponential_moving_average,
    benchmark_moving_average,
    save_series_json,
    load_series_auto,
)


# ---------------------------------------------------------------------------
# Источники данных
# ---------------------------------------------------------------------------
def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Генерирует ряд заданного типа."""
    if kind == "random":
        return random_series(n, low=-50.0, high=50.0, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10.0, frequency=2.0, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0.0, step=1.0, noise=0.5, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")


def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника). Поддерживает --input файл или '-'."""
    source_path = args.input if args.input is not None else args.load
    if source_path is not None:
        data = load_series_auto(source_path)
        label = "<stdin>" if str(source_path) == "-" else f"файл: {source_path}"
        return data, label

    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"


# ---------------------------------------------------------------------------
# Экспорт в CSV
# ---------------------------------------------------------------------------
def export_series_csv(path: str, data: List[float]) -> None:
    """Экспорт ряда в CSV: столбцы i, value. Ошибки нормализуются в ValueError."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
    except OSError as err:
        raise ValueError(f"Не удалось записать CSV {path}: {err}") from err


# ---------------------------------------------------------------------------
# Печать
# ---------------------------------------------------------------------------
def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    """Печатает ряд в одну строку с выравниванием."""
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))


def print_header(source: str) -> None:
    print("=" * 60)
    print(f"Источник данных: {source}")
    print("-" * 60)


def print_stats(stats: dict) -> None:
    """Печатает блок базовых статистик и коэффициента вариации (Вариант 10)."""
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана               : {stats['median']:>10.4f}")
    print(f"Размах (max - min)    : {stats['spread']:>10.4f}")
    print(f"СКО (выборочное)      : {stats['stdev']:>10.4f}")
    print(f"Коэф. вариации (CV)   : {stats['cv']:>10.4f}")
    print(f"min / max             : {stats['min']:>10.4f} / {stats['max']:.4f}")


def print_footer() -> None:
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов (Вариант 10)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Пример: python main.py --input series.txt --window 10",
    )
    # источники (по умолчанию n=1000 и window=10 как задано для вариантов)
    parser.add_argument(
        "--input",
        metavar="FILE_OR_DASH",
        default=None,
        help="входной ряд из файла (по числу в строке) или '-' для stdin",
    )
    parser.add_argument(
        "--load",
        metavar="PATH",
        default=None,
        help="загрузить ряд из файла (.json/.txt/.csv); отменяет --kind/--n/--seed",
    )
    parser.add_argument(
        "--kind",
        choices=["random", "sine", "trend"],
        default="sine",
        help="тип генерируемого ряда",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1000,
        help="количество точек в ряде",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="зерно ГПСЧ для воспроизводимости",
    )
    # экспорт и бенчмарк
    parser.add_argument(
        "--save",
        metavar="PATH",
        default=None,
        help="сохранить ряд в JSON-файл",
    )
    parser.add_argument(
        "--export",
        metavar="FILE",
        default=None,
        help="экспортировать ряд в CSV (i, value)",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="замерить время выполнения SMA для list и deque",
    )
    # анализ
    parser.add_argument(
        "--window",
        type=int,
        default=10,
        help="размер окна для скользящей средней",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.3,
        help="коэффициент сглаживания для EMA, 0 < alpha <= 1",
    )
    return parser


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv: Optional[List[str]] = None) -> int:
    """Точка входа. Возвращает код выхода (0 — успех, 1 — ошибка)."""
    args = build_parser().parse_args(argv)

    # --- 1. Получаем ряд
    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1

    # --- 2. Сохраняем / экспортируем
    if args.save:
        meta = {"source": source}
        if args.input is None and args.load is None:
            meta.update({"kind": args.kind, "seed": args.seed})
        try:
            save_series_json(data, args.save, meta=meta)
            print(f"[сохранено] {args.save} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка сохранения: {err}", file=sys.stderr)
            return 1

    if args.export:
        try:
            export_series_csv(args.export, data)
            print(f"[экспортировано] {args.export} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка экспорта: {err}", file=sys.stderr)
            return 1

    # --- 3. Анализ (SMA list, SMA deque, EMA, статистика с CV)
    try:
        stats = summarize(data)
        sma_list = simple_moving_average(data, args.window)
        sma_deque = simple_moving_average_deque(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1

    # --- 4. Вывод
    print_header(source)
    print_stats(stats)
    print_series("Исходный ряд", data)
    print_series(f"SMA list (window={args.window})", sma_list)
    print_series(f"SMA deque (window={args.window})", sma_deque)
    print_series(f"EMA (alpha={args.alpha})", ema)

    if args.benchmark:
        print("-" * 60)
        print("Замер времени выполнения SMA (среднее за 1000 повторов):")
        timings = benchmark_moving_average(data, args.window, repeats=1000)
        print(f"  list  : {timings['list']:.8f} c")
        print(f"  deque : {timings['deque']:.8f} c")
        if timings["deque"] > 0:
            print(f"  отношение (list/deque): {timings['list'] / timings['deque']:.2f}")

    print_footer()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())