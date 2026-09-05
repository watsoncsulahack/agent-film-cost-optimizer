"""Deterministic pricing normalization utilities for AI video and film production."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional, Union

# Base unit multipliers in seconds
TIME_UNIT_SECONDS: dict[str, Decimal] = {
    "s": Decimal("1"),
    "sec": Decimal("1"),
    "second": Decimal("1"),
    "seconds": Decimal("1"),
    "m": Decimal("60"),
    "min": Decimal("60"),
    "minute": Decimal("60"),
    "minutes": Decimal("60"),
    "h": Decimal("3600"),
    "hr": Decimal("3600"),
    "hour": Decimal("3600"),
    "hours": Decimal("3600"),
    "d": Decimal("86400"),
    "day": Decimal("86400"),
    "days": Decimal("86400"),
}


@dataclass(frozen=True)
class NormalizedPrice:
    """Represents a deterministically normalized price breakdown."""
    dollars_per_second: float
    dollars_per_minute: float
    dollars_per_hour: float
    input_price: str
    unit: str
    duration_seconds: Optional[float] = None
    fps: Optional[float] = None


def _to_decimal(val: Union[float, int, str, Decimal]) -> Decimal:
    """Safely converts input numeric or string to Decimal with exact precision."""
    if isinstance(val, Decimal):
        return val
    if isinstance(val, (int, float)):
        return Decimal(str(val))
    if isinstance(val, str):
        cleaned = re.sub(r"[^\d.-]", "", val.strip())
        try:
            return Decimal(cleaned)
        except InvalidOperation as err:
            raise ValueError(f"Cannot parse numeric price value from string: '{val}'") from err
    raise TypeError(f"Unsupported price type: {type(val).__name__}")


def _parse_price_string(price_str: str) -> tuple[Decimal, Optional[str], Optional[Decimal], Optional[Decimal]]:
    """Extracts (amount, unit, duration_seconds, fps) from common rate strings.

    Examples:
        - '$0.05/sec' -> (Decimal('0.05'), 'second', None, None)
        - '$0.35/5s' -> (Decimal('0.35'), 'shot', Decimal('5'), None)
        - '$3.00/min' -> (Decimal('3.00'), 'minute', None, None)
        - '$0.002/frame @ 30fps' -> (Decimal('0.002'), 'frame', None, Decimal('30'))
    """
    s = price_str.strip().lower()

    # Check for fps modifier like '@ 24fps' or 'at 30 fps'
    fps_match = re.search(r"@\s*(\d+(?:\.\d+)?)\s*fps|at\s*(\d+(?:\.\d+)?)\s*fps", s)
    fps_val = Decimal(fps_match.group(1) or fps_match.group(2)) if fps_match else None
    if fps_match:
        s = s[:fps_match.start()].strip()

    # Pattern: $X / N seconds, e.g., '$0.35 / 5s', '$0.50 per 4 sec'
    custom_dur_match = re.search(
        r"^(?:\$)?\s*([\d.]+)\s*(?:/|per)\s*(\d+(?:\.\d+)?)\s*(?:s|sec|seconds?|second)$", s
    )
    if custom_dur_match:
        amount = Decimal(custom_dur_match.group(1))
        duration = Decimal(custom_dur_match.group(2))
        return amount, "shot", duration, fps_val

    # Pattern: $X / unit (e.g. '$0.05/sec', '$3.00/min', '$180/hr', '$0.001/frame')
    unit_match = re.search(
        r"^(?:\$)?\s*([\d.]+)\s*(?:/|per)\s*([a-zA-Z_]+)$", s
    )
    if unit_match:
        amount = Decimal(unit_match.group(1))
        unit_name = unit_match.group(2)
        return amount, unit_name, None, fps_val

    # Plain number
    amount = _to_decimal(price_str)
    return amount, None, None, fps_val


def normalize_price_to_dollars_per_second(
    price: Union[float, int, str, Decimal],
    unit: Optional[str] = None,
    duration_seconds: Optional[Union[float, int, Decimal]] = None,
    fps: Union[float, int, Decimal] = 24.0,
    cost_per_credit: Optional[Union[float, int, Decimal]] = None,
    round_digits: Optional[int] = 6,
) -> float:
    """Deterministically normalizes any pricing structure to dollars per second ($/second).

    Supports:
        - Direct unit pricing: 'second', 'minute', 'hour', 'day'
        - Frame-based pricing: 'frame' (using specified FPS, default: 24.0)
        - Clip / Shot / Generation fixed pricing: 'shot', 'clip', 'generation' (using duration_seconds)
        - Credit / Token-based pricing: 'credits', 'tokens' (using cost_per_credit and duration_seconds)
        - String rate parsing: '$0.05/sec', '$3.00/min', '$0.35/5s', '$0.002/frame @ 30fps'

    Args:
        price: Price amount as a float, int, Decimal, or formatted string (e.g. '$0.05/sec').
        unit: Billing unit ('second', 'minute', 'hour', 'day', 'frame', 'shot', 'clip', 'generation', 'credit', 'credits').
              If None and price is a string, the unit is extracted automatically. Defaults to 'second'.
        duration_seconds: Duration in seconds for shot/clip/generation-based rates.
        fps: Frames per second for frame-based pricing (default: 24.0).
        cost_per_credit: Dollar cost per credit/token for credit-based pricing models.
        round_digits: Number of decimal places for deterministic rounding. If None, no rounding is performed.

    Returns:
        float: Normalized cost in dollars per second ($/sec).

    Raises:
        ValueError: If price is negative, duration <= 0, fps <= 0, or unit is unrecognized.
        TypeError: If an invalid argument type is provided.
    """
    fps_dec = _to_decimal(fps)
    if fps_dec <= Decimal("0"):
        raise ValueError(f"fps must be strictly positive (> 0), got: {fps}")

    dur_dec = _to_decimal(duration_seconds) if duration_seconds is not None else None
    if dur_dec is not None and dur_dec <= Decimal("0"):
        raise ValueError(f"duration_seconds must be strictly positive (> 0), got: {duration_seconds}")

    # Parse string rates if string is provided
    inferred_unit = None
    if isinstance(price, str):
        parsed_amt, parsed_unit, parsed_dur, parsed_fps = _parse_price_string(price)
        price_dec = parsed_amt
        inferred_unit = parsed_unit
        if parsed_dur is not None and dur_dec is None:
            dur_dec = parsed_dur
        if parsed_fps is not None:
            fps_dec = parsed_fps
    else:
        price_dec = _to_decimal(price)

    if price_dec < Decimal("0"):
        raise ValueError(f"Price cannot be negative, got: {price}")

    # Determine effective unit
    eff_unit = (unit or inferred_unit or "second").lower().strip()

    # Calculate dollars per second deterministically using Decimal
    if eff_unit in TIME_UNIT_SECONDS:
        seconds_in_unit = TIME_UNIT_SECONDS[eff_unit]
        dollars_per_sec = price_dec / seconds_in_unit

    elif eff_unit in ("frame", "frames", "per_frame"):
        # Price is per frame: dollars_per_sec = price_per_frame * fps
        dollars_per_sec = price_dec * fps_dec

    elif eff_unit in ("shot", "clip", "generation", "per_shot", "per_generation"):
        # Price is per whole shot: dollars_per_sec = price_per_shot / duration_seconds
        if dur_dec is None:
            raise ValueError(f"duration_seconds is required for shot/generation-based unit '{eff_unit}'")
        dollars_per_sec = price_dec / dur_dec

    elif eff_unit in ("credit_per_second", "credits_per_second", "credits/sec", "credits/second", "credit/sec", "credit/second"):
        if cost_per_credit is None:
            raise ValueError(f"cost_per_credit is required when price is denominated in '{eff_unit}'")
        credit_cost_dec = _to_decimal(cost_per_credit)
        if credit_cost_dec < Decimal("0"):
            raise ValueError(f"cost_per_credit cannot be negative, got: {cost_per_credit}")
        dollars_per_sec = price_dec * credit_cost_dec

    elif eff_unit in ("credit", "credits", "token", "tokens", "per_credit", "credits/shot", "credits/generation", "credits/clip"):
        # Price is in credits for a clip/shot: requires cost_per_credit and duration_seconds (or defaults to per second)
        if cost_per_credit is None:
            raise ValueError(f"cost_per_credit is required when price is denominated in '{eff_unit}'")
        credit_cost_dec = _to_decimal(cost_per_credit)
        if credit_cost_dec < Decimal("0"):
            raise ValueError(f"cost_per_credit cannot be negative, got: {cost_per_credit}")

        total_dollar_cost = price_dec * credit_cost_dec
        if dur_dec is not None:
            dollars_per_sec = total_dollar_cost / dur_dec
        else:
            # If no duration given, treat credits as per-second rate
            dollars_per_sec = total_dollar_cost

    else:
        raise ValueError(
            f"Unrecognized pricing unit: '{eff_unit}'. Supported units: "
            f"{list(TIME_UNIT_SECONDS.keys()) + ['frame', 'shot', 'clip', 'generation', 'credits', 'tokens']}"
        )

    # Deterministic rounding if requested
    if round_digits is not None:
        quantize_exp = Decimal("10") ** -round_digits
        dollars_per_sec = dollars_per_sec.quantize(quantize_exp, rounding=ROUND_HALF_UP)

    return float(dollars_per_sec)


def get_normalized_pricing_breakdown(
    price: Union[float, int, str, Decimal],
    unit: Optional[str] = None,
    duration_seconds: Optional[Union[float, int, Decimal]] = None,
    fps: Union[float, int, Decimal] = 24.0,
    cost_per_credit: Optional[Union[float, int, Decimal]] = None,
) -> NormalizedPrice:
    """Returns a full NormalizedPrice structure with per-second, per-minute, and per-hour rates."""
    d_per_sec = normalize_price_to_dollars_per_second(
        price=price,
        unit=unit,
        duration_seconds=duration_seconds,
        fps=fps,
        cost_per_credit=cost_per_credit,
        round_digits=8,
    )
    d_per_sec_dec = Decimal(str(d_per_sec))
    d_per_min = float((d_per_sec_dec * Decimal("60")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
    d_per_hr = float((d_per_sec_dec * Decimal("3600")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))

    return NormalizedPrice(
        dollars_per_second=d_per_sec,
        dollars_per_minute=d_per_min,
        dollars_per_hour=d_per_hr,
        input_price=str(price),
        unit=unit or "auto",
        duration_seconds=float(duration_seconds) if duration_seconds is not None else None,
        fps=float(fps) if fps is not None else None,
    )
