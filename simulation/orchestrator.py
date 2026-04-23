from agents.base_agent import BaseAgent

ROUNDS = 3


def run_scenario(agents: list[BaseAgent], scenario: dict) -> dict:
    """
    Runs a full 3-round debate for a single scenario.
    Returns a transcript dict with all responses, votes, and outcome.
    """
    transcript = {
        "scenario": scenario,
        "rounds": {},
        "votes": {},
        "outcome": None,
        "outcome_reason": None
    }

    conversation_history = []

    for round_num in range(1, ROUNDS + 1):
        round_responses = {}

        for agent in agents:
            response = agent.respond(scenario, conversation_history, round_num)
            round_responses[agent.role] = {
                "name": agent.name,
                "response": response
            }

            conversation_history.append({
                "role": "assistant",
                "content": f"[{agent.role} - {agent.name}]: {response}"
            })

        transcript["rounds"][round_num] = round_responses

    votes = {}
    for agent in agents:
        vote_text = agent.vote(scenario, conversation_history)
        vote_label = _extract_vote(vote_text)
        votes[agent.role] = {
            "name": agent.name,
            "raw": vote_text,
            "vote": vote_label
        }

    transcript["votes"] = votes
    transcript["outcome"], transcript["outcome_reason"] = _determine_outcome(votes, agents)

    return transcript


def _extract_vote(vote_text: str) -> str:
    upper = vote_text.upper()
    if "CONDITIONAL" in upper:
        return "CONDITIONAL"
    if "APPROVE" in upper:
        return "APPROVE"
    if "REJECT" in upper:
        return "REJECT"
    return "ABSTAIN"


def _determine_outcome(votes: dict, agents: list[BaseAgent]) -> tuple[str, str]:
    counts = {"APPROVE": 0, "REJECT": 0, "CONDITIONAL": 0, "ABSTAIN": 0}
    for v in votes.values():
        counts[v["vote"]] += 1

    total = len(agents)
    approve_total = counts["APPROVE"] + counts["CONDITIONAL"]

    if counts["APPROVE"] >= (total / 2 + 1):
        return "CONSENSUS APPROVE", f"{counts['APPROVE']}/{total} voted Approve"

    if counts["REJECT"] >= (total / 2 + 1):
        return "CONSENSUS REJECT", f"{counts['REJECT']}/{total} voted Reject"

    ceo_vote = votes.get("CEO", {}).get("vote")
    if ceo_vote in ("APPROVE", "CONDITIONAL"):
        return "CEO DECISION — APPROVE", "No consensus reached. CEO used tie-break to approve."
    if ceo_vote == "REJECT":
        return "CEO DECISION — REJECT", "No consensus reached. CEO used tie-break to reject."

    return "DEADLOCK", "No consensus and CEO abstained. This scenario requires further discussion."
