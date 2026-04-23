# CTO Technical Feasibility Study: Proposal 01 — EdgeBot Tutor

**Date:** 2026-04-09
**Analyst:** CTO (The Engineering Architect)
**Status:** Analysis Only — No Vote

---

## 1. Hardware Feasibility

### Recommended Platform: ESP32-S3

The ESP32-S3 is the correct chip for this project. Specs relevant to ML inference:

- Xtensa LX7 dual-core @ 240 MHz
- 512 KB internal SRAM
- Up to 8 MB external PSRAM (via SPI, ~80 MHz access, ~10–20× slower than internal SRAM)
- 16 MB Flash (typical dev board)
- Vector extension instructions (PIE) — limited SIMD for ML, not a true NPU
- BOM contribution: ~$3–5 chip cost, ~$8–12 for a complete module with antenna

**Drop the RP2040 from the proposal immediately.** The RP2040 has only 264 KB SRAM, no FPU (Cortex-M0+), and no native ML acceleration. It cannot run any meaningful inference workload without an external accelerator, which blows the BOM target. It does not belong in this proposal.

### Sensor Suite

The proposed sensors (IMU, IR, ultrasonic, encoder) are all commodity I2C/UART peripherals. BOM contribution is predictable, sourcing is reliable. No concerns.

### OLED + Speaker

Feasible. Small SSD1306 OLED (~$1) and a PWM-driven passive buzzer (~$0.10) keep BOM lean. A DAC + small speaker (~$0.50–$1.50) is acceptable if voice feedback is desired. This is not a bottleneck.

### BOM Realism at <$35

Achievable at prototype scale with dev boards — **not** achievable in production without a custom PCB and a minimum run of 500–1,000 units. At prototype (1–10 units), BOM will run $50–70. The sub-$35 target is a volume-pricing claim, not a Day 1 fact. The CFO should note this in their own analysis.

---

## 2. The AI Model — The Most Critical Technical Risk in This Proposal

This section contains the most important finding in this document. **The "~50M parameter" figure in the proposal is not achievable on the proposed hardware.** This must be corrected before any engineering work begins.

### Memory Budget Reality Check

| Model Size | Precision | Weight Memory | Fits on ESP32-S3? |
|---|---|---|---|
| 50M params | INT8 | ~50 MB | No (8 MB PSRAM max) |
| 50M params | INT4 | ~25 MB | No |
| 10M params | INT8 | ~10 MB | No (leaves zero room for activations/runtime) |
| 5M params | INT8 | ~5 MB | Marginal — PSRAM only, tight |
| 2M params | INT8 | ~2 MB | Feasible with PSRAM; slow inference |
| 500K params | INT8 | ~500 KB | **Yes — fits in internal SRAM with headroom** |
| 200K params | INT8 | ~200 KB | Yes — fast, ample headroom |

**The correct target for Phase 1 is ≤ 500K parameters, INT8 quantized.** This is not a limitation to apologize for — at this size, inference latency comfortably hits the <200 ms target on the LX7 core.

### The Language vs. Classification Distinction — A Fundamental Architecture Decision

The proposal describes a "language + classification micro-model." These are two completely different problems. The hardware can support one of them, not both.

**Classification (Fully Feasible on ESP32-S3):**
- Error pattern detection: "Student's PWM duty cycle is consistently off by 2×"
- Competency assessment: pass/fail on demonstrated skills
- Lesson difficulty adaptation: adjust next task based on error history vector
- All of this is achievable with a 100K–500K parameter classifier

**Generative language output (NOT feasible on ESP32-S3):**
- The smallest LLM capable of coherent tutoring dialogue is ~125M parameters (GPT-2 Small)
- At INT4 quantization: ~62 MB — 7× the available PSRAM
- Current state-of-the-art tiny LLMs (Phi-3 mini at 3.8B, Llama 3.2 at 1B) require 500 MB–4 GB — not even close
- There is no path to generative language on this hardware in this decade

**Architectural recommendation for Phase 1:**
Use a classification model to detect the error category (e.g., 20–50 error classes), then drive a finite-state machine that selects from a library of pre-authored, templated tutor responses stored in Flash. This is the architecturally correct solution. It is also the pedagogically correct one — structured, curated tutor responses are more reliable than stochastic generation for K-12 learners.

