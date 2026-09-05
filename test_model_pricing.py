"""Test suite for Veo-style per-second, credit-based, and fixed-generation pricing.

Restricted to the 7 approved video models:
1. Veo
2. Kling
3. Runway
4. Seedance
5. Luma
6. Hailuo
7. MiniMax-H3
"""

import pytest
from cost_optimizer_agent.models_pricing import (
    MODEL_PRICING_REGISTRY,
    get_model_pricing,
)
from cost_optimizer_agent.pricing import normalize_price_to_dollars_per_second

APPROVED_MODELS = ["Veo", "Kling", "Runway", "Seedance", "Luma", "Hailuo", "MiniMax-H3"]


# =========================================================================
# 1. Veo-Style Per-Second Pricing Tests
# =========================================================================

class TestVeoPerSecondPricing:
    """Tests for direct per-second billing models (Google Veo)."""

    def test_veo_standard_per_second(self):
        """Veo Standard is billed directly at $0.15 per second of output."""
        veo = get_model_pricing("Veo")
        rate_per_sec = veo.normalize()
        assert rate_per_sec == 0.15

        # 5-second shot total cost
        total_5s = rate_per_sec * 5.0
        assert round(total_5s, 2) == 0.75

        # 8-second shot total cost
        total_8s = rate_per_sec * 8.0
        assert round(total_8s, 2) == 1.20

    def test_veo_fast_mode_per_second(self):
        """Veo Fast mode is billed at $0.08 per second."""
        veo_fast = get_model_pricing("Veo-Fast")
        rate_per_sec = veo_fast.normalize()
        assert rate_per_sec == 0.08

        # 5-second shot
        assert round(rate_per_sec * 5.0, 2) == 0.40

    def test_veo_string_rate_parsing(self):
        """Tests parsing formatted string prices for Veo."""
        assert normalize_price_to_dollars_per_second("$0.15/sec") == 0.15
        assert normalize_price_to_dollars_per_second("$0.08 / second") == 0.08

    def test_veo_time_projections(self):
        """Validates per-minute and per-hour breakdowns for Veo."""
        veo = get_model_pricing("Veo")
        breakdown = veo.get_breakdown()
        assert breakdown.dollars_per_second == 0.15
        assert breakdown.dollars_per_minute == 9.00     # 0.15 * 60
        assert breakdown.dollars_per_hour == 540.00     # 0.15 * 3600


# =========================================================================
# 2. Credit-Based Pricing Tests (Kling, Runway, Hailuo)
# =========================================================================

class TestCreditBasedPricing:
    """Tests for token / credit-based video models."""

    def test_kling_standard_credit_pricing(self):
        """Kling Standard: 35 credits per 5s video @ $0.01/credit -> $0.07/sec."""
        kling = get_model_pricing("Kling")
        rate_per_sec = kling.normalize()
        # 35 * $0.01 = $0.35 / 5s = $0.07/sec
        assert rate_per_sec == 0.07

    def test_kling_pro_credit_pricing(self):
        """Kling Pro: 70 credits per 10s video @ $0.01/credit -> $0.07/sec."""
        kling_pro = get_model_pricing("Kling-Pro")
        rate_per_sec = kling_pro.normalize()
        # 70 * $0.01 = $0.70 / 10s = $0.07/sec
        assert rate_per_sec == 0.07

    def test_runway_gen3_turbo_credit_pricing(self):
        """Runway Gen-3 Alpha Turbo: 5 credits per second @ $0.01/credit -> $0.05/sec."""
        runway_turbo = get_model_pricing("Runway-Gen3-Turbo")
        rate_per_sec = runway_turbo.normalize()
        # 5 * $0.01 = $0.05/sec
        assert rate_per_sec == 0.05

        # 5-second generation: 25 credits = $0.25
        assert round(rate_per_sec * 5.0, 2) == 0.25

    def test_runway_gen3_alpha_credit_pricing(self):
        """Runway Gen-3 Alpha: 10 credits per second @ $0.01/credit -> $0.10/sec."""
        runway_alpha = get_model_pricing("Runway-Gen3-Alpha")
        rate_per_sec = runway_alpha.normalize()
        # 10 * $0.01 = $0.10/sec
        assert rate_per_sec == 0.10

        # 10-second generation: 100 credits = $1.00
        assert round(rate_per_sec * 10.0, 2) == 1.00

    def test_hailuo_credit_pricing(self):
        """Hailuo AI Credits: 24 credits per 6s generation @ $0.01/credit -> $0.04/sec."""
        hailuo_cr = get_model_pricing("Hailuo-Credits")
        rate_per_sec = hailuo_cr.normalize()
        # 24 * $0.01 = $0.24 / 6s = $0.04/sec
        assert rate_per_sec == 0.04

    def test_credit_rate_volume_discount(self):
        """Tests credit normalization with volume discount rate ($0.008 per credit)."""
        rate = normalize_price_to_dollars_per_second(
            price=35,
            unit="credits",
            cost_per_credit=0.008,
            duration_seconds=5.0,
        )
        # 35 * $0.008 = $0.28 / 5s = $0.056/sec
        assert rate == 0.056


