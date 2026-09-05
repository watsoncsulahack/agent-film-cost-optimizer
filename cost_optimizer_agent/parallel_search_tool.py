"""Parallel Search API tool for searching video generation providers, live pricing, capabilities, limitations, and availability."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional
import requests
from cost_optimizer_agent.config import PARALLEL_API_KEY, PARALLEL_API_URL
from cost_optimizer_agent.models_pricing import MODEL_PRICING_REGISTRY

logger = logging.getLogger(__name__)


def search_video_models_and_pricing(
    query: str,
    target_models: Optional[List[str]] = None,
    mode: str = "turbo",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Queries the Parallel Search API to retrieve current video-generation model information.

    Retrieves current data on:
    - Pricing (per-second, credit-based, fixed-generation)
    - Capabilities & strengths (motion fidelity, photorealism, camera controls)
    - Limitations & known issues
    - Availability & API status

    Args:
        query: Specific search prompt (e.g., 'Google Veo Vertex AI pricing capabilities limitations 2026').
        target_models: Optional list of model names to filter information for.
        mode: Parallel search mode ('turbo', 'basic', 'advanced').
        api_key: Optional Parallel API key.

    Returns:
        Dict containing search results, model intelligence, and source URLs.
    """
    key = (api_key if api_key is not None else os.environ.get("PARALLEL_API_KEY", "")).strip()
    models_to_check = target_models if target_models else list(MODEL_PRICING_REGISTRY.keys())

    objective = f"Retrieve latest pricing, capabilities, limitations, and availability for AI video models: {', '.join(models_to_check)}. Context: {query}"
    search_queries = [
        f"{m} AI video generation API pricing capabilities limitations"
        for m in models_to_check[:3]
    ]

    if not key:
        raise ValueError(
            "PARALLEL_API_KEY is strictly required. Please set PARALLEL_API_KEY in your environment, .env file, or pass it in the request."
        )

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json",
        "User-Agent": "Google-ADK-CostOptimizerAgent/2.0",
    }
    payload = {
        "objective": objective,
        "search_queries": search_queries,
        "mode": mode,
    }

    try:
        response = requests.post(PARALLEL_API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            raw_res = data.get("results", [])
            formatted_res = []
            for item in raw_res:
                excerpts = item.get("excerpts", [])
                excerpt_str = "\n".join(excerpts) if isinstance(excerpts, list) else str(excerpts)
                formatted_res.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "excerpts": excerpt_str,
                })
            return {
                "status": "live_success",
                "source": "Parallel Search API (Live)",
                "objective": objective,
                "queries_used": search_queries,
                "raw_results": formatted_res,
            }
        else:
            return {
                "status": "api_error",
                "status_code": response.status_code,
                "error": response.text,
            }
    except Exception as exc:
        return {
            "status": "network_error",
            "message": str(exc),
        }