This is not a compromise. It is the right design. The "AI" does the hard part (pattern recognition from sensor + code state); the tutor response is deterministic lookup. This distinction must be explicit in the product spec.

---

## 3. Model Training Pipeline

The model is the product. Its quality determines whether students learn. Training deserves as much engineering attention as the hardware.

### Training Data — The Hardest Problem

There is no public dataset of robotics debugging sessions. This must be synthesized or collected from scratch. Options:

1. **Simulation-based synthetic data (recommended for Phase 1):** Simulate motor control, PWM, and sensor scenarios in software; inject known error classes; use the resulting (input, error_label) pairs as training data. This is automatable and scalable.
2. **Human annotation of real sessions (Phase 2):** Capture real learner sessions from pilots; label error patterns; fine-tune on real data. Requires an annotation pipeline.
3. **Transfer learning:** Pre-train on general signal/time-series datasets, fine-tune on robotics-specific errors. Can reduce the synthetic data requirement.

**Blocking item:** The training data strategy must be defined and partially executed before Week 8. You cannot train a model in the last two days of the sprint.

### Quantization Strategy

Post-training quantization (PTQ) alone often degrades small model accuracy significantly because there is no headroom to absorb precision loss. **Quantization-aware training (QAT) is required.** This means the quantization constraints must be baked into the training loop from the start, not applied as a post-processing step. Factor this into the model development schedule.

### Inference Runtime

Use **TensorFlow Lite Micro (TFLM)** as the inference engine. It is the most mature, ESP32-S3-compatible, actively maintained runtime for microcontrollers. It compiles to ~50 KB of Flash. ONNX Runtime Micro is an alternative but has less community support for Xtensa. Do not roll a custom inference engine.

---

## 4. Software Stack Assessment

### Student-Facing Code Layer: MicroPython

MicroPython is the correct choice for student code authoring — it is readable, forgiving, and familiar to learners with Python experience. However, there are two constraints to engineer around:

1. **Memory overhead:** The MicroPython interpreter itself consumes ~200–300 KB of SRAM. This must be budgeted against the inference model's SRAM use. On ESP32-S3 with internal SRAM only, this is tight. PSRAM offloading for model weights is the solution.
2. **Sandboxing:** MicroPython provides no process isolation. A student's infinite loop or bad memory access can hang or crash the device. Mitigation: implement a watchdog timer (WDT) with an enforced execution timeout on student code runs. This is a single-line hardware register write in the firmware — not complex, but it must be explicitly designed in.

### Inference Layer: C++ / TFLite Micro

All inference must run in the firmware's C++ layer, not in MicroPython. Expose a clean API to MicroPython via the `umodule` system (e.g., `import tutor; tutor.classify(sensor_state, code_state)`). This is a standard ESP-IDF pattern.

### Curriculum Engine (DAG)

The DAG curriculum graph is architecturally sound but over-engineered for Phase 1. A linear, sequential lesson path (3 modules, fixed order) is sufficient for the prototype. Implement the DAG as Phase 2 when the lesson library justifies non-linear traversal. Store curriculum state in Flash (NVS partition) so progress survives a power cycle.

### Connectivity and OTA Updates

The proposal is ambiguous about how firmware updates are delivered if Wi-Fi is not required. This must be resolved. Options:

| Method | Pros | Cons |
|---|---|---|
| USB (default) | Always available, fast, no pairing | Requires laptop at update time |
| BLE OTA | Wireless, works from phone app | Slower, needs OTA app development |
| Wi-Fi (optional) | Fastest, fully automated | Contradicts "no cloud" narrative |

**Recommendation for Phase 1:** USB OTA only. It is zero-cost to implement (ESP-IDF bootloader supports this natively), requires no app development, and keeps the firmware update story honest. Add BLE OTA in Phase 2 if the market demands it.

### Teacher Dashboard

This is a web UI against a local or cloud backend. It is decoupled from the on-device experience. No technical objections. **Flag:** dashboard data requires the device to sync somehow (USB, BLE, or Wi-Fi). The sync mechanism must be specified. Do not design the dashboard until the sync protocol is locked.

---

## 5. Development Timeline Assessment

### Week 8 Prototype Feasibility

