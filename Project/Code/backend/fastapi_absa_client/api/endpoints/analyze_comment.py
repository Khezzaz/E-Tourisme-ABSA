from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.remote_colab_client import ColabClient

router = APIRouter()

class CommentRequest(BaseModel):
    sentence: str

class AspectResult(BaseModel):
    aspect: str
    polarity: str
    confidence: float

class CommentResponse(BaseModel):
    sentence: str
    aspects: List[AspectResult]
    processing_time: float

@router.post("/analyze-comment", response_model=CommentResponse)
async def analyze_comment(request: CommentRequest):
    try:
        client = ColabClient()
        result = await client.analyze_single_comment(request.sentence)

        if not result:
            raise HTTPException(status_code=500, detail="Failed to analyze sentence")

        return CommentResponse(
            sentence=request.sentence,
            aspects=result["aspects"],
            processing_time=result["processing_time"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
