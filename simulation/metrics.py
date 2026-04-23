from collections import defaultdict


def compute_simulation_metrics(simulation_results: list[dict]) -> dict:
    """
    Takes a list of scenario transcripts and returns a team dynamics report.
    """
    if not simulation_results:
        return {}

    roles = _get_all_roles(simulation_results)
    metrics = {
        "scenarios_run": len(simulation_results),
        "outcomes": _count_outcomes(simulation_results),
        "alignment_matrix": _compute_alignment_matrix(simulation_results, roles),
        "strongest_alignment": None,
        "biggest_fault_line": None,
        "decision_velocity": _compute_decision_velocity(simulation_results),
        "role_influence": _compute_role_influence(simulation_results, roles),
        "deadlock_scenarios": _get_deadlock_scenarios(simulation_results),
        "team_risk_profile": _compute_risk_profile(simulation_results),
        "groupthink_warning": _detect_groupthink(simulation_results),
    }

    metrics["strongest_alignment"], metrics["biggest_fault_line"] = _find_alignment_extremes(
        metrics["alignment_matrix"]
    )

    return metrics


def _get_all_roles(results: list[dict]) -> list[str]:
    roles = set()
    for r in results:
        roles.update(r.get("votes", {}).keys())
    return sorted(roles)


def _count_outcomes(results: list[dict]) -> dict:
    counts = defaultdict(int)
    for r in results:
        outcome = r.get("outcome", "UNKNOWN")
        if "APPROVE" in outcome:
            counts["approved"] += 1
        elif "REJECT" in outcome:
            counts["rejected"] += 1
        elif "DEADLOCK" in outcome:
            counts["deadlocked"] += 1
    return dict(counts)


def _compute_alignment_matrix(results: list[dict], roles: list[str]) -> dict:
    agreement_counts = defaultdict(int)
    pair_counts = defaultdict(int)

    for result in results:
        votes = result.get("votes", {})
        role_votes = {role: data["vote"] for role, data in votes.items()}

        role_list = list(role_votes.keys())
        for i in range(len(role_list)):
            for j in range(i + 1, len(role_list)):
                r1, r2 = role_list[i], role_list[j]
                pair = f"{r1}↔{r2}"
                pair_counts[pair] += 1
                if role_votes[r1] == role_votes[r2]:
                    agreement_counts[pair] += 1

    matrix = {}
    for pair, total in pair_counts.items():
        matrix[pair] = round(agreement_counts[pair] / total * 100) if total > 0 else 0

    return matrix


def _find_alignment_extremes(matrix: dict) -> tuple[str | None, str | None]:
    if not matrix:
        return None, None
    strongest = max(matrix, key=matrix.get)
    weakest = min(matrix, key=matrix.get)
    strongest_pct = matrix[strongest]
    weakest_pct = matrix[weakest]
    return f"{strongest} ({strongest_pct}% agreement)", f"{weakest} ({weakest_pct}% agreement)"


def _compute_decision_velocity(results: list[dict]) -> dict:
    category_rounds = defaultdict(list)
    for result in results:
        category = result["scenario"].get("category", "unknown")
        rounds = len(result.get("rounds", {}))
        category_rounds[category].append(rounds)

    return {
        cat: round(sum(v) / len(v), 1)
        for cat, v in category_rounds.items()
    }


def _compute_role_influence(results: list[dict], roles: list[str]) -> dict:
    """
    Approximates influence by counting how often each role's vote matched the final outcome.
    """
    match_counts = defaultdict(int)
    total_counts = defaultdict(int)

    for result in results:
        outcome = result.get("outcome", "")
        votes = result.get("votes", {})

        outcome_direction = "APPROVE" if "APPROVE" in outcome else ("REJECT" if "REJECT" in outcome else None)
        if not outcome_direction:
            continue

        for role, data in votes.items():
            total_counts[role] += 1
            vote = data.get("vote", "")
            if vote == outcome_direction or (outcome_direction == "APPROVE" and vote == "CONDITIONAL"):
                match_counts[role] += 1

    return {
        role: round(match_counts[role] / total_counts[role] * 100) if total_counts[role] > 0 else 0
        for role in roles
    }


def _get_deadlock_scenarios(results: list[dict]) -> list[str]:
    return [
        r["scenario"]["title"]
        for r in results
        if "DEADLOCK" in r.get("outcome", "")
    ]


def _compute_risk_profile(results: list[dict]) -> str:
    approve_count = sum(
        1 for r in results
        if "APPROVE" in r.get("outcome", "")
    )
    total = len(results)
    if total == 0:
        return "Unknown"

    ratio = approve_count / total
    if ratio >= 0.75:
        return "Aggressive"
    if ratio >= 0.5:
        return "Moderately Aggressive"
    if ratio >= 0.35:
        return "Balanced"
    return "Conservative"


def _detect_groupthink(results: list[dict]) -> list[str]:
    """
    Flags scenarios where all agents voted the same way (no dissent).
    """
    flagged = []
    for result in results:
        votes = result.get("votes", {})
        unique_votes = set(d["vote"] for d in votes.values())
        if len(unique_votes) == 1:
            flagged.append(result["scenario"]["title"])
    return flagged


def format_report(metrics: dict) -> str:
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "           TEAM DYNAMICS REPORT",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"Scenarios Run:        {metrics.get('scenarios_run', 0)}",
    ]

    outcomes = metrics.get("outcomes", {})
    lines.append(
        f"Outcomes:             {outcomes.get('approved', 0)} approved / "
        f"{outcomes.get('rejected', 0)} rejected / "
        f"{outcomes.get('deadlocked', 0)} deadlocked"
    )

    lines.append(f"Team Risk Profile:    {metrics.get('team_risk_profile', 'Unknown')}")
    lines.append(f"Strongest Alignment:  {metrics.get('strongest_alignment', 'N/A')}")
    lines.append(f"Biggest Fault Line:   {metrics.get('biggest_fault_line', 'N/A')}")

    influence = metrics.get("role_influence", {})
    if influence:
        lines.append("\nRole Influence (% votes matched outcome):")
        for role, pct in sorted(influence.items(), key=lambda x: -x[1]):
            lines.append(f"  {role:<8} {pct}%")

    deadlocks = metrics.get("deadlock_scenarios", [])
    if deadlocks:
        lines.append(f"\nDeadlock Scenarios ({len(deadlocks)}):")
        for title in deadlocks:
            lines.append(f"  ⚠️  {title}")

    groupthink = metrics.get("groupthink_warning", [])
    if groupthink:
        lines.append(f"\nGroupthink Warnings (no dissent in {len(groupthink)} scenarios):")
        for title in groupthink:
            lines.append(f"  ⚠️  {title}")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)
