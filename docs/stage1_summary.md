## Overview ##
Stage 1 evaluated foundational control integrity of an LLM-based conversational system, focusing on prompt-based attacks that target instruction hierarchy, role integrity, and system authority boundaries.

## Scope ##
* Single FastAPI-based LLM chat endpoint
* No authentication or role seperation
* Black-box interactive via API requests

## Attack Classes Tested ##
* Prompt injection and instruction override
* Instruction hierarchy confusion
* Role and integrity redefinition

## Key Findings ##
* Partial compliance observed during prompt injection attempts due to engagement with attacker framing
* Instruction hierarchy override enabled user-supplied authority claims to supercede system unstructions
* Role redefinition attacks successfully induced the model to abandon its intended identity

## Mitigations Implemented ##
* All previously identified attack classes were re-tested post-mitigation
* Clean refusals observed across all tests
* No instruction hierarchy override or role redefinition observed

## Conclusion ##
Stage 1 mitigations significantly reduced prompt-based control failures and improved system resilience against foundational AI red-team attack techniques.


