# Reproducible Execution Evidence

## Automated Tests

Command:

```powershell
python -m pytest
```

Result:

```text
28 tests collected
28 tests passed
0 tests failed
```

## CLI Advisor

Command:

```powershell
python main_advisor.py
```

Representative output:

```text
Input: How should I schedule medication?
Sources: pet_care_knowledge.md#Schedule conflicts,
pet_care_knowledge.md#Medication,
pet_care_knowledge.md#Daily routines
Confidence: 90%

Input: How do walking and exercise needs vary?
Sources: pet_care_knowledge.md#Walking and exercise,
pet_care_knowledge.md#Schedule conflicts
Confidence: 75%

Input: What is quantum cryptography?
Answer: I do not have enough supporting guidance in the local knowledge base to answer that safely.
Sources: none
Confidence: 20%
```

## Syntax Validation

Command:

```powershell
python -m py_compile app.py main.py main_advisor.py pawpal_system.py src/care_advisor.py
```

Result: all entry points compiled successfully with no syntax errors.

## Evaluation Harness

Command:

```powershell
python evaluate_advisor.py
```

Result:

```text
PASS: medication retrieval
  confidence=90%
PASS: unsupported refusal
  confidence=20%
PASS: exercise retrieval
  confidence=75%
Summary: 3/3 passed
```
