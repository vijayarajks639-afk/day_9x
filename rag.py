"""D9X-4 — Shadow-mode retrieval engine (adapted from reg_rag_assistant/rag.py).

The AI teammate's "reading": structure-aware chunking of the team's runbooks PLUS any
coached Skills, local embeddings (fastembed/ONNX — nothing leaves the machine), a
transparent numpy cosine index, and the abstain guardrail.

The Watkins point this encodes: Kai's TECHNICAL learning is instant (it reads every
runbook before Monday), but CULTURAL knowledge only enters the index when a human
coaches it into data/skills/ — after which reindex() makes it retrievable.
"""
from __future__ import annotations

import re

import numpy as np

import config

_model = None


def _embedder():
    """Lazy-load the local embedding model (fastembed/ONNX, no PyTorch)."""
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        try:
            _model = TextEmbedding(model_name=config.EMBED_MODEL)
        except Exception:
            _model = TextEmbedding()  # fall back to fastembed's default model
    return _model


def embed(texts):
    """Embed strings -> (n, d) L2-normalised matrix; dot product == cosine similarity."""
    vecs = np.asarray(list(_embedder().embed(list(texts))), dtype=np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / np.clip(norms, 1e-8, None)


def load_corpus():
    """Runbooks + coached Skills -> list of (filename, text). Skills join the corpus
    only once an SME has written them (data/skills/) — coaching is explicit work."""
    docs = [(p.name, p.read_text(encoding="utf-8"))
            for p in sorted(config.RUNBOOKS_DIR.glob("*.md"))]
    docs += [(p.name, p.read_text(encoding="utf-8"))
             for p in sorted(config.SKILLS_DIR.glob("*.md"))]
    return docs


def _split_sections(text):
    """Cut at markdown headings so each rule/section stays one retrievable idea."""
    parts = re.split(r"(?m)^(#{1,6} .*)$", text)
    sections = []
    if parts[0].strip():
        sections.append(parts[0].strip())
    for i in range(1, len(parts), 2):
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((parts[i].strip() + "\n" + body).strip())
    return [s for s in sections if s]


def chunk_text(text, size=None, overlap=None):
    """Headings first; oversize sections packed by paragraph with an overlap tail."""
    size = size or config.CHUNK_CHARS
    overlap = overlap or config.CHUNK_OVERLAP
    chunks = []
    for sec in _split_sections(text):
        if len(sec) <= size:
            chunks.append(sec)
            continue
        cur = ""
        for p in [p.strip() for p in sec.split("\n\n") if p.strip()]:
            if cur and len(cur) + len(p) + 2 > size:
                chunks.append(cur)
                cur = ((cur[-overlap:] if overlap else "") + "\n\n" + p).strip()
            else:
                cur = (cur + "\n\n" + p).strip()
        if cur:
            chunks.append(cur)
    return chunks


class Index:
    """Transparent numpy vector store (production path: Chroma / pgvector / Qdrant)."""

    def __init__(self):
        self.ids, self.texts, self.vecs = [], [], None

    def build(self):
        ids, texts = [], []
        for name, text in load_corpus():
            # contextual chunk headers: a tiny section like "## Tolerance" can't be
            # found by cosine similarity on its own — prefixing the document title
            # gives every chunk enough context to compete. Bare title-only chunks
            # (a heading with no body) are dropped as retrieval noise.
            m = re.match(r"\s*#{1,2} (.+)", text)
            title = m.group(1).strip() if m else name
            for i, ch in enumerate(chunk_text(text)):
                if ch.lstrip().startswith("#") and len(ch.strip().splitlines()) <= 1:
                    continue
                ids.append(f"{name}#{i}")
                texts.append(ch if title.lower() in ch.lower() else f"[{title}]\n{ch}")
        self.ids, self.texts = ids, texts
        self.vecs = embed(texts) if texts else None
        return self

    reindex = build   # after coaching writes a new Skill, rebuild so it becomes retrievable

    def retrieve(self, query, k=None):
        """Top-k chunks by cosine similarity: [(chunk_id, text, score), ...]."""
        if self.vecs is None:
            return []
        k = k or config.TOP_K
        q = embed([query])[0]
        sims = self.vecs @ q
        order = np.argsort(-sims)[:k]
        return [(self.ids[i], self.texts[i], float(sims[i])) for i in order]

    def grounded(self, query, k=None):
        """Retrieve + apply the abstain guardrail.
        Returns (hits, abstained): below MIN_SCORE the teammate refuses to answer —
        'I don't have grounding for that' beats a confident hallucination."""
        hits = self.retrieve(query, k)
        abstained = (not hits) or (hits[0][2] < config.MIN_SCORE)
        return hits, abstained
