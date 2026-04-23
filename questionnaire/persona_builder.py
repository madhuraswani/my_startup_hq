import json
import os
from pathlib import Path
from questionnaire.questions import ROLE_QUESTIONS, TRAIT_TO_PERSONA_MODIFIER

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
BASE_DATA_DIR = Path(__file__).parent.parent / "data" / "teams"


def _team_dir(team_code: str) -> Path:
    path = BASE_DATA_DIR / team_code.upper()
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_persona(role: str, answers: dict[str, str]) -> str:
    base_persona_path = PROMPTS_DIR / f"{role}_persona.md"
    base_persona = base_persona_path.read_text()

    questions = ROLE_QUESTIONS.get(role, [])
    trait_modifiers = []

    for question in questions:
        qid = question["id"]
        trait = question["trait"]
        chosen_option = answers.get(qid)
        if chosen_option and trait in TRAIT_TO_PERSONA_MODIFIER:
            modifier = TRAIT_TO_PERSONA_MODIFIER[trait].get(chosen_option)
            if modifier:
                trait_modifiers.append(f"- {modifier}")

    if not trait_modifiers:
        return base_persona

    modifier_block = "\n## Personality Modifiers (from questionnaire)\n" + "\n".join(trait_modifiers)
    return base_persona + modifier_block


def save_team_persona(role: str, answers: dict[str, str], team_code: str, name: str = "") -> str:
    persona_text = build_persona(role, answers)
    filepath = _team_dir(team_code) / f"{role.lower()}_persona.json"

    data = {
        "role": role,
        "name": name,
        "team_code": team_code.upper(),
        "answers": answers,
        "persona_text": persona_text
    }

    filepath.write_text(json.dumps(data, indent=2))
    return persona_text


def load_team_personas(team_code: str) -> dict[str, dict]:
    personas = {}
    team_path = BASE_DATA_DIR / team_code.upper()
    if not team_path.exists():
        return personas

    for filepath in team_path.glob("*_persona.json"):
        data = json.loads(filepath.read_text())
        role = data["role"]
        personas[role] = data

    return personas


def load_persona_text(role: str, team_code: str) -> str:
    filepath = BASE_DATA_DIR / team_code.upper() / f"{role.lower()}_persona.json"
    if filepath.exists():
        data = json.loads(filepath.read_text())
        return data["persona_text"]

    base_persona_path = PROMPTS_DIR / f"{role}_persona.md"
    if base_persona_path.exists():
        return base_persona_path.read_text()

    return f"You are the {role} of an early-stage startup. Act in character."
