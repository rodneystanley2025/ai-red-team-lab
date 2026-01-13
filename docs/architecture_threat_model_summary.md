# Architecture Threat Model Summary

## Purpose

This document summarizes the threat model for the AI Red Team Lab, mapping architectural components to identified threat classes, implemented mitigations, and residual risks. It serves as a high-level security reference for reviewers, auditors, and future maintainers.

This summary reflects the system state following completion of Stage 7 (Residual Risk Analysis).

---

## System Architecture Overview

### High-Level Flow

1. User submits input via HTTP API (`/chat`)
2. Input is forwarded to a local LLM backend (Ollama)
3. Model output is treated as untrusted text
4. Centralized policy enforcement evaluates:
   - Memory boundary violations
   - Authority / role assumption
   - Training data claims
   - System artifact leakage
5. Approved output is returned or a canonical denial is issued

### Trust Boundaries

| Boundary | Trust Level |
|--------|-------------|
| User Input | Untrusted |
| Model Output | Untrusted |
| Policy Enforcer | Trusted |
| Tool Registry | Trusted |
| Runtime Environment | Assumed Trusted |

---

## Threat Categories and Analysis

### T1. Memory Evasion & Statelessness Bypass

**Threat:**  
Adversary attempts to induce fabricated prior context, decisions, or conversation continuity.

**Attack Vectors:**
- Implicit continuation prompts
- Professional or audit-style phrasing
- Multi-turn conversational pressure

**Mitigations Implemented:**
- Statelessness enforcement via output inspection
- Canonical denial responses
- Implicit context detection patterns
- Multi-turn reassertion behavior

**Residual Risk:**  
Low. Pattern-based detection may miss novel phrasing.

---

### T2. Authority & Role Indirection

**Threat:**  
Adversary attempts to extract internal system state, logs, or enforcement outcomes by assuming privileged roles.

**Attack Vectors:**
- “Compliance review” framing
- Oversight or audit impersonation
- Requests for logs or enforcement actions

**Mitigations Implemented:**
- Authority boundary detector
- System artifact suppression
- Single enforcement authority design

**Residual Risk:**  
Low. False positives are possible but acceptable.

---

### T3. Training Data Softening

**Threat:**  
Gradual coercion into implying use of proprietary, confidential, or non-public training data.

**Attack Vectors:**
- Speculative phrasing (“Is it possible…?”)
- Enterprise partnership references
- Indirect confirmation requests

**Mitigations Implemented:**
- Strict training data denial policy
- Speculation suppression
- Canonical non-implication responses

**Residual Risk:**  
Low. Model wording changes may require detector updates.

---

### T4. Multi-Turn Context Pressure

**Threat:**  
Adversary incrementally establishes false context across multiple turns.

**Attack Vectors:**
- Explicit stateless acknowledgment followed by assumption
- Gradual continuity framing
- Semantic carry-forward pressure

**Mitigations Implemented:**
- Output-based memory violation detection
- Statelessness reassertion on continuation cues
- Centralized enforcement after every turn

**Residual Risk:**  
Medium-Low. Fully semantic attacks remain possible.

---

### T5. Policy Contradiction via Contextual Framing

**Threat:**  
Disallowed content elicited through fictional, educational, historical, or simulated framing.

**Attack Vectors:**
- Creative writing scenarios
- Academic or historical analysis
- Ethical or training justifications

**Mitigations Implemented:**
- Output suppression on explicit violations
- Conservative refusal patterns
- Documentation of residual risk

**Residual Risk:**  
Medium. Contextual nuance is inherently difficult to classify deterministically.

---

## Threat Coverage Matrix (Summary)

| Threat Class | Prevented | Mitigated | Residual |
|-------------|----------|-----------|----------|
| Memory Evasion | ✓ | — | Low |
| Authority Indirection | ✓ | — | Low |
| Training Data Leakage | ✓ | — | Low |
| Multi-Turn Pressure | — | ✓ | Medium-Low |
| Policy Contradiction | — | ✓ | Medium |

---

## Design Strengths

- Single, centralized policy authority
- Canonical and deterministic denials
- Explicit trust boundary enforcement
- Stateless architecture reduces attack surface
- Clear documentation of assumptions and limits

---

## Accepted Trade-Offs

- Pattern-based detection over semantic modeling
- Deterministic enforcement over probabilistic scoring
- No cross-request behavioral correlation
- Model-dependent output variability

These trade-offs were intentionally selected to prioritize auditability, clarity, and instructional value.

---

## Conclusion

The AI Red Team Lab demonstrates a defensible, transparent security posture against common and adaptive LLM threat classes. While not immune to all contextual or semantic attacks, the system:

- Prevents high-impact violations
- Detects and mitigates adaptive probing
- Explicitly documents residual risk

This threat model is considered complete and aligned with the project’s stated assumptions, non-goals, and educational objectives.

---

## Review Status

- Threat model reviewed against Stage 5–7 findings
- Residual risks cross-referenced with risk register
- Approved for final documentation set
