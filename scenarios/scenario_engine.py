import json
import random
from pathlib import Path

LIBRARY_PATH = Path(__file__).parent / "scenario_library.json"

SCENARIO_PACKS = {
    "Early Stage Gauntlet": ["funding_001", "hiring_001", "product_001", "pivot_001", "comp_001"],
    "Team Dynamics": ["team_001", "team_002", "ops_001", "hiring_002", "ethics_002"],
    "Growth & Scale": ["growth_001", "growth_002", "growth_003", "strategy_001", "strategy_002"],
    "Crisis Mode": ["crisis_001", "crisis_002", "market_001", "legal_001", "ai_001"],
    "Full Stress Test": None,
}


def load_all_scenarios() -> list[dict]:
    return json.loads(LIBRARY_PATH.read_text())


def get_scenario_by_id(scenario_id: str) -> dict | None:
    scenarios = load_all_scenarios()
    return next((s for s in scenarios if s["id"] == scenario_id), None)


def get_scenarios_by_category(category: str) -> list[dict]:
    return [s for s in load_all_scenarios() if s["category"] == category]


def get_scenario_pack(pack_name: str, count: int = 5) -> list[dict]:
    all_scenarios = load_all_scenarios()
    scenario_map = {s["id"]: s for s in all_scenarios}

    if pack_name == "Full Stress Test":
        selected = random.sample(all_scenarios, min(count, len(all_scenarios)))
        return selected

    ids = SCENARIO_PACKS.get(pack_name, [])
    return [scenario_map[sid] for sid in ids if sid in scenario_map]


def get_all_categories() -> list[str]:
    scenarios = load_all_scenarios()
    return sorted(set(s["category"] for s in scenarios))


def get_all_pack_names() -> list[str]:
    return list(SCENARIO_PACKS.keys())
