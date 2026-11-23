"""Run reproducible PawPal RAG advisor examples from the command line."""

from datetime import date, time
from pathlib import Path

from pawpal_system import Owner, Pet, Task
from src.care_advisor import CareAdvisor


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    mochi.add_task(
        Task(
            "Medication",
            time(8, 0),
            "daily",
            10,
            "high",
            due_date=date.today(),
        )
    )
    owner.add_pet(mochi)

    advisor = CareAdvisor(
        Path("data/pet_care_knowledge.md"),
        Path("assets/advisor_log.jsonl"),
    )

    for question in (
        "How should I schedule medication?",
        "How do walking and exercise needs vary?",
        "What is quantum cryptography?",
    ):
        try:
            response = advisor.advise(owner, question)
        except ValueError as error:
            print(f"ERROR: {error}")
            continue

        print(f"\nInput: {question}")
        print(f"Answer: {response.answer}")
        print(
            "Sources: "
            + (", ".join(response.sources) if response.sources else "none")
        )
        print(f"Confidence: {response.confidence:.0%}")


if __name__ == "__main__":
    main()
