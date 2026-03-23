import re
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Fish S2 Transformer Helper")


class TransformRequest(BaseModel):
    text: str
    mode: str = "balanced"
    tone_profile: str = "warm"


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def choose_opening(mode: str, tone_profile: str) -> str:
    tone = tone_profile.strip().lower()
    if mode == "instructional":
        return "[clear, professional]" if tone == "neutral" else "[clear, reassuring]"
    if mode == "dramatic":
        return "[low, focused]" if tone == "serious" else "[confident, vivid]"
    if mode == "supportive":
        return "[empathetic, calm]"
    return "[friendly, warm]" if tone != "serious" else "[serious, measured]"


def apply_inline_tags(sentence: str, is_first: bool) -> str:
    tagged = sentence
    tagged = re.sub(r"([.!?])", r"\1 [short pause]", tagged)
    tagged = re.sub(r"\b(important|critical|key)\b", r"[firm tone] \1", tagged, flags=re.IGNORECASE)
    tagged = re.sub(r"\b(great|awesome|amazing)\b", r"[excited] \1", tagged, flags=re.IGNORECASE)
    tagged = re.sub(r"\b(sorry|unfortunately)\b", r"[soft voice] \1", tagged, flags=re.IGNORECASE)
    tagged = re.sub(r"\b(but)\b", r"[short pause] \1", tagged, flags=re.IGNORECASE)
    if "?" in sentence:
        tagged = f"[curious] {tagged}"
    elif "!" in sentence:
        tagged = f"[energized] {tagged}"
    elif not is_first:
        tagged = f"[calm] {tagged}"
    return re.sub(r"\s+", " ", tagged).strip()


def transform_text(text: str, mode: str, tone_profile: str) -> str:
    raw = text.strip()
    if not raw:
        raise HTTPException(status_code=400, detail="text is required")

    sentences = split_sentences(raw)
    if not sentences:
        raise HTTPException(status_code=400, detail="text is required")

    opening = choose_opening(mode, tone_profile)
    transformed: list[str] = []
    for index, sentence in enumerate(sentences):
        line = apply_inline_tags(sentence, is_first=index == 0)
        if index == 0:
            line = f"{opening} {line}"
        transformed.append(line)
    return "\n\n".join(transformed)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/text/transform")
def transform(req: TransformRequest) -> dict:
    return {
        "text": req.text,
        "transformed_text": transform_text(req.text, req.mode, req.tone_profile),
        "mode": req.mode,
        "tone_profile": req.tone_profile,
    }
