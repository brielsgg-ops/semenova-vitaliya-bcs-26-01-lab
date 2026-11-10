"""Точка входа: демонстрация модульного приложения обработки числовых рядов."""
from __future__ import annotations
import argparse
import sys
from typing import List

from num_series import (
    random_series, sine_series, trend_series,
    summarize,
    simple_moving_average, centered_moving_average, exponential_moving_average,
)

def build_series(kind: str, n: int, seed: int) -> List[float]:
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0, step=1.0, noise=0.5, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")

def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))

def print_header(kind: str, n: int) -> None:
    print("=" * 60)
    print(f"Тип ряда: {kind}, n = {n}")
    print("-" * 60)

def print_stats(stats: dict) -> None:
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана                : {stats['median']:>10.4f}")
    print(f"Размах (max - min)     : {stats['spread']:>10.4f}")
    print(f"min / max              : {stats['min']:>10.4f} / {stats['max']:>10.4f}")

def print_footer() -> None:
    print("=" * 60)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--kind", choices=["random", "sine", "trend"], default="sine", help="тип генерируемого ряда")
    parser.add_argument("--n", type=int, default=20, help="количество точек в ряде")
    parser.add_argument("--window", type=int, default=3, help="размер окна для скользящей средней")
    parser.add_argument("--alpha", type=float, default=0.3, help="коэффициент сглаживания для EMA")
    parser.add_argument("--seed", type=int, default=42, help="зерно ГПСЧ")
    parser.add_argument("--export", metavar="FILE", help="экспорт в CSV")
    parser.add_argument("--json", action="store_true", help="вывод в формате JSON")
    return parser

def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        data = build_series(args.kind, args.n, args.seed)
        stats = summarize(data)
        sma = simple_moving_average(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = centered_moving_average(data, args.window) if args.window % 2 == 1 else None
    except ValueError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return 1

    if args.export:
        import csv
        with open(args.export, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
        print(f"Экспортировано в {args.export}")

    if args.json:
        import json
        print(json.dumps({"data": data, "stats": stats, "sma": sma}, indent=2))

    print_header(args.kind, args.n)
    print_stats(stats)
    print_series("Исходный ряд", data)
    print_series(f"SMA (window={args.window})", sma)
    print_series(f"EMA (alpha={args.alpha})", ema)
    if cma is not None:
        print_series(f"Центрированное MA (window={args.window})", cma)

    print_footer()
    return 0

if __name__ == "__main__":
    main()