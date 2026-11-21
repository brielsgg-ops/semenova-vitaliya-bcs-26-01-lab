"""Чтение числовых рядов из текстовых файлов и стандартного ввода (stdin)."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, TextIO, Union

PathLike = Union[str, Path]

_SEPARATORS = re.compile(r"[,;\s]+")


# ---------------------------------------------------------------------------
# Внутренние помощники чтения потока с нумерацией строк
# ---------------------------------------------------------------------------
def _parse_single_column_stream(stream: TextIO, source_label: str) -> List[float]:
    """Читает по одному числу на строку из потока; пустые строки и # пропускает."""
    result: List[float] = []
    for lineno, raw in enumerate(stream, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            result.append(float(line))
        except ValueError as err:
            raise ValueError(
                f"{source_label}: строка {lineno}: '{line}' не является числом"
            ) from err

    if not result:
        raise ValueError(f"{source_label} не содержит чисел")
    return result


# ---------------------------------------------------------------------------
# Публичные функции чтения
# ---------------------------------------------------------------------------
def load_series_stdin(stream: TextIO | None = None) -> List[float]:
    """Читает числа из стандартного ввода (по одному числу на строку)."""
    src = sys.stdin if stream is None else stream
    try:
        return _parse_single_column_stream(src, "<stdin>")
    except OSError as err:
        raise ValueError(f"Не удалось прочитать <stdin>: {err}") from err


def load_series_txt(path: PathLike) -> List[float]:
    """Читает числа из .txt (или '-' для stdin) — по одному числу на строку."""
    if str(path) == "-":
        return load_series_stdin()

    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as f:
            return _parse_single_column_stream(f, str(file_path))
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err


def load_series_csv(path: PathLike) -> List[float]:
    """Читает числа из .csv через разделитель, возможно, с заголовком."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                tokens = [t for t in _SEPARATORS.split(line) if t]
                if not tokens:
                    continue
                try:
                    values = [float(t) for t in tokens]
                except ValueError as err:
                    if lineno == 1:
                        continue
                    raise ValueError(
                        f"{file_path}: строка {lineno}: '{line}' содержит нечисловые значения"
                    ) from err
                result.extend(values)
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_auto(path: PathLike) -> List[float]:
    """Автоматически выбирает парсер по расширению или '-' для stdin."""
    if str(path) == "-":
        return load_series_stdin()

    from .io_json import load_series_json

    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return load_series_json(path)
    if suffix in {".txt", ".dat"}:
        return load_series_txt(path)
    if suffix in {".csv", ".tsv"}:
        try:
            return load_series_csv(path)
        except ValueError:
            return load_series_txt(path)
    return load_series_txt(path)


__all__ = [
    "load_series_stdin",
    "load_series_txt",
    "load_series_csv",
    "load_series_auto",
]