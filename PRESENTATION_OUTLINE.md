# PawPal+ Applied AI System Presentation

**Target length:** 5-7 minutes

## 1. Problem and Base Project (45-60 seconds)

- Introduce the original PawPal+ scheduling project.
- Explain the need to ground pet-care scheduling guidance in visible, local sources.

## 2. Live Demonstration (2-3 minutes)

- Start the Streamlit application.
- Add or select a pet and schedule a high-priority medication task.
- Ask a medication question.
- Show retrieved sources and confidence.
- Ask an unsupported question and show the refusal.
- Run `python evaluate_advisor.py` or `python -m pytest`.

## 3. Architecture and Design (60-90 seconds)

- Explain input validation, lexical retrieval, PawPal scheduling context, response assembly,
  citations, confidence, logging, and testing.
- Explain the trade-off between local reproducibility and limited semantic retrieval.

## 4. Reliability and Guardrails (60 seconds)

- Summarize 28/28 pytest results and 3/3 evaluation-harness cases.
- Explain unsupported-question refusal, source display, and the general-guidance disclaimer.

## 5. Ethics and Reflection (45-60 seconds)

- Discuss pet privacy, misuse, medical safety, limitations, and lack of human clinical evaluation.
- Describe one accepted suggestion and one revised suggestion.
- Explain what the project taught you about responsible AI engineering.
