Stage 10.2 — Crescendo Escalation Rules & Enforcement Strategy

Purpose
This document defines deterministic escalation rules for handling crescendo-style attacks detected by the Crescendo 
Guard. The goal is to prevent gradual policy erosion caused by multi-turn or contextually softened prompts while 
preserving stateless operation and minimizing false positives.

These rules explicitly separate risk detection from enforcement actions, ensuring transparency, auditability, and 
defense-in-depth.

Design Principles
The escalation model adheres to the following principles:
1. Stateless Enforcement
  * No conversation history is stored.
  * Each request is evaluated independently using semantic risk scoring.

2. Progressive Escalation
  * Not all risky prompts result in immediate denial.
  * Responses tighten as risk increases.

3. Deterministic Outcomes
  * Given the same input, the same escalation outcome occurs.
  * No probabilistic or opaque behavior.

4. Policy Compatibility
  * Escalation complements existing policy enforcement.
  * Crescendo Guard does not replace content policy checks.

Risk Levels
The Crescendo Guard produces one of four risk levels based on accumulated semantic signals:

Risk Level	          Description
LOW	                  Benign input with no meaningful risk indicators
MEDIUM	              Implicit pressure or contextual softening detected
HIGH	              Clear convergence toward restricted domains
CRITICAL	          Strong indicators of imminent policy violation

Escalation Actions by Risk Level

LOW — Normal Operation
Criteria
  * Total risk score below threshold
  * No high-risk domain indicators

Enforcement Action
  * No escalation
  * Input proceeds through standard policy enforcement
  * Normal model response allowed

Rationale
Benign inputs should not incur friction or unnecessary disclaimers.

MEDIUM — Soft Guardrail Activation
Criteria
  * Implicit continuation, contextual softening, or mild convergence detected

Enforcement Actions
* Allow response generation
* Apply safety-aware framing, such as:
  * Generalized explanations
  * High-level descriptions
  * Avoidance of procedural or operational detail

* Optionally reassert statelessness if continuation is implied

Example Response Behavior
“I can discuss this at a high level, but I can’t assume prior context or provide step-by-step guidance.”

Rationale
This level intercepts early crescendo pressure without prematurely denying legitimate educational queries.

HIGH — Constraint Tightening
Criteria
  * Multiple risk signals
  * Clear approach toward disallowed domains
  * Escalation pattern consistent with crescendo attacks

Enforcement Actions
* Block procedural, instructional, or actionable content
* Restrict output to:
  * Safety context
  * Risk discussion
  * Historical or ethical framing without technical details
* Trigger canonical boundary responses if applicable

Example Response Behavior
“I can explain why this topic is risky or how such threats are mitigated, but I can’t provide instructions or simulations.”

Rationale
At this stage, the system should assume adversarial pressure and prioritize safety over usefulness.

CRITICAL — Hard Denial
Criteria
  * High-risk domain indicators combined with contextual justification
  * Strong likelihood of policy violation if answered

Enforcement Actions
  * Immediately halt response generation
  * Return a canonical refusal
  * Do not provide alternative phrasing suggestions that advance the same goal

Example Response
“I can’t help with that request.”

Rationale
CRITICAL signals indicate imminent misuse. No additional information should be disclosed.

Interaction with Existing Policy Enforcement
The Crescendo Guard operates as a pre-policy risk gate:
1. User input is scored by Crescendo Guard
2. Escalation rules determine allowable response scope
3. Standard policy enforcement (policy_enforcer.py) is applied
4. Tool execution remains subject to allow-lists and schema validation
If either system triggers a denial, the denial is enforced.

Non-Goals
This escalation system explicitly does not:
  * Infer user intent with certainty
  * Track users across sessions
  * Maintain conversational memory
  * Replace content policy enforcement
  * Use machine learning classifiers

Security Value
This design directly mitigates:
  * Crescendo attacks
  * Contextual policy contradictions
  * Multi-turn pressure without memory
  * Fictional, educational, or historical framing bypasses
It provides a scalable, explainable control suitable for real-world AI systems.
