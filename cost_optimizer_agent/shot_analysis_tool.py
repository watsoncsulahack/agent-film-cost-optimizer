"""Shot Analysis Tool for extracting technical requirements and essential capabilities from shot descriptions."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TechnicalShotRequirements:
    """Structured technical requirements extracted from an AI-video shot description."""
    shot_description: str
    subject_type: str  # 'character', 'landscape_environment', 'object_vehicle', 'action_vfx', 'macro_texture'
    motion_dynamics: str  # 'high_speed_action', 'moderate_motion', 'slow_cinematic', 'subtle_ambient'
    camera_movement: str  # 'drone_aerial', 'tracking_follow', 'orbit_pan', 'dolly_zoom', 'handheld', 'static'
    lighting_style: str  # 'golden_hour', 'neon_cyberpunk', 'dramatic_cinematic', 'natural_ambient', 'studio_clean'
    environment_complexity: str  # 'high_detail_city', 'natural_wilderness', 'interior_room', 'abstract_minimal'
    physics_complexity: str  # 'complex_fluid_particles', 'rigid_body_vehicles', 'soft_body_fabric', 'standard'
    character_count: int = 0
    requires_human_face_consistency: bool = False
    requires_character_dialogue: bool = False
    requires_camera_control: bool = False
    requires_complex_physics: bool = False
    requires_photorealism: bool = False
    essential_capabilities: List[str] = field(default_factory=list)


def analyze_shot_requirements(shot_description: str) -> Dict[str, Any]:
    """Extracts technical shot requirements and determines essential capabilities needed.

    This tool deconstructs an AI-video shot prompt into its core visual, physics,
    camera, and subject constraints to determine which AI video model capabilities are mandatory.

    Args:
        shot_description: Detailed description of the video shot, scene prompt, or storyboard brief.

    Returns:
        Dict containing structured technical requirements, flags, and essential capabilities.
    """
    desc = shot_description.strip().lower()

    # 1. Subject classification
    character_keywords = ["person", "man", "woman", "detective", "robot", "girl", "boy", "face", "talking", "arguing", "crowd", "people", "warrior", "actor", "interview"]
    has_character = any(k in desc for k in character_keywords)
    has_dialogue = any(k in desc for k in ["talking", "arguing", "speaking", "dialogue", "conversation", "interview", "saying", "whispering"])
    is_macro = any(k in desc for k in ["macro", "close up", "close-up", "raindrop", "leaves", "eye", "texture", "drop", "extreme close"])
    is_landscape = any(k in desc for k in ["skyline", "city", "mountains", "alps", "ocean", "beach", "sunset", "aerial", "drone", "forest", "desert", "landscape", "valley"])

    if has_dialogue:
        subject_type = "character_dialogue"
    elif has_character:
        subject_type = "character"
    elif is_macro:
        subject_type = "macro_texture"
    elif is_landscape:
        subject_type = "landscape_environment"
    else:
        subject_type = "action_vfx"

    # 2. Camera movement detection
    if any(k in desc for k in ["drone", "aerial", "sweeping", "bird's eye", "overhead"]):
        camera_movement = "drone_aerial"
        requires_camera_control = True
    elif any(k in desc for k in ["tracking", "follow", "chase", "steadicam"]):
        camera_movement = "tracking_follow"
        requires_camera_control = True
    elif any(k in desc for k in ["orbit", "pan", "panning", "tilt", "rotating"]):
        camera_movement = "orbit_pan"
        requires_camera_control = True
    elif any(k in desc for k in ["dolly", "zoom", "push in", "pull out"]):
        camera_movement = "dolly_zoom"
        requires_camera_control = True
    elif any(k in desc for k in ["handheld", "shaky", "documentary"]):
        camera_movement = "handheld"
        requires_camera_control = False
    else:
        camera_movement = "cinematic_static"
        requires_camera_control = False

    # 3. Motion dynamics
    if any(k in desc for k in ["fast", "running", "chase", "explosion", "fight", "blizzard", "storm", "racing", "speeding", "flying"]):
        motion_dynamics = "high_speed_action"
    elif any(k in desc for k in ["slow motion", "slow-motion", "slowmo", "macro", "falling raindrops", "gentle"]):
        motion_dynamics = "slow_cinematic"
    else:
        motion_dynamics = "moderate_motion"

    # 4. Physics complexity
    if any(k in desc for k in ["rain", "raindrops", "water", "fluid", "smoke", "fire", "particles", "snow", "blizzard", "splash", "waves"]):
        requires_complex_physics = True
        physics_complexity = "complex_fluid_particles"
    elif any(k in desc for k in ["car", "vehicle", "spaceship", "robot", "cyberpunk"]):
        requires_complex_physics = True
        physics_complexity = "rigid_body_vehicles"
    else:
        requires_complex_physics = False
        physics_complexity = "standard"

    # 5. Photorealism
    requires_photorealism = not any(k in desc for k in ["anime", "cartoon", "cgi", "illustration", "painting", "claymation", "3d render"])

    # 6. Build essential capabilities list
    essential_caps = []
    if requires_photorealism:
        essential_caps.append("high_photorealism")
    if requires_camera_control:
        essential_caps.append("camera_motion_control")
    if motion_dynamics == "high_speed_action":
        essential_caps.append("high_motion_adherence")
    elif motion_dynamics == "slow_cinematic":
        essential_caps.append("high_frame_consistency")
    if requires_complex_physics:
        essential_caps.append("complex_physics_simulation")
    if has_character:
        essential_caps.append("character_anatomy_consistency")
    if has_dialogue:
        essential_caps.append("lip_sync_and_audio")

    reqs = TechnicalShotRequirements(
        shot_description=shot_description,
        subject_type=subject_type,
        motion_dynamics=motion_dynamics,
        camera_movement=camera_movement,
        lighting_style="dramatic_cinematic" if "neon" in desc or "golden" in desc else "natural_ambient",
        environment_complexity="high_detail" if is_landscape or "neon" in desc else "standard",
        physics_complexity=physics_complexity,
        character_count=2 if "arguing" in desc or "dialogue" in desc else (1 if has_character else 0),
        requires_human_face_consistency=has_character,
        requires_character_dialogue=has_dialogue,
        requires_camera_control=requires_camera_control,
        requires_complex_physics=requires_complex_physics,
        requires_photorealism=requires_photorealism,
        essential_capabilities=essential_caps,
    )

    return asdict(reqs)
