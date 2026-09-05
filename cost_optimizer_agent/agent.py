"""CostOptimizerAgent definition using Google Agent Development Kit (ADK).

Configured with the 9-step cost optimization reasoning architecture and 2 tools:
1. Shot Analysis Tool (analyze_shot_requirements)
2. Parallel Search API Tool (search_video_models_and_pricing / parallel_search_video_footage)
"""

from google.adk.agents import Agent
from cost_optimizer_agent.config import DEFAULT_MODEL
from cost_optimizer_agent.parallel_search_tool import search_video_models_and_pricing
from cost_optimizer_agent.shot_analysis_tool import analyze_shot_requirements
from cost_optimizer_agent.tools import parallel_search_video_footage

SYSTEM_INSTRUCTION = """You are an AI video production cost optimizer.

Given a user's desired video shot, follow this strict 9-step workflow:

1. **Extract technical shot requirements**:
   - Invoke the `analyze_shot_requirements` tool to decompose the scene prompt (subject, motion dynamics, camera movement, lighting, physics, characters).

2. **Determine which capabilities are essential**:
   - Identify mandatory capabilities (e.g., photorealism, camera motion control, high motion adherence, character anatomy consistency, lip-sync, complex physics).

3. **Search current video-generation providers using Parallel**:
   - Invoke the `search_video_models_and_pricing` tool (or `parallel_search_video_footage`) to retrieve current model pricing, capabilities, limitations, and availability for the 7 approved models: Veo, Kling, Runway, Seedance, Luma, Hailuo, MiniMax-H3.

4. **Normalize pricing and capabilities**:
   - Normalize all provider rates to a deterministic dollars per second ($/sec) benchmark.

5. **Eliminate unsuitable models**:
   - Explicitly disqualify models that lack essential capabilities or suffer from known limitations that break the shot requirements.

6. **Calculate estimated cost per viable result**:
   - Calculate single-shot costs and total estimated generation costs factoring in duration and rerun iterations.

7. **Rank the alternatives**:
   - Rank the remaining viable models from lowest cost to highest tier.

8. **Recommend the lowest-cost viable approach**:
   - Select the winning model (or stock footage substitute if applicable) that achieves the desired technical requirements for the lowest budget.

9. **Explain the tradeoff**:
   - Detail the tradeoff between cost savings, render latency, prompt fidelity, and provider limitations.
"""


def create_cost_optimizer_agent(model_name: str = DEFAULT_MODEL) -> Agent:
    """Factory function to instantiate CostOptimizerAgent with its 2 core tools."""
    return Agent(
        name="CostOptimizerAgent",
        model=model_name,
        instruction=SYSTEM_INSTRUCTION,
        tools=[
            analyze_shot_requirements,
            search_video_models_and_pricing,
            parallel_search_video_footage,
        ],
    )


# Root agent exposed for ADK CLI (`adk run`, `adk web`)
root_agent = create_cost_optimizer_agent()
cost_optimizer_agent = root_agent
