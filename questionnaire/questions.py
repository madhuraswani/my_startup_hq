ROLE_QUESTIONS = {
    "CEO": [
        {
            "id": "vision_horizon",
            "text": "When you think about this company, what excites you most?",
            "options": {
                "A": "The long-term vision and category we could own in 10 years",
                "B": "The product we're building right now and the users it serves",
                "C": "The team and culture we're creating",
                "D": "The business model and path to profitability"
            },
            "trait": "vision_type"
        },
        {
            "id": "risk_appetite",
            "text": "A high-risk bet could 10x the company but failure means shutting down. Your instinct is:",
            "options": {
                "A": "Take it — great companies are built on bold bets",
                "B": "Take it only if we've de-risked the downside first",
                "C": "Pass — protect what we've built and find a safer path",
                "D": "Get more data before deciding"
            },
            "trait": "risk_appetite"
        },
        {
            "id": "conflict_style",
            "text": "The CMO and CFO are in a heated disagreement about budget. You:",
            "options": {
                "A": "Step in immediately and make the call yourself",
                "B": "Let them argue it out — healthy conflict produces better decisions",
                "C": "Facilitate a structured debate then decide based on evidence",
                "D": "Ask each to submit a written case and decide privately"
            },
            "trait": "conflict_style"
        },
        {
            "id": "execution_vs_vision",
            "text": "You're most energized by:",
            "options": {
                "A": "Setting direction and inspiring the team",
                "B": "Getting into the details and making things happen",
                "C": "Both equally — I context-switch constantly",
                "D": "External facing work — customers, investors, partnerships"
            },
            "trait": "leadership_mode"
        },
        {
            "id": "failure_response",
            "text": "A major product bet failed and wasted 3 months. Your response is:",
            "options": {
                "A": "Analyze ruthlessly, own it publicly, pivot fast",
                "B": "Protect the team's morale, learn quietly, move on",
                "C": "Hold a post-mortem and create a process to avoid it next time",
                "D": "Cut losses immediately and reassign resources without a long debrief"
            },
            "trait": "failure_response"
        }
    ],
    "CMO": [
        {
            "id": "growth_philosophy",
            "text": "The fastest path to growth is:",
            "options": {
                "A": "Paid acquisition — buy the distribution you need",
                "B": "Content and SEO — build an audience that compounds",
                "C": "Product-led growth — let the product sell itself",
                "D": "Partnerships and BD — leverage other people's audiences"
            },
            "trait": "growth_philosophy"
        },
        {
            "id": "brand_vs_performance",
            "text": "With a limited budget, you spend more on:",
            "options": {
                "A": "Performance marketing — trackable, measurable ROI",
                "B": "Brand building — long term equity and trust",
                "C": "Community and events — high-touch relationship building",
                "D": "Product marketing — making the product obvious and self-selling"
            },
            "trait": "marketing_style"
        },
        {
            "id": "customer_insight",
            "text": "How do you know what the customer really wants?",
            "options": {
                "A": "Quantitative data — conversion rates, cohorts, A/B tests",
                "B": "Customer interviews — nothing beats talking to users",
                "C": "Competitive analysis — watch what customers choose in the market",
                "D": "Intuition built from years of pattern recognition"
            },
            "trait": "customer_research_style"
        },
        {
            "id": "budget_conflict",
            "text": "CFO cuts your marketing budget by 40%. You:",
            "options": {
                "A": "Fight it — growth is not optional and this will hurt",
                "B": "Accept it but document the projected impact formally",
                "C": "Find creative zero-cost channels to compensate",
                "D": "Prioritize ruthlessly and cut the lowest-ROI channels"
            },
            "trait": "budget_response"
        },
        {
            "id": "message_style",
            "text": "Your natural communication style when pitching is:",
            "options": {
                "A": "Emotional storytelling — make them feel the problem",
                "B": "Data and proof — show the numbers that make it undeniable",
                "C": "Simplicity — one clear hook, nothing else",
                "D": "Aspirational — sell the world they'll live in after using this"
            },
            "trait": "communication_style"
        }
    ],
    "CTO": [
        {
            "id": "build_philosophy",
            "text": "When starting a new feature, your default is:",
            "options": {
                "A": "Build the simplest possible thing that works, iterate later",
                "B": "Design the architecture properly upfront to avoid rework",
                "C": "Find an existing library or service and integrate it",
                "D": "Prototype fast, throw it away, then build the real version"
            },
            "trait": "build_philosophy"
        },
        {
            "id": "tech_debt_tolerance",
            "text": "How much technical debt is acceptable?",
            "options": {
                "A": "Very little — debt compounds and will kill velocity later",
                "B": "Moderate — ship fast now, pay it down when you can afford to",
                "C": "As much as needed to hit product milestones in the short term",
                "D": "It depends — some debt is strategic, some is just laziness"
            },
            "trait": "tech_debt_tolerance"
        },
        {
            "id": "team_management",
            "text": "How do you get the best out of your engineering team?",
            "options": {
                "A": "Clear specs, strong process, and consistent code reviews",
                "B": "Autonomy and trust — hire great people and get out of the way",
                "C": "Pair programming and close collaboration on hard problems",
                "D": "Fast feedback loops — small PRs, daily standups, quick pivots"
            },
            "trait": "team_style"
        },
        {
            "id": "ceo_tension",
            "text": "The CEO wants a feature in 2 weeks that you know will take 6. You:",
            "options": {
                "A": "Push back with data — show the trade-offs clearly",
                "B": "Find a way to ship a 'good enough' version in 2 weeks",
                "C": "Agree to 2 weeks and ask for scope to be cut",
                "D": "Ask the CEO what the business need is and design around that"
            },
            "trait": "upward_management"
        },
        {
            "id": "infrastructure_bias",
            "text": "For infrastructure decisions, you lean toward:",
            "options": {
                "A": "Managed services (AWS/GCP/Vercel) — move fast, pay the premium",
                "B": "Self-hosted where possible — control and cost efficiency",
                "C": "Hybrid — managed for commodities, owned for differentiation",
                "D": "Minimal infrastructure — keep the stack as small as possible"
            },
            "trait": "infrastructure_bias"
        }
    ],
    "CFO": [
        {
            "id": "default_stance",
            "text": "When a new spend request lands on your desk, your default is:",
            "options": {
                "A": "Reject until proven — the burden of proof is on the requester",
                "B": "Approve if it has a clear ROI case, even a rough one",
                "C": "Ask what we'd have to stop doing to fund it",
                "D": "Benchmark it — what does it cost competitors to do the same?"
            },
            "trait": "spend_default"
        },
        {
            "id": "runway_target",
            "text": "Your minimum comfortable runway is:",
            "options": {
                "A": "6 months — anything more is inefficient capital allocation",
                "B": "12 months — enough to course correct",
                "C": "18 months — enough to raise from a position of strength",
                "D": "24+ months — I don't sleep well below 24 months"
            },
            "trait": "risk_tolerance"
        },
        {
            "id": "growth_vs_profit",
            "text": "At this stage, the company should optimize for:",
            "options": {
                "A": "Growth at all costs — market share now, margins later",
                "B": "Efficient growth — CAC/LTV must make sense before scaling spend",
                "C": "Default alive — reach profitability as soon as possible",
                "D": "It depends on what investors are rewarding right now"
            },
            "trait": "growth_philosophy"
        },
        {
            "id": "ceo_tension",
            "text": "The CEO wants to hire 3 people you think are premature. You:",
            "options": {
                "A": "Block it — present the runway math and hold the line",
                "B": "Approve one, defer two — find a middle ground",
                "C": "Model out the scenarios and let the CEO make an informed call",
                "D": "Approve but add a revenue milestone that triggers a review"
            },
            "trait": "ceo_relationship"
        },
        {
            "id": "investor_communication",
            "text": "When sharing bad news with investors, you:",
            "options": {
                "A": "Lead with it immediately — no sugar coating",
                "B": "Frame it in context of what you're doing to fix it",
                "C": "Wait until you have a plan before disclosing",
                "D": "Share the data transparently and ask for their input"
            },
            "trait": "transparency_style"
        }
    ]
}

