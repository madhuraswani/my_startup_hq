# CFO Analysis: Proposal 01 — EdgeBot Tutor

**Date:** 2026-04-09
**Analyst:** CFO (The Pragmatic Anchor)
**Status:** Analysis Only — No Vote

---

## 1. Runway Implications

No budget figures are stated in the proposal. This is the first red flag. Before any green-light, I need:

- **Prototype cost estimate** (hardware BOM × N units + engineering hours)
- **Pilot cost** (2 free school units + logistics + support time)
- **Monthly burn rate** to reach the crowdfunding milestone

Without these numbers, the 6-month horizon is a roadmap, not a plan. The CEO has described *what* to build, not *what it costs* to build it.

---

## 2. Unit Economics (As Estimable)

**BOM target: <$35**

At that BOM, retail pricing likely needs to land at $80–120 to achieve a sustainable gross margin (~55–65%). That is a reasonable price for a K-12 STEM kit, but it is not validated. Comparable kits (Arduino Starter Kit ~$65, LEGO Mindstorms ~$360) suggest the market can bear this — but LEGO operates at scale with brand equity. We do not.

| Scenario | Retail Price | BOM | Gross Margin |
|---|---|---|---|
| Conservative | $80 | $35 | ~56% |
| Target | $100 | $30 (at volume) | ~70% |
| Risk case | $65 | $40 (low volume) | ~38% |

The 38% risk case is the one that kills us. Small production runs mean BOM doesn't fall to $30 — it likely rises above $35 due to low-volume component pricing.

---

## 3. CAC Assessment

**Phase 1 GTM relies on:**
1. Free pilot units (direct relationship, near-zero CAC)
2. Crowdfunding (platform-mediated, CAC embedded in campaign spend)
3. B2B school procurement (high-touch, long sales cycle, high CAC)

The crowdfunding path is the only near-term revenue event. Crowdfunding CAC for hardware products typically runs $15–40/backer. For a $100 kit, that is 15–40% of revenue per unit before any COGS. This is manageable only if backer volume is high enough to drive a production run that reduces BOM.

**B2B school procurement is a cash flow trap.** School districts can take 6–18 months from demo to PO. Do not count this as Phase 1 revenue. The proposal correctly notes this risk but the mitigation (sell direct-to-consumer in parallel) needs to be the *primary* channel, not a hedge.

---

## 4. LTV Considerations

The proposal has a one-time hardware model with an optional teacher dashboard. This is a weak LTV structure.

- No subscription revenue mentioned
- No consumables model (replacement parts, sensor packs)
- No content licensing or premium curriculum tiers

A single $100 unit sale with no follow-on revenue means every new customer requires full CAC spend again. The LTV:CAC ratio at launch is likely below 3:1 — the minimum threshold for a venture-backable model.

**This is the most significant fiscal gap in the proposal.** The CEO needs to define a recurring revenue layer before this is investor-ready.

---

## 5. Technical Cost Risks

The on-device AI angle is fiscally sound — it eliminates recurring cloud inference costs (which can run $0.01–0.10 per session at scale). At 500 session hours in the pilot, cloud costs would be negligible anyway, but at 500,000 sessions/year, the savings become material. This is a genuine long-term cost advantage.

However, the model development cost is not addressed:
- Quantization and hardware-specific optimization is non-trivial engineering work
- Training data for robotics task debugging must be curated — this has a real time cost
- OTA firmware update infrastructure adds backend complexity (contradicts "lean" framing)

---

## 6. Market Size — Reality Check

- "$340B EdTech by 2030" is a total addressable market figure, not a serviceable one
- STEM robotics kits is a niche within EdTech — realistically a $2–5B segment
- India/SEA beachhead is strategically sound for the on-device value proposition, but these are also the most price-sensitive buyers — margin compression risk is real

The beachhead market and the high-margin market may not be the same market.

---

## 7. Key Missing Numbers (Blocking Items)

| Missing Item | Why It Matters |
|---|---|
| Prototype budget ($ and hours) | Sets burn rate; determines runway needed |
| Crowdfunding target amount | Defines success threshold for Phase 1 |
| Minimum production run quantity | Determines if BOM of <$35 is achievable |
| Recurring revenue model | Required for LTV:CAC ratio above 3:1 |
| Founder cash/salary assumptions | Cannot assess runway without this |

---

## 8. What the Proposal Gets Right (Fiscally)

- **On-device inference = no API cost.** Strong long-term OpEx advantage.
- **Commodity hardware (ESP32-S3).** Reduces supply chain risk and keeps BOM predictable.
- **Crowdfund before mass production.** Correct sequencing — demand validation before capital commitment.
- **Lean backend claim is credible** given the founder's automation background, which reduces headcount cost to ship v1.
- **Pilot-first approach.** Free units for data is an efficient use of prototype spend.

---

## Summary

The technical thesis is sound. The fiscal thesis is incomplete. The proposal is structured as a product vision, not a financial plan. Before a funding or resource commitment decision can be made, the CFO requires a Phase 1 budget with explicit cost estimates, a defined crowdfunding target, and a proposed recurring revenue mechanism.

*Vote: Withheld pending additional financial detail.*
