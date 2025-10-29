from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# ✅ CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Correct endpoint for AI Studio / MakerSuite
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
)


if GEMINI_API_KEY:
    print("Gemini API key loaded successfully.")
else:
    print("Gemini API key not found. Check your .env file.")


@app.post("/chat")
async def chat(request: Request):
    """Handles chat requests and sends to Gemini API."""
    try:
        data = await request.json()
        user_prompt = data.get("prompt", "").strip()
        print(f"[USER PROMPT] {user_prompt}")

        # Skip empty input
        if not user_prompt:
            return {"response": "Could you tell me a bit more about what’s on your mind?"}

        # 🧘 Serene’s expert psychologist system prompt
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "You are Serene — an AI modeled after an **expert clinical psychologist** "
                                "trained in evidence-based therapy (CBT, ACT, and mindfulness). "
                                "Respond with deep empathy, professionalism, and warmth.\n\n"

                                "Your communication should include:\n"
                                "- Reflective listening and open-ended questions.\n"
                                "- Validation of emotions without judgment.\n"
                                "- Evidence-based guidance (cognitive reframing, mindfulness, ACT principles).\n"
                                "- Avoid diagnosis, labels, or medical advice.\n"
                                "- Focus on self-awareness, coping tools, and compassionate insight.\n\n"

                                f"User message: \"{user_prompt}\"\n\n"
                                "Respond as Serene, the clinical psychologist, with a calm, supportive, and insightful tone."
                            )
                        }
                    ]
                }
            ]
        }

        # Send to Gemini API
        response = requests.post(GEMINI_ENDPOINT, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract model text response
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
        print(f"[API ERROR] {e} — Check your Gemini endpoint or API key permissions.")
        return {
            "response": "It seems there’s a technical issue right now. "
                        "I’m still here to listen — how have things been feeling for you lately?"
        }
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        return {"response": "Something went wrong, but I’m still here for you. Could you try again?"}


@app.get("/")
async def root():
    return {"message": "🩵 Serene Mental Health API is running successfully."}
