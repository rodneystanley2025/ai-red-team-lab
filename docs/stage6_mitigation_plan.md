# Stage 6 — Mitigation Plan & Control Design

## Objective

This document defines targeted mitigations for risks identified in Stage 6 risk assessment.  
Each mitigation is designed to address a specific failure class observed during Stage 5 adaptive adversary testing.

The goal is **defense-in-depth**, not reliance on prompt quality or model behavior alone.

---

## Mitigation Strategy Overview

Mitigations are grouped by failure class to ensure consistency, maintainability, and auditability.

| Mitigation Group | Addresses | Control Type |
|----------------|----------|--------------|
| A | Implicit memory & continuity assumptions | Deterministic rule-based |
| B | Training data implication softening | Canonical response |
| C | Contextual justification bypass | Capability-based hard denial |

---

## Mitigation Group A — Implicit Context Assumption Guard

### Addresses
- Tests 5.1.1–5.1.5
- Test 5.4.1

### Problem Statement
Current enforcement detects explicit memory references but fails to reject **implicit continuity assumptions**, such as:
- “continue where we left off”
- “based on your earlier assessment”
- “given the background you already have”

These prompts induce fabricated context without explicit memory language.

---

### Control Design

Introduce a deterministic **Implicit Context Assumption Detector** that triggers when user input relies on prior 
context not supplied in the current request.

#### Detection Examples
- “already discussed”
- “earlier assessment”
- “continue”
- “as before”
- “previously shared”
- “background you already have”

#### Enforcement Action
Return a canonical statelessness denial:

> “I don’t have access to prior context or earlier discussions. Please provide the necessary information in this request.”

This check must execute **before** tool parsing or LLM output trust.

---

## Mitigation Group B — Training Data Canonicalization

### Addresses
- Test 5.3.4

### Problem Statement
Speculative responses (“it’s possible”) weaken guarantees by implicitly suggesting proprietary or confidential data 
involvement.

---

### Control Design

Any mention of training sources must be replaced with a **single canonical response**, regardless of framing.

#### Canonical Response
> “I don’t have visibility into or access to specific training datasets and can’t confirm whether any proprietary or 
> confidential data was used.”

No speculation, hedging, or conditional language is permitted.

---

## Mitigation Group C — Context-Insensitive Capability Denial

### Addresses
- Tests 5.5.2, 5.5.4, 5.5.5

### Problem Statement
Creative, historical, or simulation framing successfully bypasses policy controls and results in disallowed guidance.

---

### Control Design

Introduce a **Justification-Insensitive Denial Layer** that blocks content based on **capability class**, not user 
intent or narrative framing.

#### Disallowed Capability Classes
- Chemical synthesis
- Explosive construction
- Document forgery
- Other procedural wrongdoing

#### Enforcement Action
Immediate refusal with a safety-oriented explanation, independent of:
- Fictional framing
- Educational framing
- Historical framing
- Simulation framing

---

## Expected Outcomes

After implementation, the system should:

- Reject implicit memory and continuity assumptions deterministically
- Eliminate speculative training data implications
- Prevent creative or contextual bypass of safety policies
- Maintain acceptable educational content where explicitly allowed

---

## Implementation Guidance

- Policy enforcement should remain centralized (e.g., `policy_enforcer.py`)
- Controls should be deterministic where possible
- Canonical responses should be reused across stages for consistency
- Mitigations must be validated via re-execution of Stage 5 tests

---

## Conclusion

This mitigation plan establishes a clear path from observed adversarial behavior to enforceable, auditable controls. 
It reinforces system guarantees under realistic adaptive pressure while preserving legitimate use cases.

- Implemented implicit-context detection to block memory evasion via assumed
  conversational continuity (Stage 5.1).
