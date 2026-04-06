from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API endpoint (Use gemini-1.5-flash for stability)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
)

# Print API load status (no emojis for Windows console)
if GEMINI_API_KEY:
    print("Gemini API key loaded successfully.")
else:
    print("Gemini API key not found. Check your .env file.")


@app.post("/chat")
async def chat(request: Request):
    """Handles chat requests and sends to Gemini API."""
    try:
        data = await request.json()
        user_prompt = data.get("prompt", "").strip()  # ✅ FIXED trim() → strip()
        print(f"[USER PROMPT] {user_prompt}")

        if not user_prompt:
            return {"response": "Could you tell me a bit more about what’s on your mind?"}

        # Serene system prompt (expert psychologist behavior)
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "You are Serene — an AI modeled after an expert clinical psychologist "
                                "trained in CBT, ACT, and mindfulness. "
                                "Respond with empathy and evidence-based guidance.\n\n"
                                f"User message: \"{user_prompt}\"\n\n"
                                "Respond calmly, professionally, and supportively."
                            )
                        }
                    ]
                }
            ]
        }

        response = requests.post(GEMINI_ENDPOINT, json=payload)
        response.raise_for_status()
        result = response.json()

        model_output = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if not model_output:
            return {"response": "I'm here and listening — could you tell me a little more?"}

        return {"response": model_output}

    except requests.exceptions.HTTPError as e:
        print(f"[API ERROR] {e}")
        return {
            "response": "It seems there’s a technical issue right now. "
                        "I'm still here — how have things been feeling for you lately?"
        }
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        return {"response": "Something went wrong, but I'm here for you. Can you try again?"}


@app.get("/")
async def root():
    return {"message": "Serene Mental Health API is running successfully."}