| Deliverable | Estimated Effort | Feasibility |
|---|---|---|
| ESP32-S3 dev board bring-up + sensor wiring | 1 week | Straightforward |
| Inference runtime (TFLM) integration | 1 week | Standard, well-documented |
| Synthetic training data generation (500–2K samples) | 1–2 weeks | **Critical path — start Day 1** |
| Classifier model training + QAT + deployment | 1–2 weeks | Depends on data readiness |
| MicroPython SDK + watchdog integration | 1 week | Parallelizable with hardware work |
| 3 linear lesson modules (content authoring) | 1–2 weeks | Parallelizable |
| OLED/speaker feedback integration | 0.5 weeks | Simple peripheral work |

**Total: 7–9 weeks of single-engineer work at realistic pace.**

Week 8 is achievable **if and only if:**
1. Training data generation begins in Week 1 (not Week 5)
2. The model is scoped to classification + templated responses (not language generation)
3. The curriculum engine is a linear state machine, not a DAG
4. The teacher dashboard is deferred out of the prototype scope

If any of these conditions are not met, the timeline slips to Week 10–12.

---

## 6. Technical Risk Register

| Risk | Severity | Probability | Mitigation |
|---|---|---|---|
| **Model parameter budget mismatch (50M params on ESP32-S3)** | Critical | Certain if not corrected | Redesign to ≤500K params INT8 immediately |
| **Language generation assumption in tutor behavior** | Critical | High if not clarified | Commit to classification + template architecture in product spec |
| **Training data scarcity for robotics error classification** | High | High | Begin synthetic data generation in Week 1; simulation pipeline is non-negotiable |
| **QAT not planned; PTQ accuracy degradation** | High | Medium | Mandate QAT from the start of model development |
| **MicroPython watchdog not implemented; student code crashes device** | Medium | High (students will write infinite loops) | WDT enforcement is a Day 1 firmware requirement |
| **OTA update mechanism undefined** | Medium | Certain if not addressed | Default to USB OTA; document explicitly |
| **BOM target not achievable at prototype volumes** | Low | Certain | Accepted — prototype BOM is $50–70; production BOM is the <$35 target |
| **ESP32-S3 supply chain disruption** | Low | Low | Commodity chip; multiple distributors (Mouser, LCSC, Digi-Key) |

---

## 7. What the Proposal Gets Right (Technically)

- **ESP32-S3 as the primary platform.** Correct call. It has the best ML support in its price tier.
- **INT4/INT8 quantization as the deployment strategy.** Correct framing. QAT is the missing detail.
- **On-device inference eliminates cloud dependency.** Architecturally sound and a genuine differentiator.
- **Commodity chip selection (ESP32-S3 widely available).** Reduces supply chain risk. Good engineering judgment.
- **Sensor suite selection (IMU, IR, ultrasonic, encoder).** Appropriate for a beginner robotics curriculum. All are I2C/UART addressable, no custom drivers needed.
- **MicroPython for student-facing code.** Right choice for the target learner age group.
- **Pilot-first data collection.** Pilot usage will generate real error pattern data for model iteration — this is the correct feedback loop.

---

## 8. Phase 1 Architecture Specification (Recommended)

To summarize the actionable decisions that must be locked before engineering begins:

| Decision | Recommendation |
|---|---|
| Hardware platform | ESP32-S3-WROOM-1 with 8 MB PSRAM (drop RP2040) |
| Model architecture | Classifier, ≤500K params, INT8, QAT-trained, deployed via TFLM |
| Tutor behavior | FSM + templated response library (no language generation) |
| Inference runtime | TensorFlow Lite Micro |
| Student code layer | MicroPython + WDT-enforced execution timeout |
| Curriculum engine | Linear state machine (3 modules for prototype; DAG is Phase 2) |
| OTA update method | USB only for Phase 1 |
| Dashboard sync | Deferred to Phase 2 |
| Training data strategy | Simulation-based synthetic data; begin Week 1 |

---

## Summary

The core technical thesis — on-device, quantized AI for adaptive robotics tutoring — is sound and feasible. The hardware platform choice is correct. The BOM target is achievable at production scale.

However, the proposal contains one critical technical error that must be corrected before any engineering begins: **the "~50M parameter" model does not fit on the ESP32-S3, and the "language + classification" framing conflates two fundamentally different problems.** Reframing the AI tutor as a classification model driving templated responses resolves both issues and produces a better, more reliable product.

The Week 8 prototype timeline is achievable with correct scoping. The critical path is training data, not hardware.

*Vote: Withheld. Contingent on revision of model architecture specification in the proposal.*