# =========================================================================
# 3. Fixed-Generation Pricing Tests (Seedance, Luma, Hailuo, MiniMax-H3)
# =========================================================================

class TestFixedGenerationPricing:
    """Tests for fixed price per generation/clip models."""

    def test_seedance_fixed_pricing(self):
        """Seedance: $0.30 per 5s generation -> $0.06/sec."""
        seedance = get_model_pricing("Seedance")
        rate_per_sec = seedance.normalize()
        # $0.30 / 5s = $0.06/sec
        assert rate_per_sec == 0.06

    def test_luma_dream_machine_fixed_pricing(self):
        """Luma Dream Machine: $0.40 per 5s generation -> $0.08/sec."""
        luma = get_model_pricing("Luma")
        rate_per_sec = luma.normalize()
        # $0.40 / 5s = $0.08/sec
        assert rate_per_sec == 0.08

    def test_hailuo_fixed_pricing(self):
        """Hailuo AI: $0.24 per 6s generation -> $0.04/sec."""
        hailuo = get_model_pricing("Hailuo")
        rate_per_sec = hailuo.normalize()
        # $0.24 / 6s = $0.04/sec
        assert rate_per_sec == 0.04

    def test_minimax_h3_fixed_pricing(self):
        """MiniMax-H3: $0.25 per 5s video generation -> $0.05/sec."""
        minimax = get_model_pricing("MiniMax-H3")
        rate_per_sec = minimax.normalize()
        # $0.25 / 5s = $0.05/sec
        assert rate_per_sec == 0.05

    def test_fixed_generation_custom_durations(self):
        """Tests fixed generation with custom clip lengths."""
        # Seedance 10-second extension: $0.30 / 10s = $0.03/sec
        seedance = get_model_pricing("Seedance")
        assert seedance.normalize(duration_seconds=10.0) == 0.03

        # Luma 4-second clip: $0.40 / 4s = $0.10/sec
        luma = get_model_pricing("Luma")
        assert luma.normalize(duration_seconds=4.0) == 0.10


# =========================================================================
# 4. Comparative Model Ranking & Registry Constraint Tests
# =========================================================================

class TestComparativeModelRanking:
    """Verifies that all 7 approved models are correctly registered and ranked."""

    def test_all_seven_model_families_present(self):
        """Ensures all 7 required models exist in registry."""
        for model in APPROVED_MODELS:
            matching_keys = [k for k in MODEL_PRICING_REGISTRY if k.startswith(model)]
            assert len(matching_keys) > 0, f"Model family '{model}' missing from registry"

    def test_unregistered_model_rejection(self):
        """Ensures pricing queries for models outside the approved 7 are rejected."""
        with pytest.raises(ValueError, match="Unknown model 'Sora'"):
            get_model_pricing("Sora")

        with pytest.raises(ValueError, match="Unknown model 'Pika'"):
            get_model_pricing("Pika")

    def test_dollars_per_second_cost_ranking(self):
        """Validates relative cost efficiency across all 7 video models for a 5s shot."""
        rates = {
            "Hailuo": get_model_pricing("Hailuo").normalize(),
            "Runway-Turbo": get_model_pricing("Runway-Gen3-Turbo").normalize(),
            "MiniMax-H3": get_model_pricing("MiniMax-H3").normalize(),
            "Seedance": get_model_pricing("Seedance").normalize(),
            "Kling": get_model_pricing("Kling").normalize(),
            "Luma": get_model_pricing("Luma").normalize(),
            "Runway-Alpha": get_model_pricing("Runway-Gen3-Alpha").normalize(),
            "Veo": get_model_pricing("Veo").normalize(),
        }

        # Assert specific deterministic rates
        assert rates["Hailuo"] == 0.04
        assert rates["Runway-Turbo"] == 0.05
        assert rates["MiniMax-H3"] == 0.05
        assert rates["Seedance"] == 0.06
        assert rates["Kling"] == 0.07
        assert rates["Luma"] == 0.08
        assert rates["Runway-Alpha"] == 0.10
        assert rates["Veo"] == 0.15

        # Verify sorted order (cheapest to most expensive $/sec)
        sorted_models = sorted(rates.items(), key=lambda x: x[1])
        model_order = [m[0] for m in sorted_models]
        expected_order = [
            "Hailuo",
            "Runway-Turbo",
            "MiniMax-H3",
            "Seedance",
            "Kling",
            "Luma",
            "Runway-Alpha",
            "Veo",
        ]
        # Hailuo is cheapest, Veo is highest tier
        assert model_order[0] == "Hailuo"
        assert model_order[-1] == "Veo"
        assert rates["Hailuo"] < rates["Seedance"] < rates["Veo"]
