"""Configuration settings for CostOptimizerAgent."""

import os
from dotenv import load_dotenv

# Load .env file if available
load_dotenv()

# Model configuration
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Parallel API configuration
PARALLEL_API_KEY = os.environ.get("PARALLEL_API_KEY", "")
PARALLEL_API_URL = os.environ.get("PARALLEL_API_URL", "https://api.parallel.ai/v1/search")

# Cost optimization benchmark defaults (USD)
ESTIMATED_AI_GEN_COST_PER_SEC = float(os.environ.get("AI_GEN_COST_PER_SEC", "0.07"))  # e.g., ~$0.35 for 5s shot
DEFAULT_SHOT_DURATION_SEC = 5.0
AVG_RERUN_MULTIPLIER = 2.2  # AI video generation usually requires 2-3 reruns to get the desired shot
