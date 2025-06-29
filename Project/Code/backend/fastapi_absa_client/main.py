# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import analyze_comment, analyze_csv,chat_with_llm
import os

app = FastAPI(title="Restaurant ABSA API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static folder
os.makedirs("static/plots", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(analyze_comment.router, prefix="/api/v1")
app.include_router(analyze_csv.router, prefix="/api/v1")
app.include_router(chat_with_llm.router,prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Restaurant ABSA API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)