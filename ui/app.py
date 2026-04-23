import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from questionnaire.questions import ROLE_QUESTIONS
from questionnaire.persona_builder import save_team_persona, load_team_personas
from agents import build_agent, AVAILABLE_ROLES
from scenarios.scenario_engine import (
    load_all_scenarios, get_scenario_by_id, get_scenario_pack,
    get_all_categories, get_all_pack_names
)
from simulation.orchestrator import run_scenario
from simulation.metrics import compute_simulation_metrics, format_report

ROLE_COLORS = {
    "CEO": "#4A90D9",
    "CMO": "#E67E22",
    "CTO": "#27AE60",
    "CFO": "#8E44AD"
}

ROLE_EMOJI = {
    "CEO": "👔",
    "CMO": "📣",
    "CTO": "⚙️",
    "CFO": "💰"
}

st.set_page_config(
    page_title="Startup HQ — Team Simulation",
    page_icon="🏢",
    layout="wide"
)

if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = []
if "current_transcript" not in st.session_state:
    st.session_state.current_transcript = None
if "team_code" not in st.session_state:
    st.session_state.team_code = ""


def render_team_code_gate():
    """
    Shown on every tab. Returns the active team code or None.
    All data is scoped to this code — share it with your team.
    """
    with st.sidebar:
        st.title("🏢 Startup HQ")
        st.caption("Multi-Agent Team Simulation")
        st.divider()

        st.subheader("Team Code")
        st.caption("Create a code and share it with your team. Everyone uses the same code to join.")

        code_input = st.text_input(
            "Enter or create a team code",
            value=st.session_state.team_code,
            placeholder="e.g. ROCKETSHIP42",
            max_chars=20
        ).strip().upper()

        if st.button("Set Team Code", type="primary", use_container_width=True):
            if code_input:
                st.session_state.team_code = code_input
                st.session_state.simulation_results = []
                st.session_state.current_transcript = None
                st.rerun()
            else:
                st.error("Enter a code first.")

        if st.session_state.team_code:
            st.success(f"Active: **{st.session_state.team_code}**")
            st.caption("Share this code with your team so everyone fills their role.")
            st.divider()

            personas = load_team_personas(st.session_state.team_code)
            if personas:
                st.write(f"**Team ({len(personas)}/4 roles filled)**")
                for role in AVAILABLE_ROLES:
                    if role in personas:
                        name = personas[role].get("name", role)
                        st.write(f"{ROLE_EMOJI.get(role,'')} **{role}** — {name}")
                    else:
                        st.write(f"⬜ {role} — *not filled*")
            else:
                st.info("No roles filled yet for this team.")

            if st.session_state.simulation_results:
                st.divider()
                st.metric("Simulations Run", len(st.session_state.simulation_results))

    return st.session_state.team_code or None


