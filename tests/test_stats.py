"""Тесты модуля num_series.stats (включая CV для варианта 10)."""

import math
import pytest

from num_series.stats import (
    coefficient_of_variation,
    mean,
    median,
    spread,
    stdev,
    summarize,
)


class TestMean:
    @pytest.mark.parametrize(
        "data, expected",
        [
            ([1], 1.0),
            ([1, 2, 3], 2.0),
            ([1, 2, 3, 4], 2.5),
            ([-5, 5], 0.0),
            ([0, 0, 0], 0.0),
        ],
    )
    def test_basic(self, data, expected):
        assert mean(data) == pytest.approx(expected)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            mean([])

    def test_floats(self):
        assert mean([0.1, 0.2, 0.3]) == pytest.approx(0.2)


class TestMedian:
    @pytest.mark.parametrize(
        "data, expected",
        [
            ([1], 1),
            ([1, 2, 3], 2),
            ([3, 1, 2], 2),
            ([1, 2, 3, 4], 2.5),
            ([4, 1, 3, 2], 2.5),
            ([-3, -1, -2], -2),
            ([0, 0, 0, 0], 0),
        ],
    )
    def test_basic(self, data, expected):
        assert median(data) == pytest.approx(expected)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            median([])

    def test_resistant_to_outlier(self):
        clean = [1, 2, 3, 4, 5]
        with_outlier = [1, 2, 3, 4, 1000]
        assert median(clean) == 3
        assert median(with_outlier) == 3


class TestSpread:
    @pytest.mark.parametrize(
        "data, expected",
        [
            ([5], 0),
            ([1, 2, 3], 2),
            ([-10, 10], 20),
            ([0, 0, 0], 0),
        ],
    )
    def test_basic(self, data, expected):
        assert spread(data) == expected

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            spread([])


class TestVariant10StdevAndCV:
    """Тесты выборочного СКО и коэффициента вариации CV = stdev / mean."""

    @pytest.mark.parametrize(
        "data, expected_stdev, expected_cv",
        [
            # [2, 4, 4, 4, 5, 5, 7, 9]: mean = 5.0, sample variance = 32/7, stdev = sqrt(32/7)
            ([2, 4, 4, 4, 5, 5, 7, 9], math.sqrt(32.0 / 7.0), math.sqrt(32.0 / 7.0) / 5.0),
            # [10, 10, 10]: mean = 10.0, stdev = 0.0, cv = 0.0
            ([10, 10, 10], 0.0, 0.0),
            # [2, 6]: mean = 4.0, sample variance = ((2-4)^2 + (6-4)^2) / 1 = 8.0, stdev = sqrt(8), cv = sqrt(8)/4
            ([2, 6], math.sqrt(8.0), math.sqrt(8.0) / 4.0),
        ],
    )
    def test_stdev_and_cv_manual_cases(self, data, expected_stdev, expected_cv):
        assert stdev(data) == pytest.approx(expected_stdev)
        assert coefficient_of_variation(data) == pytest.approx(expected_cv)

    def test_cv_zero_mean_returns_inf(self):
        assert coefficient_of_variation([-1.0, 1.0]) == math.inf

    def test_stdev_single_element_is_zero(self):
        assert stdev([42.0]) == 0.0

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            stdev([])
        with pytest.raises(ValueError, match="пуст"):
            coefficient_of_variation([])


class TestSummarize:
    def test_keys(self):
        s = summarize([1, 2, 3, 4, 5])
        assert {"count", "mean", "median", "spread", "min", "max"}.issubset(set(s))

    def test_values(self):
        s = summarize([1, 2, 3, 4, 5])
        assert s["count"] == 5
        assert s["mean"] == pytest.approx(3.0)
        assert s["median"] == 3
        assert s["spread"] == 4
        assert s["min"] == 1
        assert s["max"] == 5

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            summarize([])