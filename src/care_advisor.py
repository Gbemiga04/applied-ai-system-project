"""Retrieval-grounded, local Pet-Care Advisor for PawPal+."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from pawpal_system import Owner, Scheduler


@dataclass(frozen=True)
class KnowledgeChunk:
    heading: str
    text: str
    source: str


@dataclass(frozen=True)
class AdvisorResponse:
    answer: str
    sources: tuple[str, ...]
    confidence: float
    retrieved: tuple[KnowledgeChunk, ...]


class CareAdvisor:
    """Retrieve pet-care guidance and ground short recommendations in it."""

    def __init__(
        self,
        knowledge_path: str | Path,
        log_path: str | Path | None = None,
    ) -> None:
        self.knowledge_path = Path(knowledge_path)
        self.log_path = Path(log_path) if log_path else None
        self.chunks = self._load_chunks()

    def _load_chunks(self) -> tuple[KnowledgeChunk, ...]:
        if not self.knowledge_path.exists():
            raise FileNotFoundError(
                f"Knowledge file not found: {self.knowledge_path}"
            )

        markdown = self.knowledge_path.read_text(encoding="utf-8")
        chunks: list[KnowledgeChunk] = []
        heading = "General guidance"
        paragraph_lines: list[str] = []

        for line in markdown.splitlines() + [""]:
            if line.startswith("## "):
                if paragraph_lines:
                    chunks.append(
                        KnowledgeChunk(
                            heading,
                            " ".join(paragraph_lines).strip(),
                            f"{self.knowledge_path.name}#{heading}",
                        )
                    )
                    paragraph_lines = []
                heading = line.removeprefix("## ").strip()
            elif line.startswith("# ") or not line.strip():
                continue
            else:
                paragraph_lines.append(line.strip())

        if not chunks:
            raise ValueError("Knowledge file contains no guidance sections.")
        return tuple(chunks)

    @staticmethod
    def _terms(text: str) -> set[str]:
        stop_words = {
            "and", "are", "for", "from", "have", "that", "the", "this",
            "what", "when", "where", "which", "with", "should", "does",
            "how", "is", "to",
        }
        return {
            word
            for word in re.findall(r"[a-z0-9]+", text.casefold())
            if len(word) > 2 and word not in stop_words
        }

    def retrieve(self, question: str, limit: int = 3) -> tuple[KnowledgeChunk, ...]:
        query_terms = self._terms(question)
        if not query_terms:
            return ()

        scored: list[tuple[float, KnowledgeChunk]] = []
        for chunk in self.chunks:
            chunk_terms = self._terms(f"{chunk.heading} {chunk.text}")
            overlap = len(query_terms & chunk_terms)
            if overlap:
                score = overlap / max(len(query_terms), 1)
                if any(term in chunk.heading.casefold() for term in query_terms):
                    score += 0.25
                scored.append((score, chunk))

        scored.sort(key=lambda item: (-item[0], item[1].heading))
        return tuple(chunk for _, chunk in scored[:limit])

    def advise(
        self,
        owner: Owner,
        question: str,
        on_date: date | None = None,
    ) -> AdvisorResponse:
        cleaned_question = question.strip()
        if not cleaned_question:
            raise ValueError("Question cannot be empty.")
        if len(cleaned_question) > 500:
            raise ValueError("Question must be 500 characters or fewer.")

        retrieved = self.retrieve(cleaned_question)
        scheduler = Scheduler(owner)
        schedule_date = on_date or date.today()
        schedule = scheduler.organize_tasks(include_completed=False)
        conflicts = scheduler.detect_conflicts(on_date=schedule_date)

        if not retrieved:
            response = AdvisorResponse(
                answer=(
                    "I do not have enough supporting guidance in the local knowledge "
                    "base to answer that safely. Please rephrase the question or consult "
                    "a veterinarian."
                ),
                sources=(),
                confidence=0.20,
                retrieved=(),
            )
        else:
            guidance = " ".join(chunk.text for chunk in retrieved)
            answer_parts = [guidance]

            if schedule:
                first_three = schedule[:3]
                plan_lines = [
                    f"{pet.name}: {task.description} at "
                    f"{task.time.strftime('%I:%M %p')} ({task.priority} priority)"
                    for pet, task in first_three
                ]
                answer_parts.append(
                    "Current priority context: " + "; ".join(plan_lines) + "."
                )

            if conflicts:
                answer_parts.append(
                    "Scheduling caveat: " + " ".join(conflicts)
                )

            answer_parts.append(
                "This is general guidance, not an individual veterinary diagnosis."
            )
            response = AdvisorResponse(
                answer=" ".join(answer_parts),
                sources=tuple(dict.fromkeys(chunk.source for chunk in retrieved)),
                confidence=min(0.95, 0.45 + 0.15 * len(retrieved)),
                retrieved=retrieved,
            )

        self._log(question=cleaned_question, response=response)
        return response

    def _log(self, *, question: str, response: AdvisorResponse) -> None:
        if self.log_path is None:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "question": question,
            "answer": response.answer,
            "sources": list(response.sources),
            "confidence": response.confidence,
            "retrieved_sections": [
                chunk.heading for chunk in response.retrieved
            ],
        }
        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(record) + "\n")
