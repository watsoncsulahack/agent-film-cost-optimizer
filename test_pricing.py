"""Unit tests for deterministic pricing normalization function."""

from decimal import Decimal
import pytest

from cost_optimizer_agent.pricing import (
    normalize_price_to_dollars_per_second,
    get_normalized_pricing_breakdown,
)


def test_standard_time_units():
    # Direct per second
    assert normalize_price_to_dollars_per_second(0.05, unit="second") == 0.05
    assert normalize_price_to_dollars_per_second(0.05, unit="sec") == 0.05
    assert normalize_price_to_dollars_per_second(0.05, unit="s") == 0.05

    # Per minute: $3.00 / min = $0.05 / sec
    assert normalize_price_to_dollars_per_second(3.00, unit="minute") == 0.05
    assert normalize_price_to_dollars_per_second(3.00, unit="min") == 0.05

    # Per hour: $180.00 / hr = $0.05 / sec
    assert normalize_price_to_dollars_per_second(180.00, unit="hour") == 0.05
    assert normalize_price_to_dollars_per_second(180.00, unit="hr") == 0.05

    # Per day: $8640.00 / day = $0.10 / sec
    assert normalize_price_to_dollars_per_second(8640.00, unit="day") == 0.10


def test_frame_based_pricing():
    # $0.002 per frame @ 24 fps = $0.048 / sec
    assert normalize_price_to_dollars_per_second(0.002, unit="frame", fps=24) == 0.048

    # $0.001 per frame @ 60 fps = $0.06 / sec
    assert normalize_price_to_dollars_per_second(0.001, unit="frame", fps=60) == 0.06

    # $0.002 per frame @ 30 fps = $0.06 / sec
    assert normalize_price_to_dollars_per_second(0.002, unit="frame", fps=30) == 0.06


def test_shot_based_pricing():
    # $0.35 per 5-second shot = $0.07 / sec
    assert normalize_price_to_dollars_per_second(0.35, unit="shot", duration_seconds=5.0) == 0.07

    # $1.00 per 10-second generation = $0.10 / sec
    assert normalize_price_to_dollars_per_second(1.00, unit="generation", duration_seconds=10.0) == 0.10


def test_credit_based_pricing():
    # 10 credits for 5-sec shot, $0.035 per credit -> $0.35 / 5s = $0.07 / sec
    assert normalize_price_to_dollars_per_second(
        price=10,
        unit="credits",
        cost_per_credit=0.035,
        duration_seconds=5.0,
    ) == 0.07

    # 5 credits/sec at $0.01/credit = $0.05/sec
    assert normalize_price_to_dollars_per_second(
        price=5,
        unit="credits",
        cost_per_credit=0.01,
    ) == 0.05


def test_string_rate_parsing():
    # '$0.05/sec'
    assert normalize_price_to_dollars_per_second("$0.05/sec") == 0.05

    # '$3.00/min'
    assert normalize_price_to_dollars_per_second("$3.00/min") == 0.05

    # '$180/hr'
    assert normalize_price_to_dollars_per_second("$180/hr") == 0.05

    # '$0.35/5s'
    assert normalize_price_to_dollars_per_second("$0.35/5s") == 0.07

    # '$0.002/frame @ 30fps'
    assert normalize_price_to_dollars_per_second("$0.002/frame @ 30fps") == 0.06


def test_determinism_and_decimal_types():
    # Decimal input
    d_price = Decimal("0.05")
    assert normalize_price_to_dollars_per_second(d_price, unit="second") == 0.05

    # Exact decimal representation test for 1/3 dollar per minute -> $0.005556/sec
    res1 = normalize_price_to_dollars_per_second(1.0 / 3.0, unit="minute", round_digits=6)
    res2 = normalize_price_to_dollars_per_second(1.0 / 3.0, unit="minute", round_digits=6)
    assert res1 == res2


def test_breakdown_helper():
    breakdown = get_normalized_pricing_breakdown(0.05, unit="second")
    assert breakdown.dollars_per_second == 0.05
    assert breakdown.dollars_per_minute == 3.0
    assert breakdown.dollars_per_hour == 180.0


def test_validation_errors():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        normalize_price_to_dollars_per_second(-1.0, unit="second")

    with pytest.raises(ValueError, match="fps must be strictly positive"):
        normalize_price_to_dollars_per_second(0.05, unit="frame", fps=0)

    with pytest.raises(ValueError, match="duration_seconds is required"):
        normalize_price_to_dollars_per_second(0.35, unit="shot")

    with pytest.raises(ValueError, match="cost_per_credit is required"):
        normalize_price_to_dollars_per_second(10, unit="credits")

    with pytest.raises(ValueError, match="Unrecognized pricing unit"):
        normalize_price_to_dollars_per_second(0.05, unit="lightyears")
