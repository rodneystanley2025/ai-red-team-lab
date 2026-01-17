# Known Limitations

This document outlines known and accepted limitations of the AI Red Team Lab.
These limitations are intentional design trade-offs made to preserve system
clarity, auditability, and safety.

The presence of these limitations does not indicate unmitigated vulnerabilities,
but rather clearly scoped boundaries of responsibility.

---

## 1. Stateless Risk Evaluation

The system is intentionally stateless and does not retain user conversation
history across requests.

As a result:
- Long-horizon crescendo attacks spanning many turns may evade detection
- Risk scoring is based solely on the current input
- Cross-session correlation is out of scope

This trade-off prioritizes determinism, privacy, and auditability over
long-term behavioral tracking.

---

## 2. Heuristic-Based Crescendo Detection

Crescendo-style attack detection relies on heuristic signal detectors
(e.g., implicit continuation, contextual softening, high-risk domain terms).

Limitations include:
- Adversarial paraphrasing may reduce signal activation
- Novel linguistic patterns may not trigger existing detectors
- Risk scoring reflects likelihood, not certainty of malicious intent

These limitations are partially mitigated through conservative escalation
thresholds and defense-in-depth enforcement.

---

## 3. False Positives at Elevated Risk Levels

The system intentionally tolerates false positives at HIGH and CRITICAL
risk levels.

This may result in:
- Soft warnings or denials for benign but ambiguous prompts
- Reduced assistance in edge-case educational scenarios

This behavior is considered acceptable to prioritize safety over completeness.

---

## 4. No User Identity or Intent Attribution

The system does not perform:
- User identification
- Behavioral profiling
- Intent attribution beyond prompt-level analysis

All risk assessments are content-based and context-limited by design.

---

## 5. Non-Goals

The following are explicitly out of scope:
- Persistent user tracking
- Automated incident response
- Forensic reconstruction of attack chains
- Real-time model retraining or adaptive learning

These capabilities may be appropriate for production systems but are
intentionally excluded from this lab to preserve clarity and reviewability.

---

## Summary

These limitations are known, documented, and accepted.
They reflect conscious architectural decisions rather than implementation gaps.
