"""Gemini service integration for CostOptimizerAgent."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types

from cost_optimizer_agent.config import DEFAULT_MODEL

logger = logging.getLogger(__name__)


def run_gemini_shot_reasoning(
    shot_description: str,
    duration_seconds: float,
    rerun_multiplier: float,
    viable_models_summary: List[Dict[str, Any]],
    eliminated_models_summary: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model_name: str = DEFAULT_MODEL,
) -> Dict[str, Any]:
    """Invokes Google Gemini to generate production reasoning, tradeoff analysis, and recommendations.

    Args:
        shot_description: The filmmaker's scene prompt.
        duration_seconds: Target shot duration in seconds.
        rerun_multiplier: Expected generation trial/error multiplier.
        viable_models_summary: Data on viable models.
        eliminated_models_summary: Data on eliminated models.
        api_key: Optional Gemini API key. If not passed, checks os.environ.
        model_name: Gemini model name (default: gemini-2.5-flash).

    Returns:
        Dict with Gemini's detailed reasoning, tradeoff breakdown, and advice.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return {
            "used_gemini": False,
            "message": "GEMINI_API_KEY not configured. Set GEMINI_API_KEY in .env or the UI settings to enable live Gemini LLM reasoning.",
            "reasoning": None,
        }

    client = genai.Client(api_key=key)

    candidate_models = [model_name, "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-3-flash-preview"]
    # De-duplicate while preserving order
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

    last_error = None
    prompt = f"""You are the CostOptimizerAgent, an expert AI video production cost optimizer.

Analyze this desired video shot and evaluate the ranked video models:
- Desired Shot: "{shot_description}"
- Planned Duration: {duration_seconds} seconds
- Rerun Iteration Multiplier: {rerun_multiplier}x

Viable Models (calculated from lowest to highest cost):
{json.dumps(viable_models_summary, indent=2)}

Eliminated Models (unsuitable due to capability mismatch):
{json.dumps(eliminated_models_summary, indent=2)}

Please provide a concise, expert analysis formatted with the following markdown sections:
1. **🎬 Shot Complexity & Essential Capabilities**: Break down what makes this shot technically challenging (motion, physics, camera, lighting).
2. **⚖️ Tradeoff Explanation**: Explain the concrete tradeoffs between the lowest-cost viable model and the higher-tier options (e.g. prompt fidelity, render latency, camera control precision, artifact risk).
3. **🚀 Production Recommendation**: Give specific, actionable advice for a filmmaker on how to execute this shot with maximum budget efficiency.
"""

    for target_model in models_to_try:
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7),
            )
            if response.text:
                return {
                    "used_gemini": True,
                    "model_used": target_model,
                    "reasoning": response.text.strip(),
                }
        except Exception as exc:
            last_error = exc
            logger.warning("Gemini model %s failed (%s), trying fallback...", target_model, exc)

    logger.exception("All candidate Gemini models failed: %s", last_error)
    return {
        "used_gemini": False,
        "error": str(last_error),
        "reasoning": None,
    }
