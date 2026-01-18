Stage 11A — Cross-Turn Risk Dampening (Design)

Objective
Design a cross-turn risk dampening mechanism that mitigates crescendo-style multi-turn attacks while preserving the 
system’s core statelessness guarantees and avoiding conversational memory retention.

This stage focuses on architectural design only. No implementation decisions are enforced at this stage.

Background
Earlier stages demonstrated that:
  * Single-turn semantic risk detection (Stage 10) significantly improves safety.
  * Stateless enforcement alone is insufficient against crescendo attacks, where risk escalates gradually across turns.
  * Fully conversational memory introduces unacceptable privacy, leakage, and compliance risks.

Therefore, a minimal, risk-only continuity model is required.

Threat Model
Adversary Capabilities
  * Adaptive multi-turn prompting
  * Contextual softening (fiction, education, history)
  * Incremental escalation toward disallowed content
  * Avoidance of explicit policy keywords

Target Weakness
  * Stateless systems that treat each request independently
  * Guards that evaluate intent only per-turn
  * Lack of cumulative risk awareness

Design Constraints (Non-Negotiable)
The dampening mechanism MUST:
1. Not store or reconstruct conversation content
2. Not retain user prompts or model outputs
3. Not infer or simulate conversational memory
4. Be deterministic and auditable
5. Fail closed (safe behavior on error)
6. Remain compatible with stateless deployment models

Design Principles
1. Risk-Only Continuity

Only numeric or categorical risk metadata may persist across turns.

Allowed examples:
  * Aggregate risk score
  * Last observed risk level
  * Escalation counter
  * Time-based decay values

Disallowed examples:
  * Prompt text
  * Summaries
  * Topic inference
  * User intent narratives

2. Escalation Dampening (Not Immediate Blocking)
The system should:
  * Allow benign exploration
  * Slow escalation through warnings
  * Harden enforcement only after sustained risk accumulation

This prevents false positives while stopping slow-burn attacks.

3. Temporal Decay
Risk should decay over time, preventing permanent lockout due to:
  * Accidental phrasing
  * Legitimate educational inquiry
  * One-off high-risk terms

Decay resets the system toward neutrality unless reinforced.

Conceptual Model
Risk State (Ephemeral)

A minimal risk state may include:

Field	               Description
cumulative_score	   Sum of recent risk signals
last_risk_level	       Highest recent risk level
escalation_count	   Number of consecutive escalations
last_updated	       Timestamp for decay calculations

This state:
  * Is not content-derived
  * Can be scoped to session, request batch, or short-lived token
  * Is disposable without security impact

Escalation Logic (Conceptual)
Condition	           Outcome
LOW → MEDIUM	       Allow with no change
MEDIUM → repeated	   Soft warning
HIGH sustained	       Hardened refusal
CRITICAL spike	       Immediate denial
Risk decay elapsed	   Gradual reset

Integration Points (Design Only)

The dampening layer is evaluated:
  * After single-turn risk scoring (crescendo_guard)
  * Before final allow/deny decision
  * Before model output is returned

This ensures:
  * Model outputs never leak unsafe content
  * Enforcement remains centralized

Failure Modes & Safety
On State Loss
  * Default to single-turn enforcement
  * Do not assume benign or malicious intent

On Corruption
  * Reset state
  * Apply conservative enforcement

Explicit Non-Goals
This stage does not attempt to:
  * Perform user profiling
  * Infer user intent
  * Build conversational memory
  * Replace policy-based controls
  * Detect all possible attacks

It strictly reduces residual risk, not eliminates it.

Expected Benefits
  * Strong mitigation against crescendo attacks
  * Maintains privacy guarantees
  * Preserves explainability
  * Aligns with real-world AI safety constraints
  * Demonstrates mature security architecture thinking
