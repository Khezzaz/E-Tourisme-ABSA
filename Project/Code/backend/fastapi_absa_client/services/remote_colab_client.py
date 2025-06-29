import httpx
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()
NGROK_URL = os.getenv("NGROK_URL")

class ColabClient:
    def __init__(self):
        if not NGROK_URL:
            raise ValueError("NGROK_URL is not set in environment variables.")
        self.ngrok_url = NGROK_URL.rstrip('/')
        self.timeout = 300

    async def analyze_single_comment(self, comment: str) -> Optional[Dict]:
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.ngrok_url}/predict-text",
                    json={"sentence": comment}
                )
                if response.status_code == 200:
                    result = response.json()  # result is a list of aspects
                    processing_time = time.time() - start_time
                    aspects = []
                    for aspect_data in result:
                        aspects.append({
                            "aspect": aspect_data.get("aspect", ""),
                            "polarity": aspect_data.get("sentiment", "neutral"),  # corrected key
                            "confidence": aspect_data.get("confidence", 0.0)
                        })
                    return {
                        "aspects": aspects,
                        "processing_time": processing_time
                    }
                return None
        except Exception as e:
            print(f"Error in analyze_single_comment: {e}")
            return None

    async def analyze_csv_comments(self, comments: List[str]) -> Optional[Dict]:
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.ngrok_url}/predict-file",
                    json={"comments": comments}
                )
                if response.status_code == 200:
                    raw = response.json()  # dict attendu avec 'results'
                    processing_time = time.time() - start_time

                    all_aspects = []
                    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
                    processed_results = []

                    for comment_result in raw.get("results", []):
                        sentence = comment_result.get("sentence", "")
                        processed_aspects = []
                        for aspect in comment_result.get("aspects", []):
                            polarity = aspect.get("sentiment", "neutral")  # correspondance avec la clé 'sentiment'
                            mapped = {
                                "aspect": aspect.get("aspect", ""),
                                "polarity": polarity,
                                "confidence": aspect.get("confidence", 0.0)
                            }
                            processed_aspects.append(mapped)
                            all_aspects.append(mapped)
                            if polarity in sentiment_counts:
                                sentiment_counts[polarity] += 1

                        processed_results.append({
                            "sentence": sentence,
                            "aspects": processed_aspects
                        })

                    summary = {
                        "total_aspects": len(all_aspects),
                        "sentiment_distribution": sentiment_counts,
                        "top_aspects": self._get_top_aspects(all_aspects)
                    }

                    return {
                        "results": processed_results,
                        "processing_time": processing_time,
                        "summary": summary
                    }
                return None
        except Exception as e:
            print(f"Error in analyze_csv_comments: {e}")
            return None

    def _get_top_aspects(self, aspects: List[Dict]) -> List[Dict]:
        aspect_counts = {}
        for aspect in aspects:
            name = aspect.get("aspect", "")
            if name:
                aspect_counts[name] = aspect_counts.get(name, 0) + 1

        sorted_aspects = sorted(aspect_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"aspect": aspect, "count": count} for aspect, count in sorted_aspects[:8]]
