from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from collections import Counter, defaultdict
from typing import List
from services.llm_requester import send_to_llm

router = APIRouter()

class AspectItem(BaseModel):
    aspect: str
    polarity: str  # "positive", "negative", "neutral"

class ChatRequest(BaseModel):
    aspects: List[AspectItem]
    question: str

@router.post("/chat-with-llm")
def chat_with_llm(data: ChatRequest):
    # 1. Count polarities per aspect
    aspect_counts = defaultdict(lambda: {"positive": 0, "negative": 0, "neutral": 0})
    aspect_freq = Counter()

    for item in data.aspects:
        aspect_counts[item.aspect][item.polarity] += 1
        aspect_freq[item.aspect] += 1

    # 2. Select top 8 frequent aspects
    top_aspects = [aspect for aspect, _ in aspect_freq.most_common(8)]

    # 3. Format summary string
    summary_lines = []
    for aspect in top_aspects:
        counts = aspect_counts[aspect]
        line = f"- Aspect: {aspect} → {counts['positive']} positive, {counts['negative']} negative, {counts['neutral']} neutral"
        summary_lines.append(line)
    
    summary_text = "\n".join(summary_lines)

    try:
        llm_response = send_to_llm(summary_text, data.question)
        return {"response": llm_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
