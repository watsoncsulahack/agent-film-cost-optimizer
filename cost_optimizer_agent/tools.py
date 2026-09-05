"""Tools for CostOptimizerAgent using the Parallel Search API."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional
import requests
from cost_optimizer_agent.config import (
    AVG_RERUN_MULTIPLIER,
    DEFAULT_SHOT_DURATION_SEC,
    ESTIMATED_AI_GEN_COST_PER_SEC,
    PARALLEL_API_KEY,
    PARALLEL_API_URL,
)
from cost_optimizer_agent.pricing import normalize_price_to_dollars_per_second

logger = logging.getLogger(__name__)


def _build_search_queries(shot_description: str) -> List[str]:
    """Generates keyword queries optimized for stock footage and video asset indexing."""
    cleaned = shot_description.strip().rstrip(".")
    return [
        f"{cleaned} 4k stock footage b-roll",
        f"{cleaned} royalty free video clip",
        f"{cleaned} cinematic video stock",
    ]


def parallel_search_video_footage(
    shot_description: str,
    search_objective: Optional[str] = None,
    search_queries: Optional[List[str]] = None,
    mode: str = "turbo",
    max_results: int = 5,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Queries the Parallel Search API to find stock video footage and visual assets for a shot description.

    This tool enables the CostOptimizerAgent to discover existing reusable video footage,
    open-source clips, and b-roll alternatives to minimize expensive AI video generation compute.

    Args:
        shot_description: Detailed description of the video shot or scene (e.g., 'Aerial drone shot of city skyline at night with bokeh traffic').
        search_objective: Optional specific research objective for Parallel API. If omitted, a tailored prompt is generated.
        search_queries: Optional list of keyword search queries. If omitted, queries are automatically generated.
        mode: Parallel search mode ('turbo', 'basic', 'advanced'). Defaults to 'turbo'.
        max_results: Maximum number of video search results to retrieve (default: 5).
        api_key: Optional Parallel API key.

    Returns:
        A dictionary containing the search results, source URLs, excerpts, and cost-saving opportunities.
    """
    key = api_key or os.environ.get("PARALLEL_API_KEY", PARALLEL_API_KEY).strip()

    objective = (
        search_objective
        if search_objective
        else f"Find high-quality stock video footage, royalty-free B-roll clips, and video assets matching: {shot_description}"
    )

    queries = search_queries if search_queries else _build_search_queries(shot_description)

    payload = {
        "objective": objective,
        "search_queries": queries[:3],
        "mode": mode,
    }

    if not key:
        logger.info("PARALLEL_API_KEY not configured. Returning simulated footage discovery data.")
        return {
            "status": "simulated_success",
            "message": "PARALLEL_API_KEY environment variable is not set. Providing sample discovery results for demonstration.",
            "shot_description": shot_description,
            "objective": objective,
            "queries_used": queries,
            "results": [
                {
                    "title": f"4K Stock Footage: {shot_description[:45]}",
                    "url": "https://www.pexels.com/search/videos/" + "+".join(shot_description.split()[:3]),
                    "source": "Pexels Video (CC0 / Free Commercial)",
                    "license_type": "Royalty-Free Commercial",
                    "resolution": "3840x2160 (4K)",
                    "excerpts": f"High quality cinematic footage matching '{shot_description}'. Clean camera movement, neutral color profile.",
                    "estimated_stock_cost_usd": 0.0,
                    "replacement_feasibility": "High",
                },
                {
                    "title": f"Cinematic B-Roll Clip - {shot_description[:35]}",
                    "url": "https://pixabay.com/videos/search/" + "+".join(shot_description.split()[:2]),
                    "source": "Pixabay Video Archive",
                    "license_type": "Free for Commercial Use",
                    "resolution": "1080p / 4K UHD",
                    "excerpts": f"B-roll clip capturing scenes of {shot_description}. 60fps available for slow motion.",
                    "estimated_stock_cost_usd": 0.0,
                    "replacement_feasibility": "High",
                },
                {
                    "title": f"Studio Production Plate: {shot_description[:40]}",
                    "url": "https://storyblocks.com/video/search/" + "+".join(shot_description.split()[:3]),
                    "source": "Storyblocks Video",
                    "license_type": "Subscription Unlimited",
                    "resolution": "4K ProRes 422",
                    "excerpts": f"Professional production plate for {shot_description}. Ideal for VFX background plates and timeline insertions.",
                    "estimated_stock_cost_usd": 0.15,
                    "replacement_feasibility": "Moderate to High",
                },
            ],
            "cost_analysis": {
                "estimated_ai_gen_cost_per_sec_usd": normalize_price_to_dollars_per_second(ESTIMATED_AI_GEN_COST_PER_SEC, unit="second"),
                "estimated_ai_gen_cost_total_usd": round(normalize_price_to_dollars_per_second(ESTIMATED_AI_GEN_COST_PER_SEC, unit="second") * DEFAULT_SHOT_DURATION_SEC * AVG_RERUN_MULTIPLIER, 2),
                "stock_cost_usd": 0.05,
                "net_savings_usd": round(normalize_price_to_dollars_per_second(ESTIMATED_AI_GEN_COST_PER_SEC, unit="second") * DEFAULT_SHOT_DURATION_SEC * AVG_RERUN_MULTIPLIER - 0.05, 2),
                "recommendation": "Use existing stock footage or hybrid VFX plate to reduce cost and rendering time.",
            },
        }

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json",
        "User-Agent": "Google-ADK-CostOptimizerAgent/1.0",
    }

    try:
        response = requests.post(
            PARALLEL_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        if response.status_code == 200:
            data = response.json()
            raw_results = data.get("results", [])
            formatted = []
            for item in raw_results[:max_results]:
                raw_ex = item.get("excerpts", [])
                ex_str = "\n".join(raw_ex) if isinstance(raw_ex, list) else str(raw_ex or item.get("snippet", ""))
                formatted.append({
                    "title": item.get("title", "Video Asset"),
                    "url": item.get("url", ""),
                    "excerpts": ex_str,
                    "source": item.get("source", "Live Stock Result"),
                    "score": item.get("score"),
                })

            return {
                "status": "success",
                "shot_description": shot_description,
                "objective": objective,
                "queries_used": queries,
                "results_count": len(formatted),
                "results": formatted,
            }
        else:
            return {
                "status": "api_error",
                "status_code": response.status_code,
                "error_details": response.text,
                "shot_description": shot_description,
                "queries_used": queries,
            }

    except requests.RequestException as err:
        logger.exception("Error calling Parallel Search API: %s", err)
        return {
            "status": "network_error",
            "error_message": str(err),
            "shot_description": shot_description,
        }
