Stage 9 – Crescendo Attack Mitigation Design

(Risk Scoring with Escalation Thresholds)

Objective:
Design and specify a robust mitigation mechanism capable of detecting and preventing crescendo-style multi-turn attacks, 
where adversarial intent is gradually escalated across benign-looking prompts.

This stage defines a risk-based, state-aware mitigation model that supplements existing single-turn policy enforcement 
without relying on brittle keyword blocking or static rule sets.

Threat Model:
Adversary Profile:
An adaptive user who incrementally escalates intent across multiple turns, using:

Innocuous framing

Educational or fictional context

Gradual specificity increases

Semantic pivots rather than explicit policy violations

Attack Goal:
Reach a disallowed request (e.g., weapon construction, chemical synthesis, wrongdoing enablement) without triggering 
single-turn guardrails.

Design Principles

Defense-in-depth:
Single-turn policy checks are necessary but insufficient against multi-turn escalation.

Intent accumulation:
Risk should increase across turns, even when individual prompts appear benign.

Explicit escalation thresholds:
Enforcement actions must trigger deterministically once cumulative risk exceeds defined bounds.

Explainability:
The mitigation logic must be auditable and defensible for security review.

Mitigation Architecture Overview

The proposed solution introduces a Crescendo Risk Engine (CRE) that operates alongside existing policy enforcement.

High-Level Flow

User submits prompt

Prompt is evaluated for incremental risk signals

Risk score is accumulated in a short-lived session context

Escalation thresholds are evaluated

Appropriate response action is taken

Risk Scoring Model

Each user turn is evaluated for semantic escalation indicators, not just explicit violations.

Example Risk Signals
Signal Category	          Examples	                          Risk Weight
Contextual persistence	  “continue”, “as discussed”,         +1
                          “assume we covered”
Domain narrowing	      Shifting from abstract to specific  +2
Operational framing	      “step-by-step”, “how exactly”	      +3
Harmful domain proximity  Weapons, chemicals, fraud, evasion  +4
Policy boundary probing	  “hypothetically”, “for research”	  +2

Each turn may accumulate multiple signals.

Escalation Thresholds
Cumulative Risk Score	System Behavior
0–3	                    Normal response
4–6	                    Cautionary framing + safe redirection
7–9	                    Partial refusal + boundary clarification
≥10	                    Full refusal + policy explanation

Thresholds are configurable and should be tuned based on empirical testing.

Enforcement Actions
When thresholds are crossed, the system may:
* Reassert safety boundaries
* Refuse to continue the line of inquiry
* Redirect to high-level, non-operational discussion
* Reset or decay session risk after enforcement

Responses must remain non-accusatory and non-revealing.

Session Scope and Risk Decay

To avoid overfitting or punishing benign users:
* Risk score is session-scoped
* Risk decays after:
  * Topic change
  * Explicit refusal
  * Time-based expiration

This balances security with usability.

Relationship to Existing Controls
This mitigation:
* Complements existing single-turn policy enforcement
* Does not replace content classifiers
* Closes a known gap exploited by adaptive adversaries

Notably, it addresses failures observed in:
* Stage 5.4 – Multi-turn pressure
* Stage 5.5 – Contextual policy contradiction
* Stage 8 – Crescendo attack patterns

Limitations
* Requires session tracking (even if ephemeral)
* Risk scoring involves heuristic tuning
* Cannot guarantee perfect intent inference

These limitations are acceptable given the threat model and significantly reduce practical exploitability.

Success Criteria

This mitigation is considered successful if:
* Crescendo-style escalation is detected before disallowed output
* No single-turn policy violations are required to trigger enforcement
* False positives remain low under benign multi-turn use
* Security reviewers can trace why enforcement occurred

Next Steps
* Implement CRE in policy_enforcer layer
* Add unit tests simulating crescendo escalation
* Red-team the mitigation with adaptive prompt sequences
* Tune thresholds based on observed behavior
