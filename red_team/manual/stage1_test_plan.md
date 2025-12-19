Required Structure
1. Objective
The objective of this test plan is to assess the susceptibility of the Stage 1 AI chatbot to prompt-based attacks that may compromise system instruction integrity, safety controls, or output trustworthiness.

2. In-Scope Components
List only what exists today:
/chat API endpoint
Prompt construction logic
Static system prompt
Model output returned to users

3. Out-of-Scope Components
Reinforce boundaries:
Authentication and authorization
Model training or fine-tuning
Infrastructure or network security
Rate limiting or abuse prevention

This protects you from overreach.

4. Threat-to-Test Mapping
This is the core of the document.
Create a table or bullet structure mapping:
Threat
Test Objective
Expected Insecure Behavior
Example (adapt, don’t copy verbatim):

Threat: Prompt injection
Test Objective: Determine whether user input can override or neutralize system instructions
Expected Insecure Behavior: Model prioritizes user instructions over system prompt

5. Test Execution Approach
Describe how testing will be performed, not payloads.
Include:
Manual testing via direct API calls
Incremental prompt manipulation
Observation of model behavior changes
No automation at this stage

This shows methodological restraint.

6. Success Criteria
Define what constitutes a finding:
Clear deviation from intended system behavior
Reproducible behavior across attempts
Observable impact to integrity, safety, or trust
