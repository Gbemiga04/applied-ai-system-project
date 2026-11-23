# Model Card

## Base Project and System Purpose

PawPal+ evolved from `ai110-module2show-pawpal-starter`, a pet-care task and scheduling
application. The applied system adds a local retrieval-augmented care-plan advisor that
retrieves general care guidance and combines it with current PawPal task priorities and conflicts.

The system helps pet owners draft safer scheduling questions and explanations. It does not
diagnose conditions or replace veterinary care.

## AI Collaboration

AI-assisted tools were used to identify integration points, generate candidate code and tests,
debug failures, and prepare documentation. The implementation was validated by repository
tests, local execution, and explicit source/retrieval checks. AI-generated suggestions were
reviewed manually rather than assumed correct.

### Collaboration Examples

**Suggestion accepted:** The suggestion to extend the existing PawPal+ project with a RAG-based
Care-Plan Advisor was accepted because it builds on the repository's scheduling logic, uses a
local knowledge source, and remains reproducible without an external API.

**Suggestion rejected or revised:** The original retrieval approach was revised to remove broad,
frequently used words such as "what," "when," "how," and "the" from lexical matching. This
prevented unrelated questions from retrieving general routines by ordinary wording and was
reinforced by a refusal test for unsupported topics.

## Intended Use

Intended users are pet owners who already use PawPal+ to organize routine care tasks. Suitable
uses include:

- Explaining general medication scheduling cautions
- Reviewing why tasks are prioritized
- Understanding common overlap and conflict concerns
- Finding a source section for general pet-care guidance

## Out-of-Scope Use

The system must not be used to:

- Diagnose illness or injury
- Determine medication dosage or changes
- Replace a veterinarian or emergency care
- Treat toxic exposure or medical emergencies
- Make claims about species-specific care without professional information

### Misuse Prevention

The system does not generate prescriptions or change medication doses. Unsupported questions
receive an explicit refusal, medical answers include a disclaimer and source, and the interface
does not collect or transmit pet data to an external service. Privacy-sensitive details should
still be avoided in logged questions, and future deployments should restrict or remove logs,
require consent, and add veterinary review before clinical use.

## Data and Retrieval

The knowledge source is `data/pet_care_knowledge.md`, curated for this project. Documents are
split into heading-based text chunks. Retrieval uses case-folded lexical term overlap and source
heading scoring; the top three chunks are considered.

The answer generator is a local template assembly process. It is not a generative language model
and does not call an external API. It combines retrieved text with task data from `Scheduler`
and explicitly adds sources and confidence.

## Biases and Limitations

Potential issues include:

- Lexical retrieval can miss differently worded relevant questions.
- General guidance may not fit a pet's species, breed, age, or health status.
- Knowledge content is limited and may become outdated.
- The confidence score is a retrieval heuristic, not measured clinical accuracy.
- Task priorities reflect owner-entered values rather than veterinary validation.
- English-only queries and guidance are supported.

## Guardrails

- Empty questions are rejected.
- Questions are limited to 500 characters.
- Unsupported topics receive a refusal.
- Retrieved sources are shown with answers.
- A medical disclaimer is included.
- Medication dose changes are not recommended.
- The Streamlit UI and CLI handle missing knowledge files and invalid input explicitly.
- Advisor requests, sources, confidence, and retrieved sections are written to JSON Lines.

## Reliability Testing

Automated tests verify:

- Medication guidance retrieval
- Unsupported-topic refusal
- Empty input rejection
- JSON Lines logging
- Existing task sorting and recurrence
- Conflict and open-slot behavior
- Task persistence and validation

The local automated run collected 28 tests and passed all 28.

### Surprising Testing Results

The test suite showed that a question containing ordinary pet-care words could retrieve broad
routine guidance even when the topic was unrelated. This demonstrated that lexical overlap alone
is not enough evidence for safe answers. The stop-word filter and unsupported-topic refusal were
added as a direct result of that finding.

No human medical accuracy evaluation has been completed. A future release should be reviewed by
a veterinarian or qualified animal-care professional before broad use.

## Ethical Considerations

The system minimizes privacy risk by retaining only local task data and logging questions locally.
Pet-owner names and task descriptions remain in `data.json`; users should avoid entering sensitive
information. Responses are transparent about sources and uncertainty, while the system's general
disclaimer and refusal behavior reduce misleading confidence.

Accessibility, task overload, and urgent health situations are limitations. Users should seek
professional or emergency care for symptoms outside routine scheduling.
