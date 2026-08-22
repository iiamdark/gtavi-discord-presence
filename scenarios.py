"""
Grand Theft Auto VI - Playtest Scenarios & Activity Pool
Authentic location names, mission titles, character states, and debug telemetry.
"""

import random
from typing import Dict, Any, List

CHARACTERS = [
    {"name": "Lucia Caminos", "icon": "lucia_icon", "role": "Heist Specialist"},
    {"name": "Jason Duane", "icon": "jason_icon", "role": "Wheelman"},
    {"name": "Lucia & Jason", "icon": "duo_icon", "role": "Co-op Campaign"},
]

LOCATIONS = [
    "Vice Beach (Ocean Drive)",
    "Downtown Vice City",
    "Port Gellhorn",
    "Grassrivers Wetlands",
    "Vice City Keys (Sundown Key)",
    "Little Haiti",
    "Biscayne Bay Marina",
    "Ambrosia County",
    "Leonida International Airport",
    "Starfish Island",
    "Mount Leonida Foothills",
    "Vice City Harbor",
]

BUILD_TAGS = [
    "Build #8492-REL-DVT (Leonida QA)",
    "RAGE Engine 9.4 | 144 FPS",
    "v1.0.8492-alpha (D3D12_RELEASE)",
    "Internal Playtest | NDA Protected",
    "Branch: //gta6/rel_leonida_dev",
]

SCENARIO_TEMPLATES: List[Dict[str, Any]] = [
    # Story Missions
    {
        "details": "Mission: \"High Stakes Delivery\"",
        "state_template": "{location} - Evading VCPD",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | {role}",
    },
    {
        "details": "Mission: \"First National Score\" (Heist)",
        "state_template": "{location} - Safe Cracking",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | In Combat",
    },
    {
        "details": "Mission: \"Neon Horizon\"",
        "state_template": "{location} - In Cutscene",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Story Act II",
    },
    {
        "details": "Mission: \"Contraband Run\"",
        "state_template": "{location} - Smuggling by Speedboat",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | {role}",
    },
    {
        "details": "Mission: \"Bail Bonds & Broken Chains\"",
        "state_template": "{location} - Tracking Target",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | {role}",
    },

    # Pursuits & Wanted Levels
    {
        "details": "Police Pursuit (★★★★☆)",
        "state_template": "{location} - In High-Speed Chase",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": "wanted_icon",
        "small_text_template": "Wanted Level: 4 Stars | {character_name}",
    },
    {
        "details": "Police Pursuit (★★★★★)",
        "state_template": "{location} - SWAT & Helicopter Response",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": "wanted_icon",
        "small_text_template": "Wanted Level: MAXIMUM | {character_name}",
    },

    # Free Roam & Open World
    {
        "details": "Cruising in Grotti Turismo",
        "state_template": "{location} (Free Roam)",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Listening to Flash FM",
    },
    {
        "details": "Exploring Open World",
        "state_template": "{location} (Exploration)",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | {role}",
    },
    {
        "details": "Airboating through Grassrivers",
        "state_template": "{location} - Wildlife Hunting",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Everglades",
    },
    {
        "details": "Robbing Diner (24/7 Supermarket)",
        "state_template": "{location} - Escape in Progress",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Wanted (★★☆☆☆)",
    },
    {
        "details": "Customizing Pegassi Infernus",
        "state_template": "{location} - Los Santos Customs Vice",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Garage",
    },
    {
        "details": "Weapon Wheel Bench / Safehouse",
        "state_template": "{location} - Upgrading Arsenal",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Safehouse",
    },
    {
        "details": "Stunt Jump / Night Cruising",
        "state_template": "{location} - Ocean View Strip",
        "large_image": "gtavi_cover",
        "large_text_template": "Grand Theft Auto VI ({build})",
        "small_image_override": None,
        "small_text_template": "{character_name} | Free Roam",
    },
]


def generate_scenario(custom_build_tag: str = None) -> Dict[str, str]:
    """Generates a realistic randomized GTA VI activity payload."""
    template = random.choice(SCENARIO_TEMPLATES)
    character = random.choice(CHARACTERS)
    location = random.choice(LOCATIONS)
    build = custom_build_tag or random.choice(BUILD_TAGS)

    small_image = template["small_image_override"] or character["icon"]

    details = template["details"]
    state = template["state_template"].format(
        location=location,
        character_name=character["name"],
    )
    large_text = template["large_text_template"].format(
        build=build,
        location=location,
    )
    small_text = template["small_text_template"].format(
        character_name=character["name"],
        role=character["role"],
    )

    return {
        "details": details,
        "state": state,
        "large_image": template["large_image"],
        "large_text": large_text,
        "small_image": small_image,
        "small_text": small_text,
        "location": location,
        "character": character["name"],
    }
