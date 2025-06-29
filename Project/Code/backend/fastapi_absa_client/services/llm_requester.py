import requests

HF_TOKEN = "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"  # Ou charge depuis variable d'env
API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"

def send_to_llm(summary_text: str, user_question: str) -> str:
    system_prompt = (
        "You are an intelligent assistant trained to interpret ABSA results "
        "from customer reviews and help users understand insights."
    )
    user_prompt = f"""Here are the ABSA results:\n{summary_text}\n\nUser question: "{user_question}" """

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 0.9
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
