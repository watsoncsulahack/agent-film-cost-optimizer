"""Main CLI entrypoint and evaluation runner for CostOptimizerAgent."""

import argparse
import asyncio
import json
import os
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types

from cost_optimizer_agent.agent import root_agent
from cost_optimizer_agent.tools import parallel_search_video_footage

SAMPLE_SHOTS = [
    {
        "title": "Establishing Shot - City Skyline",
        "description": "Cinematic aerial drone shot sweeping over a modern metropolis skyline at golden hour sunset, lens flare and reflective glass towers",
    },
    {
        "title": "Atmospheric Nature B-Roll",
        "description": "Slow-motion macro close up of raindrops falling on lush green jungle leaves with soft atmospheric mist and natural lighting",
    },
    {
        "title": "Dialogue Shot - Character Interaction",
        "description": "Medium close-up of a cyberpunk detective in a neon-lit alleyway arguing with a robotic informant in heavy rain",
    },
]


async def run_agent_query(runner: InMemoryRunner, prompt: str, user_id: str = "filmmaker", session_id: str = "session_001"):
    """Runs a single prompt through the ADK InMemoryRunner."""
    print(f"\n{'='*70}")
    print(f"🎬 SHOT PROMPT: {prompt}")
    print(f"{'='*70}\n")

    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"Please analyze and optimize this video shot prompt for production cost: '{prompt}'")]
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
    ):
        # Print tool calls and agent responses as they stream
        if hasattr(event, "content") and event.content:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    print(part.text, end="", flush=True)
                elif getattr(part, "function_call", None):
                    print(f"\n[Tool Call] -> {part.function_call.name}({part.function_call.args})\n")
                elif getattr(part, "function_response", None):
                    print(f"\n[Tool Response] -> {part.function_response.name} completed.\n")
    print("\n")


def run_tool_only(shot_description: str):
    """Directly calls the Parallel Search API tool without LLM runner."""
    print(f"\n[Parallel Search API Tool Direct Execution]")
    print(f"Querying for: {shot_description}\n")
    res = parallel_search_video_footage(shot_description=shot_description)
    print(json.dumps(res, indent=2))


async def main():
    parser = argparse.ArgumentParser(description="CostOptimizerAgent - AI Film Production Cost Optimization")
    parser.add_argument("--shot", type=str, help="Specific shot description to analyze")
    parser.add_argument("--tool-only", action="store_true", help="Execute only the Parallel Search tool without agent runner")
    parser.add_argument("--demo", action="store_true", help="Run automated showcase with sample film shots")

    args = parser.parse_args()

    if args.tool_only:
        shot = args.shot or SAMPLE_SHOTS[0]["description"]
        run_tool_only(shot)
        return

    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    parallel_key = os.environ.get("PARALLEL_API_KEY", "").strip()

    if not gemini_key:
        print("ERROR: GEMINI_API_KEY environment variable is required. Please set it in .env or your shell environment.")
        sys.exit(1)
    if not parallel_key:
        print("ERROR: PARALLEL_API_KEY environment variable is required. Please set it in .env or your shell environment.")
        sys.exit(1)

    runner = InMemoryRunner(agent=root_agent)

    if args.shot:
        await run_agent_query(runner, args.shot)
        return

    # Default to demo mode
    print("=======================================================================")
    print("  CostOptimizerAgent - Google ADK with Parallel Search API Integration")
    print("=======================================================================")

    for idx, sample in enumerate(SAMPLE_SHOTS, 1):
        print(f"\n--- Sample {idx}: {sample['title']} ---")
        await run_agent_query(runner, sample["description"], session_id=f"session_{idx}")


if __name__ == "__main__":
    asyncio.run(main())