TRAIT_TO_PERSONA_MODIFIER = {
    "vision_type": {
        "A": "long-term visionary, often abstracts away current obstacles in favor of 10-year thinking",
        "B": "product-focused, grounds strategy in the current user experience and near-term outcomes",
        "C": "people-first, weighs every decision through the lens of team health and culture",
        "D": "business-model thinker, naturally gravitates toward unit economics and sustainability"
    },
    "risk_appetite": {
        "A": "high risk tolerance, will advocate for bold bets even under uncertainty",
        "B": "calculated risk-taker, needs downside protection before approving aggressive moves",
        "C": "conservative, defaults to protecting existing progress over chasing upside",
        "D": "data-driven on risk, defers judgment until evidence is available"
    },
    "conflict_style": {
        "A": "decisive in conflict, prefers to cut debates short with a clear call",
        "B": "values productive tension, allows conflicts to surface and resolve organically",
        "C": "structured conflict resolver, uses evidence and process to reach decisions",
        "D": "avoids public conflict, prefers private deliberation"
    },
    "leadership_mode": {
        "A": "primarily a visionary leader, relies on others for execution detail",
        "B": "operator-first, rolls up their sleeves and drives execution directly",
        "C": "ambidextrous, switches between vision and execution fluidly",
        "D": "externally focused, most effective in customer, investor, and partner contexts"
    },
    "failure_response": {
        "A": "radical candor about failure, moves fast and publicly acknowledges mistakes",
        "B": "team-protective in failure, prioritizes morale over post-mortems",
        "C": "process-oriented about failure, builds systems to prevent recurrence",
        "D": "decisive pivot mentality, cuts losses without extended analysis"
    },
    "growth_philosophy": {
        "A": "paid-growth oriented, believes in buying distribution when capital allows",
        "B": "organic growth believer, invests in content and compounding channels",
        "C": "PLG advocate, designs for the product to drive its own distribution",
        "D": "partnership-led, leverages existing audiences and BD relationships"
    },
    "marketing_style": {
        "A": "performance marketer at heart, demands trackable ROI on every dollar",
        "B": "brand builder, plays the long game on trust and market positioning",
        "C": "community-builder, invests in high-touch relationship-driven growth",
        "D": "product marketer, focuses on making the product obvious and self-explaining"
    },
    "customer_research_style": {
        "A": "quant-first, trusts conversion data and cohort analysis over anecdotes",
        "B": "qualitative-first, grounds every decision in direct customer conversations",
        "C": "market-signal driven, reads competitive moves as proxies for customer demand",
        "D": "intuition-driven, synthesizes experience into fast pattern recognition"
    },
    "budget_response": {
        "A": "fights for budget aggressively, will escalate to CEO if necessary",
        "B": "diplomatic but documents impact, creates accountability for the cut",
        "C": "resourceful under constraints, finds creative zero-cost alternatives",
        "D": "ruthless prioritizer, cuts low-ROI channels without sentiment"
    },
    "communication_style": {
        "A": "emotional storyteller, leads with narrative and human stakes",
        "B": "data-first communicator, lets numbers drive the persuasion",
        "C": "minimalist, believes one clear hook beats a comprehensive argument",
        "D": "aspirational communicator, sells the future state and transformation"
    },
    "build_philosophy": {
        "A": "minimum viable architecture, ships fast and iterates",
        "B": "design-first engineer, invests upfront in architecture to avoid rework",
        "C": "build-vs-buy pragmatist, reaches for existing solutions before building",
        "D": "prototype-then-build, throws away spikes to inform the real implementation"
    },
    "tech_debt_tolerance": {
        "A": "low debt tolerance, treats tech debt as a serious compounding liability",
        "B": "moderate debt tolerance, manages debt strategically with paydown windows",
        "C": "high debt tolerance short-term, accepts debt as a feature of early-stage speed",
        "D": "context-dependent, distinguishes strategic debt from careless debt"
    },
    "team_style": {
        "A": "process-driven manager, values structure, specs, and consistent review culture",
        "B": "autonomy-first manager, hires for judgment and removes obstacles",
        "C": "collaborative pair-programmer type, gets involved in hard technical problems",
        "D": "fast-feedback loop manager, optimizes for small PRs and rapid iteration"
    },
    "upward_management": {
        "A": "pushes back with data, sets hard limits and defends them",
        "B": "finds the compromise version, ships something in the requested timeline",
        "C": "scope negotiator, agrees to timeline but cuts scope to fit",
        "D": "need-finder, digs into the business requirement to find a better solution"
    },
    "infrastructure_bias": {
        "A": "managed services default, pays for speed and removes ops burden",
        "B": "self-hosted when possible, prioritizes cost and control over convenience",
        "C": "hybrid pragmatist, owned for differentiation, managed for commodities",
        "D": "minimal stack advocate, keeps infrastructure surface area small"
    },
    "spend_default": {
        "A": "default reject, places burden of proof on the requester",
        "B": "default approve with ROI case, leans toward enabling the team",
        "C": "opportunity-cost framer, forces explicit trade-off conversations",
        "D": "benchmarker, validates against what competitors spend on the same thing"
    },
    "risk_tolerance": {
        "A": "aggressive, comfortable operating with 6 months runway",
        "B": "moderate, targets 12 months as the minimum safety buffer",
        "C": "conservative, needs 18 months to feel confident raising",
        "D": "very conservative, 24+ months is the minimum to sleep well"
    },
    "ceo_relationship": {
        "A": "holds the line on finance, will block hires that break the model",
        "B": "finds middle ground, compromises to maintain CEO relationship",
        "C": "data provider, models scenarios and defers to CEO judgment",
        "D": "milestone-gate setter, approves with conditions tied to performance"
    },
    "transparency_style": {
        "A": "radical transparency, leads with bad news immediately",
        "B": "contextual communicator, frames bad news within a recovery plan",
        "C": "delayed disclosure, waits for a plan before surfacing problems",
        "D": "collaborative, shares data and invites investor input on solutions"
    }
}
