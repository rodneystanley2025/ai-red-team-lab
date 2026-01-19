Stage 11B - Cross-Turn Enforcement Strategy (Minimal State)

Objective

Translate the Stage 11A cross-turn risk dampening design into an enforceable, minimal-state strategy that resists
crescendo-style attacks without introducing full conversational memory.

This stage defines how signals accumulate, decay, and trigger enforcement across turns while preserving determinism and
auditability.

Design Principles
1. Minimal State
  * No storage of raw prompts or responses
  * Only aggregate, numeric risk metadata is retained
2. Deterministic Enforcement
  * Same inputs _ same prior risk state -> same outcomes
3. Bounded Retention
  * Risk state expires automatically
  * No long-term user profiling
4. Defense-in-Depth
  * Cross-turn logic augments (does not replace) existing guards

Cross-Turn Risk Model

Risk State Structure

CrossRiskState
- rolling_score: int
- last_updated_ts: float
- strike_count: int

rolling_score
Weighted accumulation of recent risk signals.

strike_count
Counts how many times escalation thresholds were crossed.

last_updated_ts
Used to apply time-based decay.

Risk Accumulation Rules
On each request:
1. Compute single-turn crescendo score via assess_crescendo_risk()
2. Apply decay to existing rolling_score
3. Add new score

rolling_score = (rolling_score * decay_factor) + new_score

Suggested Parameters
parameter       Value           Rationale
decay_factor    0.6-0.8         Prevents permanent suspicion
state_ttl       10-20 minutes   Limits memory window
max_strikes     2-3             Prevents repeated probing

Escalation Thresholds
Condition                   Action
rolling_score >= HIGH       Soft warning
rolling_score >= CRITICAL   Hard denial
strike_count >= max_strikes Session-level blocks

Important:
  * Hard denial suppresses model output entirely
  * Soft warning still allows safe redirection

Enforcement Order
Cross-turn enforcement is evaluated before model output is returned but after single-turn stateless checks:
1. Memory boundary checks
2. Authority / training data checks
3. Single-turn crescendo scoring
4. Cross-turn risk evaluation -< this stage
5. Tool execution validation

Failure Modes & Safeguards
False Positives
Mitigation:
  * Aggressive decay
  * Require multiple signals before escalation

User Confusion
Mitigation:
  * Canonical escalation messaging
  * Clear rephrasing guidance

State Corruption
Mitigation:
  * Stateless fallback on state errors
  * Automatic state reset on TTL expiry

Audit & Observability
The following metadata MUST be loggable (without storing content):
  * rolling_score
  * risk_level
  * triggered thresholds
  * enforcement action

This enables post-incident review without violating privacy.

Exit Criteria
This stage is complete when:
  * Cross-turn logic is fully specified
  * Parameters are documented
  * No raw user content is retained
  * Design is implementable in policy_enforcer without architectural changes

## Evaluation Outcome: Cross-Turn Accumulation Failure

Despite successful single-turn crescendo detection, cross-turn accumulation did not prevent semantic drift across turns.

### Key Observation
Earlier benign context allowed later turns to inherit unsafe semantic framing without sufficient risk carryover.

### Root Cause
Risk accumulation currently influences enforcement decisions but does not constrain semantic interpretation across turns.

### Security Impact
An adaptive adversary could exploit gradual topic drift to reach unsafe outcomes despite escalation logic.

### Status
Open – Requires semantic dampening or decay-based context shaping (planned Stage 11B/11C).
