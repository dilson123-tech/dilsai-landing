from dataclasses import dataclass
from pathlib import Path
import re

from app.schemas import ChatRequest


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1] / "knowledge"

STOPWORDS = {
    "sobre",
    "para",
    "como",
    "qual",
    "quais",
    "porque",
    "por",
    "uma",
    "uns",
    "das",
    "dos",
    "com",
    "que",
    "faca",
    "faça",
    "resumo",
    "curto",
    "explique",
    "explica",
    "exemplo",
    "simples",
    "teste",
    "contrato",
}


@dataclass(frozen=True)
class KnowledgeContext:
    found: bool
    source_path: str | None = None
    title: str | None = None
    content: str | None = None
    score: int = 0

    @property
    def prompt_context(self) -> str:
        if not self.found or not self.content:
            return ""

        return (
            "Base interna DilsAI Estudos encontrada.\n"
            f"Título: {self.title or 'Material interno'}\n"
            f"Arquivo: {self.source_path or 'base interna'}\n\n"
            f"{self.content.strip()}"
        )


def _normalize(value: str) -> str:
    normalized = value.lower()
    replacements = {
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ç": "c",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def _tokens(value: str) -> set[str]:
    normalized = _normalize(value)
    raw_tokens = re.findall(r"[a-z0-9_]{3,}", normalized)
    return {token for token in raw_tokens if token not in STOPWORDS}


def _title_from_content(content: str, fallback: str) -> str:
    for line in content.splitlines():
        clean = line.strip()
        if clean.startswith("#"):
            return clean.lstrip("#").strip() or fallback
    return fallback


def _iter_knowledge_files() -> list[Path]:
    if not KNOWLEDGE_ROOT.exists():
        return []
    return sorted(KNOWLEDGE_ROOT.rglob("*.md"))


def find_knowledge_context(payload: ChatRequest, max_chars: int = 2200) -> KnowledgeContext:
    query_text = " ".join(
        [
            payload.message or "",
            payload.level.value,
            payload.topic.value,
            payload.mode.value,
        ]
    )

    query_tokens = _tokens(query_text)
    if not query_tokens:
        return KnowledgeContext(found=False)

    best: KnowledgeContext | None = None

    for path in _iter_knowledge_files():
        rel_path = path.relative_to(KNOWLEDGE_ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        searchable = _normalize(f"{rel_path}\n{content}")

        score = 0

        if payload.topic.value != "geral" and payload.topic.value in searchable:
            score += 8

        if payload.level.value != "geral" and payload.level.value in searchable:
            score += 4

        for token in query_tokens:
            if token in searchable:
                score += 2

        if score < 6:
            continue

        clipped_content = content.strip()
        if len(clipped_content) > max_chars:
            clipped_content = clipped_content[:max_chars].rstrip() + "\n..."

        candidate = KnowledgeContext(
            found=True,
            source_path=rel_path,
            title=_title_from_content(content, fallback=path.stem),
            content=clipped_content,
            score=score,
        )

        if best is None or candidate.score > best.score:
            best = candidate

    return best or KnowledgeContext(found=False)
