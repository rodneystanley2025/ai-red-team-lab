1. System Overview
Describe what exists today, not what will exist later.

### Stage 2 Additions

- Introduction of a model-invoked tool interface
- Model output may trigger tool execution
- Tool output is returned to the user
- No authentication or authorization on tool usage

Include:
FastAPI service exposing a /chat endpoint
Single LLM call per request
Static system prompt loaded from file
No authentication
No RAG
No agents

This anchors the scope.

Out of Scope (for Stage 1)

In Scope (Stage 2 Additions)

- Tool invocation logic
- Tool input construction
- Trust boundary between model output and tool execution
- Tool outputs returned to the user

2. System Boundaries
This is where you explicitly define what is in scope vs. out of scope.
In Scope
FastAPI application
Prompt construction logic
System prompt content
User-provided input
Model responses returned to user
Out of Scope (for Stage 1)
Model training
Model weights
Network-level attacks
Cloud infrastructure security
Authentication / authorization
Persistent storage

This protects you from scope creep and shows maturity.

3. Trust Boundaries
These are the critical AI-specific boundaries.
At minimum, include:

User Input → Prompt Construction
Untrusted user data is combined with trusted system instructions
Prompt → Model Inference
Model behavior depends on instruction hierarchy
Model Output → API Response
Output is returned directly without validation

Explicitly stating these is a strong signal.

Model Output → Tool Invocation

Model-generated output is treated as actionable input for system tools.
This represents a critical trust boundary where unvalidated model behavior may trigger system actions.


4. Assumptions
Assumptions make your threat model defensible.

Examples (adapt as needed):
The model provider enforces baseline safety policies
The system prompt is not modified at runtime
Users are unauthenticated and potentially malicious
All user input is untrusted
No rate limiting is in place
Assumptions explain why certain threats are or are not considered.

The system implicitly trusts model-generated tool invocation requests
Tools do not perform independent authorization or intent validation
Model output may include attacker-influenced instructions

5. Assets
Examples:
Integrity of system instructions
Predictability of model behavior
Availability of the service
Trustworthiness of responses

Integrity of tool execution
Correctness of tool inputs
Trust boundary between model reasoning and system actions

6. Actors
External user (benign)
External user (malicious)
System operator

7. Entry points
For Stage 1:
/chat endpoints
User input field

Model-generated tool invocation requests
Indirect attacker influence via embedded instructions

8. High-Level Threats
Only ones that are not exploited yet
Examples:
Prompt injection altering system behavior
Instruction hierarchy override
Safety or policy bypass
Output manipulation
Resource exhaustion via crafted prompts

Stage 2 Threats

- Indirect prompt injection via attacker-controlled content
- Unauthorized or unintended tool invocation
- Manipulation of tool inputs through model output
- Over-trust of model-generated instructions

## Stage 3 Threats ##
In Scope (Stage 3)
* Model claims of memory or stored data
* Assertions of access to prior conversations
* Assertions of access to internal documentation
* Hallucinated system logs or reports
* False training data disclosure

# Out of Scope (Stage 3) #
* Retrieval-Augmented Generation (RAG)
* External databases
* Persistent user memory
* Fine-tuning datasets
* Logging infrastructure

# New High-Level Threats (Stage 3) #
* Hallucinated memory or persistent storage
* False claims of access to internal systems
* Training data disclosure claims
* Fabricated system logs or reports
* Authority impersonation (“as an internal system…”)

# New Assumptions (Stage 3) #
* The model has no memory between requests
* The system does not store user conversations
* The model does not have access to training data contents
* Any claim of stored data is untrusted

