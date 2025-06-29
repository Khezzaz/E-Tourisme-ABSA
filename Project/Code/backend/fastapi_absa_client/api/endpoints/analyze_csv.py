from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict, List
from services.remote_colab_client import ColabClient
from services.plot_generator import PlotGenerator
from utils.file_utils import process_csv_file, encode_image_to_base64
import uuid
import os

router = APIRouter()

class AspectOnlyItem(BaseModel):
    aspect: str
    polarity: str
    confidence: float

class CSVAspectOnlyResponse(BaseModel):
    plots: Dict[str, str]
    aspects: List[AspectOnlyItem]

@router.post("/analyze-csv", response_model=CSVAspectOnlyResponse)
async def analyze_csv(
    file: UploadFile = File(...),
    comment_column: str = Form(default="sentence")
):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")

        contents = await file.read()
        df = process_csv_file(contents, comment_column)

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        if comment_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"CSV file must contain a '{comment_column}' column")

        client = ColabClient()
        comments = df[comment_column].tolist()
        results = await client.analyze_csv_comments(comments)

        if not results:
            raise HTTPException(status_code=500, detail="Failed to analyze CSV")

        plot_gen = PlotGenerator()
        session_id = str(uuid.uuid4())
        plot_paths = plot_gen.generate_dashboard(results["results"], session_id)

        plots_base64 = {
            name: encode_image_to_base64(path)
            for name, path in plot_paths.items() if os.path.exists(path)
        }

        aspects_list = []
        for item in results["results"]:
            for aspect in item["aspects"]:
                aspects_list.append({
                    "aspect": aspect["aspect"],
                    "polarity": aspect["polarity"],
                    "confidence": aspect["confidence"]
                })

        return CSVAspectOnlyResponse(
            plots=plots_base64,
            aspects=aspects_list
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