def render_team_setup(team_code: str):
    st.header("Team Setup")
    st.write(
        "Each team member opens this app, enters the team code, picks their role, "
        "and fills the questionnaire. Answers shape how their agent thinks and argues."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        role = st.selectbox("Your Role", AVAILABLE_ROLES)
        name = st.text_input("Your Name", placeholder="e.g. Alex")

    with col2:
        personas = load_team_personas(team_code)
        if role in personas:
            existing_name = personas[role].get("name", role)
            st.info(f"**{role}** is already filled by **{existing_name}**. Submitting will overwrite their answers.")

    st.divider()
    st.subheader(f"{ROLE_EMOJI.get(role, '')} {role} Questionnaire")

    questions = ROLE_QUESTIONS.get(role, [])
    answers = {}

    for q in questions:
        st.write(f"**{q['text']}**")
        options = q["options"]
        choice = st.radio(
            label=q["text"],
            options=list(options.keys()),
            format_func=lambda k, opts=options: f"{k}. {opts[k]}",
            key=f"q_{team_code}_{role}_{q['id']}",
            label_visibility="collapsed"
        )
        answers[q["id"]] = choice
        st.write("")

    if st.button(f"Submit {role} Questionnaire", type="primary"):
        if not name.strip():
            st.error("Please enter your name before submitting.")
        else:
            save_team_persona(role, answers, team_code, name.strip())
            st.success(f"Done! **{name}** saved as {role} for team **{team_code}**.")
            st.balloons()
            st.rerun()


def render_simulation(team_code: str):
    st.header("Run Simulation")

    personas = load_team_personas(team_code)
    if not personas:
        st.warning("No roles filled yet. Share the team code with your team so everyone fills their questionnaire.")
        return

    active_roles = list(personas.keys())
    missing = [r for r in AVAILABLE_ROLES if r not in personas]

    st.info(
        f"Active agents: {', '.join(ROLE_EMOJI.get(r,'') + ' ' + r for r in active_roles)}"
        + (f" · Missing: {', '.join(missing)}" if missing else " · Full team!")
    )

    if len(active_roles) < 2:
        st.warning("Need at least 2 roles filled to run a simulation.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Choose Scenario")
        mode = st.radio("Mode", ["Single Scenario", "Scenario Pack", "Random Stress Test"])

    scenario_to_run = None
    pack_to_run = None

    with col2:
        if mode == "Single Scenario":
            all_scenarios = load_all_scenarios()
            categories = get_all_categories()
            cat_filter = st.selectbox("Filter by category", ["All"] + categories)

            filtered = all_scenarios if cat_filter == "All" else [
                s for s in all_scenarios if s["category"] == cat_filter
            ]
            scenario_titles = {s["title"]: s["id"] for s in filtered}
            chosen_title = st.selectbox("Select scenario", list(scenario_titles.keys()))
            scenario_to_run = get_scenario_by_id(scenario_titles[chosen_title])

            if scenario_to_run:
                with st.expander("Preview"):
                    st.write(f"**Context:** {scenario_to_run['context']}")
                    st.write(f"**Question:** {scenario_to_run['trigger_question']}")
                    for k, v in scenario_to_run.get("data_points", {}).items():
                        st.write(f"- {k.replace('_', ' ').title()}: {v}")

        elif mode == "Scenario Pack":
            chosen_pack = st.selectbox("Select pack", get_all_pack_names())
            pack_to_run = get_scenario_pack(chosen_pack)
            st.write(f"**{len(pack_to_run)} scenarios** in this pack:")
            for s in pack_to_run:
                st.write(f"  • {s['title']}")

        else:
            count = st.slider("Number of random scenarios", 3, 10, 5)
            pack_to_run = get_scenario_pack("Full Stress Test", count)
            st.write(f"**{len(pack_to_run)} scenarios** selected:")
            for s in pack_to_run:
                st.write(f"  • {s['title']}")

    st.divider()

    if st.button("▶ Run Simulation", type="primary", use_container_width=True):
        agents = [
            build_agent(role, personas[role]["persona_text"], personas[role].get("name", role))
            for role in active_roles
        ]
        scenarios_list = [scenario_to_run] if scenario_to_run else pack_to_run

        all_results = []
        progress = st.progress(0)
        status = st.empty()

        for i, scenario in enumerate(scenarios_list):
            status.write(f"Running: **{scenario['title']}** ({i+1}/{len(scenarios_list)})")
            result = run_scenario(agents, scenario)
            all_results.append(result)
            st.session_state.simulation_results.append(result)
            progress.progress((i + 1) / len(scenarios_list))

        st.session_state.current_transcript = all_results
        status.empty()
        progress.empty()
        st.success("Simulation complete! Go to the **Debate Transcript** tab to read the debate.")
        st.rerun()


def render_results():
    st.header("Debate Transcript")

    if not st.session_state.current_transcript:
        st.info("Run a simulation to see the debate replay here.")
        return

    for result in st.session_state.current_transcript:
        scenario = result["scenario"]
        outcome = result["outcome"]

        outcome_color = "green" if "APPROVE" in outcome else ("red" if "REJECT" in outcome else "orange")
        st.markdown(
            f"### {scenario['title']} &nbsp;"
            f"<span style='color:{outcome_color}; font-size:0.85em'>{outcome}</span>",
            unsafe_allow_html=True
        )
        st.caption(f"Category: {scenario['category'].upper()} · Difficulty: {scenario.get('difficulty','').upper()}")

        for round_num, round_data in result["rounds"].items():
            with st.expander(f"Round {round_num}", expanded=(round_num == 1)):
                for role, data in round_data.items():
                    color = ROLE_COLORS.get(role, "#888")
                    emoji = ROLE_EMOJI.get(role, "")
                    st.markdown(
                        f"<div style='border-left: 4px solid {color}; padding: 10px 10px 10px 16px; "
                        f"margin-bottom: 14px; background: #fafafa; border-radius: 4px;'>"
                        f"<strong>{emoji} {role} — {data['name']}</strong><br><br>"
                        f"{data['response']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        st.write("**Final Votes:**")
        vote_cols = st.columns(len(result["votes"]))
        for col, (role, data) in zip(vote_cols, result["votes"].items()):
            vote = data["vote"]
            vote_color = "green" if vote == "APPROVE" else ("red" if vote == "REJECT" else "orange")
            col.markdown(
                f"<div style='text-align:center; padding: 10px; "
                f"border: 2px solid {ROLE_COLORS.get(role, \"#888\")}; border-radius: 8px;'>"
                f"<strong>{ROLE_EMOJI.get(role,'')} {role}</strong><br>"
                f"<small>{data['name']}</small><br>"
                f"<span style='color:{vote_color}; font-weight:bold; font-size:1.1em'>{vote}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.write(f"**Outcome:** {result['outcome_reason']}")
        st.divider()


def render_team_report():
    st.header("Team Dynamics Report")

    all_results = st.session_state.simulation_results
    if not all_results:
        st.info("Run at least one simulation to generate a team report.")
        return

    metrics = compute_simulation_metrics(all_results)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Scenarios Run", metrics["scenarios_run"])
    outcomes = metrics.get("outcomes", {})
    col2.metric("Approved", outcomes.get("approved", 0))
    col3.metric("Rejected", outcomes.get("rejected", 0))
    col4.metric("Deadlocked", outcomes.get("deadlocked", 0))

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Team Profile")
        st.metric("Risk Profile", metrics.get("team_risk_profile", "Unknown"))
        st.write(f"**Strongest Alignment:** {metrics.get('strongest_alignment', 'N/A')}")
        st.write(f"**Biggest Fault Line:** {metrics.get('biggest_fault_line', 'N/A')}")

        deadlocks = metrics.get("deadlock_scenarios", [])
        if deadlocks:
            st.warning(f"Deadlock in {len(deadlocks)} scenario(s):")
            for t in deadlocks:
                st.write(f"  ⚠️ {t}")

        groupthink = metrics.get("groupthink_warning", [])
        if groupthink:
            st.warning(f"Groupthink — no dissent in {len(groupthink)} scenario(s):")
            for t in groupthink:
                st.write(f"  ⚠️ {t}")

    with col_b:
        st.subheader("Role Influence")
        st.caption("% of the time each role's vote matched the final outcome")
        influence = metrics.get("role_influence", {})
        for role, pct in sorted(influence.items(), key=lambda x: -x[1]):
            color = ROLE_COLORS.get(role, "#888")
            st.markdown(
                f"<div style='display:flex; align-items:center; margin-bottom:10px;'>"
                f"<span style='width:70px'>{ROLE_EMOJI.get(role,'')} {role}</span>"
                f"<div style='flex:1; background:#eee; border-radius:4px; height:22px; margin:0 10px;'>"
                f"<div style='width:{pct}%; background:{color}; height:100%; border-radius:4px;'></div></div>"
                f"<span style='width:36px; text-align:right'>{pct}%</span></div>",
                unsafe_allow_html=True
            )

        st.subheader("Decision Velocity")
        st.caption("Avg rounds to reach decision by scenario category")
        velocity = metrics.get("decision_velocity", {})
        for cat, avg in sorted(velocity.items(), key=lambda x: x[1]):
            st.write(f"  **{cat.title()}:** {avg} rounds avg")

    st.divider()
    with st.expander("Raw Report Text"):
        st.text(format_report(metrics))

    if st.button("Clear Session Results"):
        st.session_state.simulation_results = []
        st.session_state.current_transcript = None
        st.rerun()


def main():
    team_code = render_team_code_gate()

    if not team_code:
        st.title("🏢 Startup HQ")
        st.write("Enter a **Team Code** in the sidebar to get started.")
        st.info(
            "**How it works:**\n\n"
            "1. Create a team code (anything you like, e.g. `ROCKETSHIP42`)\n"
            "2. Share the code + this URL with your team\n"
            "3. Each person enters the code, picks their role, fills the questionnaire\n"
            "4. Once the team is set up, run scenarios to simulate your company's decision-making\n"
            "5. See the Team Dynamics Report to understand how well your team works together"
        )
        return

    tab1, tab2, tab3, tab4 = st.tabs([
        "Team Setup",
        "Run Simulation",
        "Debate Transcript",
        "Team Report"
    ])

    with tab1:
        render_team_setup(team_code)
    with tab2:
        render_simulation(team_code)
    with tab3:
        render_results()
    with tab4:
        render_team_report()


if __name__ == "__main__":
    main()
