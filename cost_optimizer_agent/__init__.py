"""CostOptimizerAgent package using Google ADK."""

from cost_optimizer_agent.agent import (
    cost_optimizer_agent,
    create_cost_optimizer_agent,
    root_agent,
)
from cost_optimizer_agent.cost_engine import (
    CostEngineEvaluation,
    EvaluatedModelResult,
    run_cost_engine,
)
from cost_optimizer_agent.models_pricing import (
    MODEL_PRICING_REGISTRY,
    ModelCapabilityProfile,
    ModelPricingSpec,
    get_model_pricing,
)
from cost_optimizer_agent.parallel_search_tool import search_video_models_and_pricing
from cost_optimizer_agent.pricing import (
    get_normalized_pricing_breakdown,
    normalize_price_to_dollars_per_second,
)
from cost_optimizer_agent.shot_analysis_tool import (
    TechnicalShotRequirements,
    analyze_shot_requirements,
)
from cost_optimizer_agent.tools import parallel_search_video_footage

CostOptimizerAgent = root_agent

__all__ = [
    "CostOptimizerAgent",
    "root_agent",
    "cost_optimizer_agent",
    "create_cost_optimizer_agent",
    "analyze_shot_requirements",
    "search_video_models_and_pricing",
    "parallel_search_video_footage",
    "normalize_price_to_dollars_per_second",
    "get_normalized_pricing_breakdown",
    "run_cost_engine",
    "CostEngineEvaluation",
    "EvaluatedModelResult",
    "MODEL_PRICING_REGISTRY",
    "ModelCapabilityProfile",
    "ModelPricingSpec",
    "get_model_pricing",
    "TechnicalShotRequirements",
]
