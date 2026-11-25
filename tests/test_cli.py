"""Интеграционные тесты CLI через subprocess."""

from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.py"


def run_cli(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess:
    """Запустить main.py с аргументами и вернуть результат."""
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        input=input_text,
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=30,
    )


class TestCLI:
    def test_runs_successfully(self):
        r = run_cli("--kind", "sine", "--n", "20", "--window", "3", "--seed", "1")
        assert r.returncode == 0, r.stderr
        assert "Среднее" in r.stdout
        assert "SMA" in r.stdout

    def test_all_kinds_work(self):
        for kind in ("random", "sine", "trend"):
            r = run_cli("--kind", kind, "--n", "10")
            assert r.returncode == 0, f"{kind}: {r.stderr}"

    def test_defaults_work(self):
        r = run_cli()
        assert r.returncode == 0

    def test_invalid_kind_fails(self):
        r = run_cli("--kind", "foo")
        assert r.returncode != 0

    def test_invalid_n_fails_gracefully(self):
        r = run_cli("--n", "-5")
        assert r.returncode == 1
        assert "Ошибка" in r.stderr

    def test_benchmark_flag(self):
        r = run_cli("--kind", "random", "--n", "50", "--window", "5", "--benchmark")
        assert r.returncode == 0, r.stderr
        assert "list" in r.stdout and "deque" in r.stdout


class TestCLIIO:
    """Тесты расширения --save / --load и ввода варианта 10 (--input)."""

    def test_save_then_load(self, tmp_path: Path):
        pytest.importorskip("num_series.io_json")
        path = tmp_path / "series.json"
        r1 = run_cli("--kind", "sine", "--n", "10", "--save", str(path))
        assert r1.returncode == 0, r1.stderr
        assert path.exists()
        r2 = run_cli("--load", str(path), "--window", "3")
        assert r2.returncode == 0, r2.stderr

    def test_load_missing_file_fails(self, tmp_path: Path):
        pytest.importorskip("num_series.io_json")
        r = run_cli("--load", str(tmp_path / "nope.json"))
        assert r.returncode == 1

    def test_variant10_input_file_and_cv_output(self, tmp_path: Path):
        p = tmp_path / "series.txt"
        p.write_text("# входные данные\n2.0\n4.0\n6.0\n8.0\n", encoding="utf-8")
        r = run_cli("--input", str(p), "--window", "2")
        assert r.returncode == 0, r.stderr
        assert "CV" in r.stdout or "вариации" in r.stdout.lower()

    def test_variant10_stdin_dash(self):
        r = run_cli("--input", "-", "--window", "2", input_text="1.0\n2.0\n3.0\n4.0\n")
        assert r.returncode == 0, r.stderr
        assert "Среднее" in r.stdout

    def test_variant10_stdin_bad_line_reports_error_and_exit_1(self):
        r = run_cli("--input", "-", "--window", "2", input_text="1.0\nbad_val\n3.0\n")
        assert r.returncode == 1
        assert "строка 2" in r.stderr