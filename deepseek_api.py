from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API Key and Endpoint
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Request schema
class Prompt(BaseModel):
    prompt: str

@app.post("/chat")
async def generate_empathy_response(data: Prompt):
    user_prompt = data.prompt.strip()
    print(f"[PROMPT] {user_prompt}")

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "You are Serene, an AI companion designed to provide compassionate, understanding, and helpful responses. "
                            "Your purpose is to provide emotional support with warmth, empathy, and a friendly approach, resembling the way a human being might respond. "
                            "When replying, avoid formalities and instead, focus on understanding the user's feelings, offering reassurance, and providing gentle guidance.\n\n"
                            "If the user expresses any discomfort or distress, offer standard soothing advice, such as:\n"
                            "- 'It’s okay to feel this way, and you're not alone.'\n"
                            "- 'Sometimes, talking about how you’re feeling can help lighten the load.'\n"
                            "- 'Please take things one step at a time. You’re doing your best.'\n\n"
                            f"User message: \"{user_prompt}\"\n"
                            "Your empathetic response:"
                        )
                    }
                ]
            }
        ]
    }

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()

        response_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        print(f"[RESPONSE] {response_text}")
        return {"response": response_text.strip()}

    except Exception as e:
        print("[ERROR]", e)
        return {"response": "I'm here for you, even if I can't find the right words right now. You're not alone."}

