import os
import anthropic

try:
    import streamlit as st
    _api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    _model = st.secrets.get("SIMULATION_MODEL") or os.getenv("SIMULATION_MODEL", "claude-haiku-4-5-20251001")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    _api_key = os.getenv("ANTHROPIC_API_KEY")
    _model = os.getenv("SIMULATION_MODEL", "claude-haiku-4-5-20251001")

MODEL = _model

SYSTEM_SUFFIX = """
## Simulation Rules
- Stay strictly in character based on your role and personality.
- Be direct and opinionated — you have a clear point of view.
- When you disagree with another executive, say so explicitly and explain why.
- When you agree, say so and build on their point.
- Keep responses under 150 words unless the complexity demands more.
- End every Round 1 and Round 2 response with your current lean: APPROVE / REJECT / CONDITIONAL / UNDECIDED.
- In Round 3 (final), end with your FINAL VOTE: APPROVE / REJECT / CONDITIONAL APPROVAL.
"""


class BaseAgent:
    def __init__(self, role: str, persona_text: str, name: str = ""):
        self.role = role
        self.name = name or role
        self.persona_text = persona_text
        self.client = anthropic.Anthropic(api_key=_api_key)
        self._system_prompt = persona_text + SYSTEM_SUFFIX

    def respond(self, scenario: dict, conversation_history: list[dict], round_num: int) -> str:
        scenario_context = self._format_scenario(scenario, round_num)

        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": scenario_context})

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=[
                {
                    "type": "text",
                    "text": self._system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=messages
        )

        return response.content[0].text

    def vote(self, scenario: dict, conversation_history: list[dict]) -> str:
        messages = list(conversation_history)
        messages.append({
            "role": "user",
            "content": (
                "All debate rounds are complete. Cast your FINAL VOTE on this scenario.\n"
                "Reply with ONLY one of: APPROVE / REJECT / CONDITIONAL APPROVAL\n"
                "Then one sentence explaining your reasoning."
            )
        })

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=100,
            system=[
                {
                    "type": "text",
                    "text": self._system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=messages
        )

        return response.content[0].text

    def _format_scenario(self, scenario: dict, round_num: int) -> str:
        data_points = "\n".join(
            f"  - {k.replace('_', ' ').title()}: {v}"
            for k, v in scenario.get("data_points", {}).items()
        )

        round_instructions = {
            1: "This is Round 1. Give your INITIAL STANCE on this scenario. Be direct.",
            2: "This is Round 2. You've heard your colleagues' initial positions above. Respond to them — agree, push back, or propose a middle ground.",
            3: "This is Round 3 — FINAL POSITIONS. State your final stance. You may shift from your earlier position if persuaded. End with FINAL VOTE: APPROVE / REJECT / CONDITIONAL APPROVAL."
        }

        return f"""
SCENARIO: {scenario['title']}
CATEGORY: {scenario['category'].upper()}

CONTEXT:
{scenario['context']}

KEY DATA:
{data_points}

THE QUESTION:
{scenario['trigger_question']}

---
{round_instructions.get(round_num, 'Respond to this scenario.')}
"""
