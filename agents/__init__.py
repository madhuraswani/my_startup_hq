from agents.base_agent import BaseAgent

AVAILABLE_ROLES = ["CEO", "CMO", "CTO", "CFO"]


def build_agent(role: str, persona_text: str, name: str = "") -> BaseAgent:
    return BaseAgent(role=role, persona_text=persona_text, name=name)
