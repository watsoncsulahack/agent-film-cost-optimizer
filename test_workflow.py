"""Tests for the 9-step CostOptimizerAgent workflow and 2 tools."""

from cost_optimizer_agent.cost_engine import run_cost_engine
from cost_optimizer_agent.parallel_search_tool import search_video_models_and_pricing
from cost_optimizer_agent.shot_analysis_tool import analyze_shot_requirements


def test_tool_1_shot_analysis():
    # Drone aerial shot
    reqs = analyze_shot_requirements("Cinematic aerial drone shot of modern city skyline at golden hour sunset")
    assert reqs["subject_type"] == "landscape_environment"
    assert reqs["camera_movement"] == "drone_aerial"
    assert reqs["requires_camera_control"] is True
    assert "camera_motion_control" in reqs["essential_capabilities"]

    # Cyberpunk dialogue
    reqs_char = analyze_shot_requirements("Close up of a cyberpunk detective in neon alley arguing with robot informant in rain")
    assert reqs_char["subject_type"] == "character_dialogue"
    assert reqs_char["requires_character_dialogue"] is True
    assert "character_anatomy_consistency" in reqs_char["essential_capabilities"]


import pytest
from cost_optimizer_agent.gemini_service import run_gemini_shot_reasoning


def test_tool_2_parallel_search_missing_key_raises_error(monkeypatch):
    monkeypatch.delenv("PARALLEL_API_KEY", raising=False)
    with pytest.raises(ValueError, match="PARALLEL_API_KEY is strictly required"):
        search_video_models_and_pricing("Google Veo Vertex AI pricing capabilities limitations", api_key="")


def test_gemini_service_missing_key_raises_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GEMINI_API_KEY is strictly required"):
        run_gemini_shot_reasoning("drone shot", 5.0, 2.0, [], [], api_key="")


def test_cost_engine_elimination_and_ranking():
    # Shot requiring camera control
    shot_reqs = {
        "shot_description": "Drone shot rising over Manhattan skyline",
        "essential_capabilities": ["high_photorealism", "camera_motion_control"],
    }
    evaluation = run_cost_engine(shot_reqs, duration_seconds=5.0, rerun_multiplier=2.0)

    # Models without camera control (like Hailuo, MiniMax-H3) should be eliminated
    elim_names = [m.model_name for m in evaluation.eliminated_models]
    assert "Hailuo" in elim_names or "MiniMax-H3" in elim_names

    # Viable models should include Runway and Veo
    viable_names = [m.model_name for m in evaluation.viable_models]
    assert "Runway-Gen3-Turbo" in viable_names
    assert "Veo" in viable_names

    # Recommended model must be the lowest-cost viable model
    assert evaluation.recommended_model.model_name == "Runway-Gen3-Turbo"
    assert evaluation.projected_savings_usd > 0
    assert "Tradeoff:" in evaluation.tradeoff_explanation
