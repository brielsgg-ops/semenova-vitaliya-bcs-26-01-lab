"""Тесты модуля num_series.io_file (TXT, CSV, stdin и автовыбор формата)."""

import io
import pytest

from num_series.io_file import (
    load_series_auto,
    load_series_csv,
    load_series_stdin,
    load_series_txt,
)
from num_series.io_json import save_series_json


class TestLoadSeriesTxt:
    def test_valid_txt_with_comments_and_blanks(self, tmp_path):
        p = tmp_path / "data.txt"
        p.write_text("# комментарий\n\n1.5\n-2\n3.25\n", encoding="utf-8")
        assert load_series_txt(p) == [1.5, -2.0, 3.25]

    def test_non_numeric_line_reports_lineno(self, tmp_path):
        p = tmp_path / "bad.txt"
        p.write_text("1.0\n2.0\nabc\n", encoding="utf-8")
        with pytest.raises(ValueError, match=r"строка 3"):
            load_series_txt(p)

    def test_empty_file_raises(self, tmp_path):
        p = tmp_path / "empty.txt"
        p.write_text("# только комментарий\n\n", encoding="utf-8")
        with pytest.raises(ValueError, match="не содержит чисел"):
            load_series_txt(p)


class TestLoadSeriesCsv:
    def test_csv_with_header_and_mixed_separators(self, tmp_path):
        p = tmp_path / "data.csv"
        p.write_text("value1, value2\n1.0, 2.5\n3.0; 4.5\n", encoding="utf-8")
        assert load_series_csv(p) == [1.0, 2.5, 3.0, 4.5]

    def test_csv_non_numeric_on_second_line_raises(self, tmp_path):
        p = tmp_path / "bad.csv"
        p.write_text("1.0, 2.0\n3.0, oops\n", encoding="utf-8")
        with pytest.raises(ValueError, match=r"строка 2"):
            load_series_csv(p)

    def test_csv_missing_file_raises(self, tmp_path):
        with pytest.raises(ValueError, match="не найден"):
            load_series_csv(tmp_path / "absent.csv")


class TestLoadSeriesAuto:
    def test_auto_detects_json_txt_csv(self, tmp_path):
        p_json = tmp_path / "s.json"
        save_series_json([1.0, 2.0], p_json)

        p_txt = tmp_path / "s.txt"
        p_txt.write_text("3.0\n4.0\n", encoding="utf-8")

        p_csv = tmp_path / "s.csv"
        p_csv.write_text("5.0,6.0\n", encoding="utf-8")

        assert load_series_auto(p_json) == [1.0, 2.0]
        assert load_series_auto(p_txt) == [3.0, 4.0]
        assert load_series_auto(p_csv) == [5.0, 6.0]


class TestVariant10StdinAndErrors:
    """Дополнительные проверки варианта 10: чтение из stdin и номер строки при ошибке."""

    def test_load_series_stdin_valid(self):
        stream = io.StringIO("10.0\n-5.5\n2.5\n")
        assert load_series_stdin(stream) == [10.0, -5.5, 2.5]

    def test_load_series_stdin_non_numeric_reports_lineno(self):
        stream = io.StringIO("1.0\nnot_a_number\n3.0\n")
        with pytest.raises(ValueError, match=r"строка 2"):
            load_series_stdin(stream)

    def test_load_series_txt_dash_reads_stdin(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO("7.0\n8.0\n"))
        assert load_series_txt("-") == [7.0, 8.0]