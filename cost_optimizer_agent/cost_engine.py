"""Cost Engine for normalizing pricing, eliminating unsuitable models, calculating costs, and ranking alternatives."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
from cost_optimizer_agent.models_pricing import MODEL_PRICING_REGISTRY, ModelCapabilityProfile


@dataclass
class EvaluatedModelResult:
    """Evaluation output for a single AI video model against shot requirements."""
    rank: Optional[int]
    model_name: str
    provider: str
    pricing_type: str
    base_price_display: str
    rate_per_second_usd: float
    single_shot_cost_usd: float
    total_estimated_cost_usd: float
    quality_score: float
    is_viable: bool
    elimination_reason: Optional[str] = None
    missing_capabilities: List[str] = field(default_factory=list)
    tradeoff_summary: str = ""
    strengths: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    availability: str = "General Availability"


@dataclass
class CostEngineEvaluation:
    """Full evaluation result produced by the Cost Engine."""
    shot_description: str
    duration_seconds: float
    rerun_multiplier: float
    essential_capabilities: List[str]
    viable_models: List[EvaluatedModelResult]
    eliminated_models: List[EvaluatedModelResult]
    recommended_model: Optional[EvaluatedModelResult]
    lowest_cost_viable_usd: float
    highest_tier_cost_usd: float
    projected_savings_usd: float
    tradeoff_explanation: str
    stock_replacement_potential: str


def run_cost_engine(
    shot_requirements: Dict[str, Any],
    duration_seconds: float = 5.0,
    rerun_multiplier: float = 2.2,
    override_essential_capabilities: Optional[List[str]] = None,
) -> CostEngineEvaluation:
    """Executes Steps 4-9 of the Cost Optimizer Agent architecture.

    4. Normalize pricing and capabilities.
    5. Eliminate unsuitable models.
    6. Calculate estimated cost per viable result.
    7. Rank the alternatives.
    8. Recommend the lowest-cost viable approach.
    9. Explain the tradeoff.
    """
    essential_caps = (
        override_essential_capabilities
        if override_essential_capabilities is not None
        else shot_requirements.get("essential_capabilities", [])
    )

    shot_desc = shot_requirements.get("shot_description", "")
    all_evaluated: List[EvaluatedModelResult] = []

    for spec in MODEL_PRICING_REGISTRY.values():
        # Step 4: Normalize pricing
        rate_per_sec = spec.normalize(duration_seconds=duration_seconds)
        single_cost = round(rate_per_sec * duration_seconds, 3)
        total_cost = round(single_cost * rerun_multiplier, 2)

        if spec.pricing_type == "credit_based":
            if "sec" in spec.unit:
                base_display = f"{spec.base_price} cr/sec (@ ${spec.cost_per_credit}/cr)"
            else:
                base_display = f"{spec.base_price} cr / {int(spec.default_duration_seconds)}s (@ ${spec.cost_per_credit}/cr)"
        elif spec.pricing_type == "fixed_generation":
            base_display = f"${spec.base_price:.2f} / {int(spec.default_duration_seconds)}s"
        else:
            base_display = f"${spec.base_price:.2f} / sec"

        # Step 5: Eliminate unsuitable models
        is_suitable, missing_caps = spec.check_suitability(essential_caps)
        elim_reason = None
        if not is_suitable:
            readable_missing = [c.replace("_", " ").title() for c in missing_caps]
            elim_reason = f"Lacks essential capability: {', '.join(readable_missing)}"

        # Step 9: Tradeoff formulation
        tradeoff = f"{spec.strengths[0]} | Limitation: {spec.limitations[0]}"

        all_evaluated.append(
            EvaluatedModelResult(
                rank=None,
                model_name=spec.model_name,
                provider=spec.provider,
                pricing_type=spec.pricing_type.replace("_", " ").title(),
                base_price_display=base_display,
                rate_per_second_usd=round(rate_per_sec, 4),
                single_shot_cost_usd=single_cost,
                total_estimated_cost_usd=total_cost,
                quality_score=spec.quality_score,
                is_viable=is_suitable,
                elimination_reason=elim_reason,
                missing_capabilities=missing_caps,
                tradeoff_summary=tradeoff,
                strengths=spec.strengths,
                limitations=spec.limitations,
                availability=spec.availability,
            )
        )

    # Step 6 & 7: Separate viable vs eliminated and rank viable models by cost
    viable = [m for m in all_evaluated if m.is_viable]
    eliminated = [m for m in all_evaluated if not m.is_viable]

    # If all models were eliminated by overly strict filters, fallback to quality rank
    if not viable:
        viable = all_evaluated[:]
        eliminated = []

    viable.sort(key=lambda x: (x.rate_per_second_usd, -x.quality_score))
    for idx, item in enumerate(viable, 1):
        item.rank = idx

    # Step 8: Recommend lowest-cost viable approach
    recommended = viable[0]
    highest = max(all_evaluated, key=lambda x: x.total_estimated_cost_usd)
    lowest_cost = recommended.total_estimated_cost_usd
    savings = round(highest.total_estimated_cost_usd - lowest_cost, 2)

    # Step 9: Tradeoff explanation
    if recommended.model_name == highest.model_name:
        tradeoff_exp = f"Model '{recommended.model_name}' is the top viable choice with zero capability compromises."
    else:
        tradeoff_exp = (
            f"Choosing '{recommended.model_name}' (${lowest_cost:.2f}) over highest-tier '{highest.model_name}' (${highest.total_estimated_cost_usd:.2f}) "
            f"saves ${savings:.2f} ({int((savings/highest.total_estimated_cost_usd)*100)}% budget reduction). "
            f"Tradeoff: You gain maximum cost-efficiency, but accept {recommended.limitations[0].lower()}."
        )

    is_landscape_or_broll = shot_requirements.get("subject_type") in ("landscape_environment", "macro_texture")
    stock_potential = "High (90%+ match likelihood for stock b-roll replacement)" if is_landscape_or_broll else "Moderate/Low (Requires generative performance)"

    return CostEngineEvaluation(
        shot_description=shot_desc,
        duration_seconds=duration_seconds,
        rerun_multiplier=rerun_multiplier,
        essential_capabilities=essential_caps,
        viable_models=viable,
        eliminated_models=eliminated,
        recommended_model=recommended,
        lowest_cost_viable_usd=lowest_cost,
        highest_tier_cost_usd=highest.total_estimated_cost_usd,
        projected_savings_usd=savings,
        tradeoff_explanation=tradeoff_exp,
        stock_replacement_potential=stock_potential,
    )
