# Security Assumptions and Non-Goals

This document defines the assumptions under which the AI Red Team Lab’s
security controls are designed to operate, as well as explicit non-goals
that are intentionally excluded from scope.

These statements establish the boundaries of responsibility and prevent
misinterpretation of security guarantees.

---

## 1. Security Assumptions

### 1.1 Trusted Execution Environment

The system assumes:
- The application runtime is not compromised
- Source code integrity is preserved
- The enforcement layer is executed as designed

Attacks against the host environment, operating system, or runtime
infrastructure are out of scope.

---

### 1.2 Deterministic Policy Enforcement

Security guarantees assume:
- Policy enforcement is applied consistently to all requests
- Enforcement logic cannot be bypassed or reordered at runtime
- All model outputs pass through the policy enforcer before being returned

Any failure to invoke enforcement invalidates downstream protections.

---

### 1.3 Honest Integration Boundaries

The system assumes:
- External services do not modify inputs or outputs post-enforcement
- No downstream consumer removes or alters safety responses
- API clients do not suppress denial or warning messages

---

### 1.4 Single-Request Evaluation Model

The system assumes:
- Each request is evaluated independently
- No persistent conversational state is retained
- No cross-request identity linkage exists

Security controls are calibrated for stateless operation by design.

---

## 2. Explicit Non-Goals

### 2.1 Perfect Intent Classification

The system does not attempt to:
- Accurately infer user intent
- Distinguish benign curiosity from malicious planning
- Perform psychological or behavioral profiling

Risk scoring reflects probabilistic indicators, not definitive intent.

---

### 2.2 Exhaustive Language Coverage

The system does not guarantee:
- Detection of all paraphrases or obfuscations
- Coverage of all languages, dialects, or slang
- Robustness against unlimited adversarial prompt iteration

Detection is heuristic and signal-based, not exhaustive.

---

### 2.3 Autonomous Policy Evolution

The system does not:
- Self-modify enforcement rules
- Learn from user interactions
- Retrain or adapt models dynamically

All changes require explicit human review and code updates.

---

### 2.4 Zero False Positives

The system does not attempt to eliminate false positives.

Conservative enforcement is preferred over permissiveness when
ambiguity exists, particularly at elevated risk levels.

---

## 3. Rationale

These assumptions and non-goals are intentional.
They prioritize:
- Auditability
- Predictability
- Reviewer trust
- Clear threat boundaries

This design reflects red-team evaluation needs rather than production-scale deployment.

---

## Summary

Security guarantees are valid only within the assumptions stated above.
Functionality outside these boundaries is intentionally excluded from scope.
