"""Model pricing, capabilities, limitations, and availability for the 7 approved video models.

1. Veo (Google DeepMind)
2. Kling (Kuaishou)
3. Runway (RunwayML Gen-3)
4. Seedance (ByteDance)
5. Luma (Luma Dream Machine)
6. Hailuo (MiniMax)
7. MiniMax-H3 (MiniMax)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Union
from cost_optimizer_agent.pricing import (
    NormalizedPrice,
    get_normalized_pricing_breakdown,
    normalize_price_to_dollars_per_second,
)

PricingType = Literal["per_second", "credit_based", "fixed_generation"]


@dataclass(frozen=True)
class ModelCapabilityProfile:
    """Detailed profile of capabilities, limitations, and availability for a video model."""
    model_name: str
    provider: str
    pricing_type: PricingType
    base_price: Union[float, int, str]
    unit: str
    default_duration_seconds: float
    cost_per_credit: Optional[float] = None
    fps: float = 24.0
    max_duration_seconds: float = 10.0
    max_resolution: str = "1080p"
    availability: str = "General Availability"  # "General Availability", "Public API", "Vertex AI Enterprise"
    supported_capabilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    quality_score: float = 8.5  # 1.0 - 10.0 scale
    description: str = ""

    def normalize(
        self,
        duration_seconds: Optional[float] = None,
        round_digits: Optional[int] = 6,
    ) -> float:
        """Calculates normalized dollars per second for this model specification."""
        dur = duration_seconds if duration_seconds is not None else self.default_duration_seconds
        return normalize_price_to_dollars_per_second(
            price=self.base_price,
            unit=self.unit,
            duration_seconds=dur,
            fps=self.fps,
            cost_per_credit=self.cost_per_credit,
            round_digits=round_digits,
        )

    def get_breakdown(self, duration_seconds: Optional[float] = None) -> NormalizedPrice:
        """Returns the full normalized pricing breakdown (per sec, per min, per hour)."""
        dur = duration_seconds if duration_seconds is not None else self.default_duration_seconds
        return get_normalized_pricing_breakdown(
            price=self.base_price,
            unit=self.unit,
            duration_seconds=dur,
            fps=self.fps,
            cost_per_credit=self.cost_per_credit,
        )

    def check_suitability(self, essential_capabilities: List[str]) -> tuple[bool, List[str]]:
        """Checks if this model meets all essential capabilities.

        Returns:
            tuple[bool, List[str]]: (is_suitable, list_of_missing_capabilities)
        """
        missing = [cap for cap in essential_capabilities if cap not in self.supported_capabilities]
        return (len(missing) == 0, missing)


# Backward compatibility alias
ModelPricingSpec = ModelCapabilityProfile

# Registry of the 7 approved models
MODEL_PRICING_REGISTRY: dict[str, ModelCapabilityProfile] = {
    # 1. Veo (Google DeepMind)
    "Veo": ModelCapabilityProfile(
        model_name="Veo",
        provider="Google DeepMind / Vertex AI",
        pricing_type="per_second",
        base_price=0.15,
        unit="second",
        default_duration_seconds=5.0,
        max_duration_seconds=8.0,
        max_resolution="1080p / 4K Upscaled",
        availability="Vertex AI Enterprise / GA",
        quality_score=9.5,
        supported_capabilities=[
            "high_photorealism",
            "camera_motion_control",
            "high_motion_adherence",
            "complex_physics_simulation",
            "high_frame_consistency",
            "character_anatomy_consistency",
            "prompt_adherence",
        ],
        limitations=[
            "Higher cost tier ($0.15/sec)",
            "Strict safety filter can reject edgy scene prompts",
            "No native character lip-sync audio in standard generation",
        ],
        strengths=[
            "Industry-leading cinematic camera control and visual fidelity",
            "Exceptional complex physics, fluid, and particle simulation",
            "Superior prompt adherence and lighting coherence",
        ],
        description="Google Veo per-second generation pricing ($0.15/sec at 1080p)",
    ),
    "Veo-Fast": ModelCapabilityProfile(
        model_name="Veo-Fast",
        provider="Google DeepMind / Vertex AI",
        pricing_type="per_second",
        base_price=0.08,
        unit="second",
        default_duration_seconds=5.0,
        max_duration_seconds=8.0,
        max_resolution="1080p",
        availability="Vertex AI / Public Preview",
        quality_score=8.7,
        supported_capabilities=[
            "high_photorealism",
            "camera_motion_control",
            "high_motion_adherence",
            "high_frame_consistency",
            "prompt_adherence",
        ],
        limitations=[
            "Reduced physics simulation detail compared to Veo full",
            "Minor motion blur on high-speed movements",
        ],
        strengths=[
            "High speed inference at almost half the cost ($0.08/sec)",
            "Strong cinematic framing",
        ],
        description="Google Veo Fast Mode per-second generation pricing ($0.08/sec)",
    ),

    # 2. Kling (Kuaishou Kling AI)
    "Kling": ModelCapabilityProfile(
        model_name="Kling",
        provider="Kuaishou Kling AI",
        pricing_type="credit_based",
        base_price=35,
        unit="credits",
        default_duration_seconds=5.0,
        cost_per_credit=0.01,
        max_duration_seconds=10.0,
        max_resolution="1080p",
        availability="Public API / Web",
        quality_score=8.9,
        supported_capabilities=[
            "high_photorealism",
            "high_motion_adherence",
            "character_anatomy_consistency",
            "complex_physics_simulation",
            "high_frame_consistency",
        ],
        limitations=[
            "Camera motion paths can drift on complex multi-axis instructions",
            "Queue times can fluctuate during peak hours",
        ],
        strengths=[
            "Outstanding human anatomy, character motion, and facial expressions",
            "Supports long single generation clips up to 10s",
        ],
        description="Kling Standard: 35 credits per 5s generation @ $0.01/credit ($0.07/sec)",
    ),
    "Kling-Pro": ModelCapabilityProfile(
        model_name="Kling-Pro",
        provider="Kuaishou Kling AI",
        pricing_type="credit_based",
        base_price=70,
        unit="credits",
        default_duration_seconds=10.0,
        cost_per_credit=0.01,
        max_duration_seconds=10.0,
        max_resolution="1080p HD",
        availability="Public API / Web",
        quality_score=9.1,
        supported_capabilities=[
            "high_photorealism",
            "high_motion_adherence",
            "character_anatomy_consistency",
            "complex_physics_simulation",
            "high_frame_consistency",
            "camera_motion_control",
        ],
        limitations=[
            "Higher credit consumption (70 credits / 10s)",
            "Fixed clip increments",
        ],
        strengths=[
            "Enhanced prompt comprehension and superior texture detail",
            "Exceptional 10s continuous narrative coherence",
        ],
        description="Kling Pro Mode: 70 credits per 10s generation @ $0.01/credit ($0.07/sec)",
    ),

    # 3. Runway (RunwayML Gen-3)
    "Runway-Gen3-Turbo": ModelCapabilityProfile(
        model_name="Runway-Gen3-Turbo",
        provider="RunwayML",
        pricing_type="credit_based",
        base_price=5,
        unit="credits/sec",
        default_duration_seconds=1.0,
        cost_per_credit=0.01,
        max_duration_seconds=10.0,
        max_resolution="1080p",
        availability="Public API / GA",
        quality_score=8.8,
        supported_capabilities=[
            "high_photorealism",
            "camera_motion_control",
            "high_motion_adherence",
            "high_frame_consistency",
            "complex_physics_simulation",
        ],
        limitations=[
            "Fast motion can exhibit minor artifacting in complex foliage",
            "Requires specific camera prompt syntax for best results",
        ],
        strengths=[
            "Very cost-effective ($0.05/sec) with ultra-fast generation speed",
            "Excellent camera motion presets and temporal consistency",
        ],
        description="Runway Gen-3 Alpha Turbo: 5 credits per second @ $0.01/credit ($0.05/sec)",
    ),
    "Runway-Gen3-Alpha": ModelCapabilityProfile(
        model_name="Runway-Gen3-Alpha",
        provider="RunwayML",
        pricing_type="credit_based",
        base_price=10,
        unit="credits/sec",
        default_duration_seconds=1.0,
        cost_per_credit=0.01,
        max_duration_seconds=10.0,
        max_resolution="1080p / 4K",
        availability="Public API / GA",
        quality_score=9.3,
        supported_capabilities=[
            "high_photorealism",
            "camera_motion_control",
            "high_motion_adherence",
            "character_anatomy_consistency",
            "complex_physics_simulation",
            "high_frame_consistency",
            "prompt_adherence",
        ],
        limitations=[
            "Higher cost tier ($0.10/sec)",
            "Longer queue latency compared to Turbo",
        ],
        strengths=[
            "Hollywood-grade dynamic range, lighting, and cinematic motion fidelity",
            "Precise camera motion and keyframe control",
        ],
        description="Runway Gen-3 Alpha: 10 credits per second @ $0.01/credit ($0.10/sec)",
    ),

    # 4. Seedance (ByteDance Seedance)
    "Seedance": ModelCapabilityProfile(
        model_name="Seedance",
        provider="ByteDance Seedance",
        pricing_type="fixed_generation",
        base_price=0.30,
        unit="generation",
        default_duration_seconds=5.0,
        max_duration_seconds=5.0,
        max_resolution="1080p",
        availability="Public API / Beta",
        quality_score=8.6,
        supported_capabilities=[
            "high_photorealism",
            "high_motion_adherence",
            "character_anatomy_consistency",
            "high_frame_consistency",
        ],
        limitations=[
            "Limited camera motion customization",
            "Fixed 5-second generation limit per call",
        ],
        strengths=[
            "Strong character styling and smooth natural motion",
            "Low fixed cost ($0.30 per 5s shot)",
        ],
        description="Seedance fixed generation: $0.30 per 5s shot ($0.06/sec)",
    ),

    # 5. Luma (Luma Dream Machine)
    "Luma": ModelCapabilityProfile(
        model_name="Luma",
        provider="Luma AI (Dream Machine)",
        pricing_type="fixed_generation",
        base_price=0.40,
        unit="generation",
        default_duration_seconds=5.0,
        max_duration_seconds=5.0,
        max_resolution="1080p / 4K",
        availability="Public API / GA",
        quality_score=8.9,
        supported_capabilities=[
            "high_photorealism",
            "camera_motion_control",
            "camera_motion_control",
            "complex_physics_simulation",
            "high_frame_consistency",
        ],
        limitations=[
            "Fixed $0.40 per 5s shot cost structure",
            "Fast character movements can occasionally morph",
        ],
        strengths=[
            "Spectacular camera moves, sweeps, and environmental scale",
            "Clean visual textures and keyframe extension support",
        ],
        description="Luma Dream Machine fixed generation: $0.40 per 5s clip ($0.08/sec)",
    ),

    # 6. Hailuo (MiniMax Hailuo AI)
    "Hailuo": ModelCapabilityProfile(
        model_name="Hailuo",
        provider="MiniMax Hailuo AI",
        pricing_type="fixed_generation",
        base_price=0.24,
        unit="generation",
        default_duration_seconds=6.0,
        max_duration_seconds=6.0,
        max_resolution="1080p",
        availability="Public API / GA",
        quality_score=8.7,
        supported_capabilities=[
            "high_photorealism",
            "character_anatomy_consistency",
            "high_frame_consistency",
            "complex_physics_simulation",
        ],
        limitations=[
            "Lacks fine-grained programmatic camera path controls",
            "Fixed 6-second clips",
        ],
        strengths=[
            "Most cost-effective model in catalog ($0.04/sec)",
            "Stunning realistic human faces, skin tones, and organic motion",
        ],
        description="Hailuo AI fixed generation: $0.24 per 6s shot ($0.04/sec)",
    ),
    "Hailuo-Credits": ModelCapabilityProfile(
        model_name="Hailuo-Credits",
        provider="MiniMax Hailuo AI",
        pricing_type="credit_based",
        base_price=24,
        unit="credits",
        default_duration_seconds=6.0,
        cost_per_credit=0.01,
        max_duration_seconds=6.0,
        max_resolution="1080p",
        availability="Public API / GA",
        quality_score=8.7,
        supported_capabilities=[
            "high_photorealism",
            "character_anatomy_consistency",
            "high_frame_consistency",
            "complex_physics_simulation",
        ],
        limitations=[
            "No advanced camera trajectory steering",
        ],
        strengths=[
            "Ultra-low credit cost (24 credits / 6s = $0.04/sec)",
            "Rich character dynamics",
        ],
        description="Hailuo AI credits: 24 credits per 6s generation @ $0.01/credit ($0.04/sec)",
    ),

    # 7. MiniMax-H3 (MiniMax Video-01 / H3)
    "MiniMax-H3": ModelCapabilityProfile(
        model_name="MiniMax-H3",
        provider="MiniMax",
        pricing_type="fixed_generation",
        base_price=0.25,
        unit="generation",
        default_duration_seconds=5.0,
        max_duration_seconds=6.0,
        max_resolution="1080p",
        availability="Public API / GA",
        quality_score=8.8,
        supported_capabilities=[
            "high_photorealism",
            "character_anatomy_consistency",
            "complex_physics_simulation",
            "high_frame_consistency",
            "prompt_adherence",
        ],
        limitations=[
            "Camera movement is determined primarily from text prompt without direct velocity curve controls",
        ],
        strengths=[
            "Remarkable price-to-performance ratio ($0.05/sec)",
            "Excellent prompt adherence and physics interaction",
        ],
        description="MiniMax-H3 fixed generation: $0.25 per 5s video ($0.05/sec)",
    ),
}


def get_model_pricing(model_name: str) -> ModelCapabilityProfile:
    """Retrieves capability and pricing specification for one of the approved models."""
    if model_name not in MODEL_PRICING_REGISTRY:
        allowed = list(MODEL_PRICING_REGISTRY.keys())
        raise ValueError(f"Unknown model '{model_name}'. Allowed models: {allowed}")
    return MODEL_PRICING_REGISTRY[model_name]
