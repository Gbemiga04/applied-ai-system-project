"""Run predefined Care-Advisor reliability cases and print a pass/fail summary."""

from pathlib import Path

from pawpal_system import Owner
from src.care_advisor import CareAdvisor


CASES = (
    {
        "name": "medication retrieval",
        "question": "How should medication be given?",
        "expected_source": "Medication",
        "should_refuse": False,
    },
    {
        "name": "unsupported refusal",
        "question": "What is quantum cryptography?",
        "expected_source": None,
        "should_refuse": True,
    },
    {
        "name": "exercise retrieval",
        "question": "How do walking and exercise needs vary?",
        "expected_source": "Walking and exercise",
        "should_refuse": False,
    },
)


def main() -> None:
    advisor = CareAdvisor(
        Path("data/pet_care_knowledge.md"),
        Path("assets/advisor_log.jsonl"),
    )
    passed = 0

    print("PawPal+ RAG Evaluation")
    print("======================")
    for case in CASES:
        response = advisor.advise(Owner("Evaluation"), case["question"])
        source_text = " ".join(response.sources)
        source_pass = (
            case["expected_source"] is None
            or case["expected_source"] in source_text
        )
        refusal_pass = (
            ("do not have enough supporting guidance" in response.answer)
            if case["should_refuse"]
            else bool(response.sources)
        )
        case_passed = source_pass and refusal_pass
        passed += int(case_passed)
        status = "PASS" if case_passed else "FAIL"

        print(f"{status}: {case['name']}")
        print(f"  confidence={response.confidence:.0%}")
        print(
            "  sources="
            + (", ".join(response.sources) if response.sources else "none")
        )

    print("======================")
    print(f"Summary: {passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
