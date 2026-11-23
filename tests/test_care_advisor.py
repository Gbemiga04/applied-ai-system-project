from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task
from src.care_advisor import CareAdvisor


def make_owner() -> Owner:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(
        Task(
            "Medication",
            time(8, 0),
            "daily",
            10,
            "high",
            due_date=date.today(),
        )
    )
    owner.add_pet(pet)
    return owner


def test_advisor_retrieves_medication_guidance(tmp_path) -> None:
    advisor = CareAdvisor(
        "data/pet_care_knowledge.md",
        tmp_path / "advisor.jsonl",
    )

    response = advisor.advise(make_owner(), "When should medication be given?")

    assert "Medication" in " ".join(chunk.heading for chunk in response.retrieved)
    assert response.sources
    assert response.confidence >= 0.45


def test_advisor_refuses_when_no_knowledge_matches(tmp_path) -> None:
    advisor = CareAdvisor(
        "data/pet_care_knowledge.md",
        tmp_path / "advisor.jsonl",
    )

    response = advisor.advise(make_owner(), "What is quantum cryptography?")

    assert "do not have enough supporting guidance" in response.answer
    assert not response.sources
    assert response.confidence == 0.20


def test_advisor_rejects_empty_question() -> None:
    advisor = CareAdvisor("data/pet_care_knowledge.md")

    try:
        advisor.advise(make_owner(), "   ")
    except ValueError as error:
        assert "cannot be empty" in str(error)
    else:
        raise AssertionError("Empty questions must be rejected.")


def test_advisor_logs_retrieval(tmp_path) -> None:
    log_path = tmp_path / "advisor.jsonl"
    advisor = CareAdvisor("data/pet_care_knowledge.md", log_path)
    advisor.advise(make_owner(), "How do I handle medication?")

    assert log_path.exists()
    assert "Medication" in log_path.read_text(encoding="utf-8")
