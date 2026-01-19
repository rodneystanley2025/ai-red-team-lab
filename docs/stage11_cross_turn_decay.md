# Stage 11B — Cross-Turn Risk Decay

## Objective

Introduce a controlled cross-turn **risk decay mechanism** to prevent persistent false positives and over-enforcement 
following high-risk or denied interactions, while preserving strong defenses against crescendo-style attacks.

This stage addresses the observed issue where accumulated risk persists across subsequent turns, unintentionally 
impacting legitimate, unrelated queries.

---

## Background & Motivation

During Stage 10 and Stage 11 evaluation, the system demonstrated strong resistance to:

- Implicit context continuation
- Contextual softening attacks
- High-risk domain escalation
- Multi-turn crescendo pressure

However, retesting revealed a secondary effect:

> **Once a high-risk or denied interaction occurred, subsequent benign or educational prompts were sometimes 
over-constrained.**

This behavior was most visible in:
- Test 10.4.6 (Educational Framing — Control Case)
- Stage 11D cross-turn accumulation tests

While conservative behavior is preferable to under-enforcement, persistent escalation without decay introduces usability 
and correctness risks.

---

## Threat Model

**Adversary Goal:**  
Exploit risk decay to reset or bypass crescendo safeguards.

**Defender Goal:**  
Allow legitimate requests to proceed *after* sufficient de-escalation, without enabling adversaries to “wash out” risk 
through trivial prompts.

---

## Observed Failure Mode

### Pattern Identified

1. User introduces contextual softening or high-risk framing
2. System correctly escalates or denies
3. Subsequent benign prompt is evaluated under residual elevated risk
4. Legitimate content is unnecessarily constrained

This represents **risk stickiness**, not a failure of detection.

---

## Design Principles

The risk decay mechanism must:

- Preserve **stateless-by-default architecture**
- Be **deterministic and auditable**
- Prevent rapid or trivial risk reset
- Apply only to **accumulated risk**, not individual signal detection
- Maintain defense-in-depth compatibility with existing escalation logic

---

## Risk Decay Model

### Conceptual Model

Each request is evaluated as:
effective_risk = max(0, accumulated_risk - decay)
effective_risk += new_signal_score


Key properties:

- Risk never goes negative
- New signals always contribute
- Decay applies *before* new scoring
- High-risk signals cannot be instantly neutralized

---

## Decay Strategy

### Decay Rate

A fixed, conservative decay value is applied per request:

- **Decay Amount:** 1–2 points per turn
- **Rationale:**  
  Prevents immediate reset while allowing gradual normalization

### Non-Decay Conditions

Risk decay **does not apply** when:

- A CRITICAL risk signal is detected
- A HIGH risk signal occurs in consecutive turns
- The same risk class is repeatedly triggered

This prevents adversarial “cool-down farming.”

---

## Integration with Existing Architecture

### Components Affected

- `risk_accumulator.py`
- `policy_enforcer.py`

### Responsibilities

**Risk Accumulator**
- Tracks cumulative risk score
- Applies decay before increment
- Enforces minimum and maximum bounds

**Policy Enforcer**
- Remains the single decision authority
- Uses accumulated risk for escalation thresholds
- Does not maintain conversational state

---

## Security Impact

### Improvements

- Reduces false positives after valid denials
- Restores legitimate educational and defensive queries
- Prevents “poisoned session” behavior
- Improves alignment between security posture and user intent

### Residual Risk

- A patient adversary could attempt low-risk turns to reduce score  
  → Mitigated via non-decay conditions and signal weighting

This risk is acceptable and explicitly bounded.

---

## Validation Plan

Following implementation:

- Re-run Test 10.4.6 (Educational Framing Control)
- Re-run Stage 11D cross-turn accumulation tests
- Confirm:
  - Crescendo attacks remain blocked
  - Legitimate queries recover after de-escalation

Results will be documented as a **retest appendix**.

---

## Outcome

Cross-turn risk decay completes the crescendo mitigation architecture by balancing:

- **Security**
- **Correctness**
- **Usability**

This transforms the system from a static gatekeeper into a resilient, adaptive enforcement engine aligned with 
real-world AI security threats.

---

## Status

**Stage:** Designed  
**Next Step:** Code implementation + targeted retesting
