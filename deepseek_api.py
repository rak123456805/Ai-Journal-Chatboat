from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Serene AI Chat API", version="1.0.0")

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
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables")

GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Request schema
class PromptRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "Serene AI Chat API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api": "Serene Chat API"}

@app.post("/chat", response_model=ChatResponse)
async def generate_empathy_response(data: PromptRequest):
    user_prompt = data.prompt.lower().strip()
    print(f"[PROMPT] {user_prompt}")

    # Intelligent fallback responses based on user input
    def get_contextual_response(prompt):
        # Crisis detection keywords - highest priority
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'not worth living', 'want to die', 'kill my self', 'kill myself']
        violence_keywords = ['kill you', 'kill him', 'kill her', 'kill someone', 'hurt someone', 'kill my friend', 'kill hi']

        prompt_lower = prompt.lower()

        # Handle crisis situations - IMMEDIATE professional help
        if any(keyword in prompt_lower for keyword in crisis_keywords):
            responses = [
                "I'm really concerned about what you're saying, and I want you to know that you're not alone. Please reach out immediately to a crisis hotline. In India, you can call the Vandrevala Foundation Helpline at 1860 2662 345 or 1800 121 4567, or contact emergency services at 112. If you're in immediate danger, please go to the nearest hospital or call emergency services right now. Your life matters, and there are people who care about you and want to help.",
                "What you're sharing is very serious, and I'm glad you reached out. Please contact professional help immediately. In India, you can call AASRA at 9820466726, or the National Suicide Prevention Helpline at 9152987821. You're not alone in this struggle, and there are trained professionals who can provide the support you need right now.",
                "I hear the pain in your words, and it concerns me deeply. Please reach out immediately to professional help. Call the Sneha Foundation at 044-24640050 (India) or emergency services at 112. There are people trained to help you through this difficult time. You matter, and your life has value."
            ]
            return random.choice(responses)

        # Handle violence/threats
        elif any(keyword in prompt_lower for keyword in violence_keywords):
            responses = [
                "I need to be very clear here - any talk of harming yourself or others is taken seriously. If you're feeling violent thoughts, please reach out immediately to mental health professionals. In India, contact the National Mental Health Helpline at 1800-121-4567 or emergency services at 112. Violence is never the answer, and there are safer ways to handle these feelings.",
                "Threats of violence are concerning and need immediate attention. Please contact professional help right away. Call emergency services at 112 or mental health helplines. There are trained professionals who can help you work through these intense emotions safely.",
                "I'm concerned about the violent thoughts you're expressing. Please seek immediate professional help. Contact emergency services at 112 or mental health helplines like AASRA at 9820466726. Violence harms everyone involved, and there are safer ways to process these feelings."
            ]
            return random.choice(responses)

        # Keywords for different emotional states
        stress_keywords = ['stress', 'workload', 'overwhelmed', 'pressure', 'busy', 'tired', 'exhausted', 'burnout']
        sad_keywords = ['sad', 'depressed', 'unhappy', 'down', 'low', 'crying', 'tears', 'heartbroken', 'grief']
        anxiety_keywords = ['anxious', 'worried', 'nervous', 'scared', 'fear', 'panic', 'attack', 'phobia']
        motivation_keywords = ['motivation', 'motivate', 'inspire', 'encourage', 'goal', 'success', 'achieve']
        mental_health_keywords = ['mental health', 'mindfulness', 'therapy', 'counseling', 'wellbeing', 'meditation']
        relationship_keywords = ['relationship', 'breakup', 'divorce', 'love', 'heartbreak', 'friend', 'family']
        sleep_keywords = ['sleep', 'insomnia', 'tired', 'exhausted', 'restless']
        self_esteem_keywords = ['worthless', 'failure', 'not good enough', 'confidence', 'self esteem']

        # Check for stress/work-related issues
        if any(keyword in prompt_lower for keyword in stress_keywords):
            responses = [
                "Work stress can be incredibly overwhelming and affect every part of our lives. It's completely valid to feel this way when you're carrying heavy responsibilities. Let me share some practical strategies that have helped many people: First, try the Pomodoro technique - work for 25 focused minutes, then take a 5-minute break. Second, practice setting boundaries by learning to say 'no' to extra tasks when you're already at capacity. Third, consider talking to your supervisor about workload distribution. Remember, taking care of your mental health at work isn't selfish - it's necessary. What specific work situation is causing you the most stress right now?",
                "I hear how heavy that workload feels, and it's completely understandable to feel overwhelmed. Many successful people have been exactly where you are. Here's what research shows helps: 1) Break large tasks into micro-steps (5-10 minutes each), 2) Use the 'eat the frog' method - tackle your most dreaded task first when energy is highest, 3) Practice the 4-7-8 breathing technique for stress relief, and 4) Build in buffer time between tasks. You're stronger than you realize, and this stress is temporary. What would help you feel more in control right now?",
                "Work stress affects millions of people worldwide, and it's a sign that you care deeply about what you do. That's actually a strength, not a weakness. Let me suggest some immediate relief strategies: Take 2 minutes right now for deep breathing (inhale 4 counts, hold 4, exhale 6). Then, try writing down everything on your mind - this 'brain dump' can reduce mental load by 30-50%. Consider reaching out to a trusted colleague or mentor for support. You're not alone in this, and there are solutions. What one small step could you take today to reduce your stress?",
                "Feeling overwhelmed by work is your brain's way of signaling that you need support. This is actually a healthy response - it means you're human! Here's what evidence-based research shows helps: Regular short breaks (even 2-3 minutes) can restore focus and reduce burnout. Physical activity, even a 10-minute walk, releases endorphins that naturally combat stress. Consider creating a 'stress first-aid kit' with calming music, favorite snacks, or encouraging notes. Most importantly, remember that chronic stress without relief can lead to serious health issues. What boundaries could you set to protect your well-being?"
            ]
            return random.choice(responses)

        # Check for sadness/depression
        elif any(keyword in prompt_lower for keyword in sad_keywords):
            responses = [
                "I'm so sorry you're carrying this sadness - it sounds really heavy right now. Depression can make everything feel gray and hopeless, but please know that these feelings, while very real, are not permanent. Many people who feel exactly like you right now have found their way to brighter days. Would you be open to trying some gentle self-care? Even small things like drinking water, stepping into sunlight, or calling a friend can sometimes help shift the fog a little. You're not broken - you're hurting, and that's different. What usually brings you a tiny bit of comfort when you're feeling this way?",
                "Sadness can feel like a weight that colors everything in your world. It's brave that you're acknowledging it and reaching out. Research shows that sadness serves a purpose - it helps us process loss and change - but when it becomes overwhelming, we need support. Consider these evidence-based approaches: 1) Practice self-compassion (talk to yourself like you would a dear friend), 2) Connect with others (even a short call can help), 3) Try mood-boosting activities like walking in nature or listening to uplifting music. You're experiencing a universal human emotion, and it will pass. What would feel supportive to you right now?",
                "Your sadness matters, and I'm here to validate that it's okay to feel this way. Depression can make it hard to see hope, but that doesn't mean hope isn't there. Studies show that consistent small actions can gradually lift the fog: keeping a gratitude journal (even just one thing daily), regular sleep patterns, and gentle exercise. Consider reaching out to a trusted person or professional - you're not burdening them by sharing your pain. Many people find that talking about their feelings is the first step toward healing. What would make you feel a little less alone right now?",
                "Feeling deeply sad is exhausting and can make the world seem very dark. You're experiencing something that millions of people go through, and it doesn't make you weak - it makes you human. Let me share what has helped others: Create a 'comfort menu' of small, easy activities (hot tea, favorite blanket, calming music). Practice grounding techniques like naming 5 things you can see. Consider professional support - therapy can provide tools that last a lifetime. Your feelings are valid, and you deserve kindness, especially from yourself. What small act of self-care feels possible today?"
            ]
            return random.choice(responses)

        # Check for anxiety/worry
        elif any(keyword in prompt_lower for keyword in anxiety_keywords):
            responses = [
                "Anxiety can feel like your mind is racing ahead without you, creating all sorts of 'what if' scenarios. This is your brain's alarm system working overtime, but there are ways to help it calm down. Try this immediate technique: Place one hand on your chest and one on your belly. Take slow breaths - make sure the hand on your belly rises more than the one on your chest. This signals to your brain that you're safe. What thoughts are causing you the most anxiety right now? Sometimes naming them specifically can reduce their power.",
                "I understand how anxiety can make everything feel urgent and threatening. It's like your survival instincts are stuck in overdrive. Here's a technique that helps many people: The 5-4-3-2-1 grounding exercise - name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. This brings your attention back to the present moment where you're actually safe. What evidence do you have that you're safe right now? Would you like to explore some longer-term strategies for managing anxiety?",
                "Anxiety attacks can feel terrifying and uncontrollable, but they are actually your body's natural response to perceived threat. The good news is that there are proven techniques to help manage them. Try the 'container technique': Imagine putting your anxious thoughts into a container that you can close and set aside for later. Then focus on something neutral in your environment. Research shows that regular practice of mindfulness or progressive muscle relaxation can significantly reduce anxiety over time. You're not alone in this - anxiety affects 1 in 4 people. What coping strategies have worked for you in the past?",
                "Worrying thoughts can spiral and make it hard to focus on anything else. This is a common experience, but there are ways to interrupt the cycle. Try the 'worry time' technique: Set aside 15-20 minutes daily as 'worry time' where you allow yourself to worry freely. Outside that time, when worries arise, gently remind yourself 'not now' and return to the present. Also, consider whether your worries are solvable (if so, make a plan) or unsolvable (if so, practice acceptance). What specific worry is occupying your mind most right now? Breaking it down might help."
            ]
            return random.choice(responses)

        # Check for motivation requests
        elif any(keyword in prompt_lower for keyword in motivation_keywords):
            responses = [
                "You have incredible potential within you - it's not about finding motivation, it's about connecting with your 'why.' Think about what truly matters to you deep down. What activities make you lose track of time? What impact do you want to have on the world? Once you connect with your core values, motivation becomes more sustainable. Remember, every expert was once a beginner who kept showing up. What small, meaningful step could you take today toward something that matters to you?",
                "Motivation isn't constant - it's more like a muscle that needs regular exercise. The key is creating systems that work even when motivation is low. Try the '2-minute rule': Commit to working on something for just 2 minutes. Usually, once you start, momentum carries you forward. Also, focus on progress over perfection. Celebrate small wins and learn from setbacks. What would make today feel like a success, even if it's something small? Building momentum through tiny victories creates lasting change.",
                "Success comes from consistent action, not giant leaps. Think of it like compound interest - small daily actions create massive results over time. Research shows that people who focus on systems rather than goals are more successful. Instead of 'lose 20 pounds,' try 'weigh myself daily and eat vegetables with every meal.' What systems could you put in place to support your goals? Remember, you're already taking a positive step by thinking about your motivation and reaching out for support.",
                "You are capable of amazing things - your brain is wired for growth and adaptation. The difference between successful people and others is often just consistent effort over time. Try reframing challenges as opportunities to grow stronger. When motivation dips (and it will), focus on your identity: 'I am someone who shows up,' rather than 'I need to be motivated.' What would the most motivated version of yourself do right now? Start there, even if it's just for 5 minutes. Small actions build momentum and confidence."
            ]
            return random.choice(responses)

        # Check for mental health advice
        elif any(keyword in prompt_lower for keyword in mental_health_keywords):
            responses = [
                "Taking care of your mental health is one of the most important investments you can make. Research consistently shows that mental wellness affects physical health, relationships, and productivity. Start with basics: aim for 7-9 hours of quality sleep, regular movement (even 10-minute walks help), and nutritious food. Practice mindfulness through apps like Headspace or Calm, or simply focus on your breath for 2 minutes daily. Consider therapy - platforms like BetterHelp or local counselors can provide professional support. What aspect of your mental health would you like to focus on first?",
                "Mental health maintenance requires consistent, gentle care - think of it as tending a garden rather than a quick fix. Evidence-based practices include: 1) Regular exercise (releases endorphins and reduces stress hormones), 2) Strong social connections (loneliness is as harmful as smoking), 3) Sleep hygiene (consistent schedule, cool dark room), 4) Stress management techniques like journaling or meditation. Professional help through therapy can provide personalized tools. Remember, seeking help is a sign of strength. What daily practices could you incorporate to support your mental well-being?",
                "Your mental health matters just as much as your physical health. Studies show that untreated mental health issues can lead to physical health problems, but the reverse is also true - improving mental health can boost physical health. Consider creating a 'mental health toolkit': calming music, grounding objects, emergency contacts, and coping strategies. Apps like Moodpath or Sanvello can help track patterns. Therapy provides tools that last a lifetime. What would make you feel more supported in your mental health journey right now?",
                "Mental wellness is a skill that can be developed with practice. Research from positive psychology shows that certain activities reliably increase well-being: acts of kindness, gratitude practices, physical exercise, and meaningful social connections. Consider starting a 'joy journal' where you note three good things daily. Professional support through counseling can help process deeper issues. Remember, mental health challenges are common - 1 in 4 people experience them annually. What small change could you make today to support your mental health?"
            ]
            return random.choice(responses)

        # Check for relationship issues
        elif any(keyword in prompt_lower for keyword in relationship_keywords):
            responses = [
                "Relationships can bring our deepest joys and most profound pains. Heartbreak and conflict are universal experiences that test our resilience. Remember that all relationships teach us something about ourselves and what we value. Give yourself time to grieve losses, but also permission to heal and grow. Consider what this experience might be teaching you about your needs and boundaries. What support do you need right now as you navigate these feelings?",
                "Relationship challenges often mirror our deepest insecurities and hopes. Whether it's a breakup, family conflict, or friendship issues, these experiences help us understand ourselves better. Practice self-compassion during this time - treat yourself with the same kindness you'd offer a dear friend. Consider journaling about what you've learned and what you want in future relationships. Professional counseling can provide valuable tools for processing these emotions. What feels most painful about this situation right now?",
                "Human connections are central to our well-being, so relationship difficulties can feel devastating. Research shows that while social support is crucial for mental health, the quality of relationships matters more than quantity. Focus on nurturing connections that are mutually supportive and respectful. If you're experiencing toxic relationships, setting boundaries or seeking distance may be necessary for your well-being. Consider talking to a trusted friend or counselor about your experiences. What kind of support would be most helpful to you right now?"
            ]
            return random.choice(responses)

        # Check for sleep issues
        elif any(keyword in prompt_lower for keyword in sleep_keywords):
            responses = [
                "Sleep issues can create a vicious cycle that affects everything from mood to concentration. Poor sleep is linked to increased anxiety, depression, and even physical health problems. Try creating a 'sleep sanctuary': cool, dark, quiet room with comfortable bedding. Avoid screens 1 hour before bed (blue light suppresses melatonin). Establish a consistent sleep schedule, even on weekends. Consider relaxation techniques like progressive muscle relaxation. If insomnia persists, consult a healthcare provider. What specific sleep challenges are you facing?",
                "Quality sleep is foundational to mental health - it's when our brains process emotions and consolidate memories. Sleep deprivation can make everything feel worse. Evidence-based tips: Keep your bedroom cool (65-68°F/18-20°C), avoid caffeine after 2 PM, and create a pre-sleep routine (reading, light stretching). Apps like Sleep Cycle can help track patterns. If you wake up worried, try writing concerns down to 'park' them until morning. Chronic sleep issues may need professional evaluation. What changes could you make to improve your sleep environment?"
            ]
            return random.choice(responses)

        # Check for self-esteem issues
        elif any(keyword in prompt_lower for keyword in self_esteem_keywords):
            responses = [
                "Feeling worthless or like a failure is a painful experience that many people go through, often because we've internalized critical voices from our past. The truth is, your worth isn't determined by achievements, productivity, or others' approval - it's inherent. Try practicing self-compassion: speak to yourself as you would a cherished friend. Challenge negative self-talk by asking 'Would I say this to someone I care about?' Consider therapy to work through underlying beliefs. What evidence do you have that contradicts these negative thoughts about yourself?",
                "Low self-esteem can feel like carrying an invisible weight that colors every experience. It's often rooted in past experiences or critical environments. Cognitive behavioral techniques can help: identify negative thought patterns and replace them with balanced alternatives. For example, instead of 'I'm a failure,' try 'I made a mistake, and that's an opportunity to learn.' Build self-esteem through small acts of self-care and accomplishments. Professional support can help rewire these deep-seated beliefs. What would you say to a friend who was feeling this way about themselves?"
            ]
            return random.choice(responses)

        # Bot identity questions
        elif any(word in prompt_lower for word in ['robot', 'bot', 'ai', 'artificial', 'human', 'real']):
            responses = [
                "I'm Serene, an AI companion designed specifically to provide empathetic support for mental health and emotional well-being. While I'm not human, I draw from extensive research in psychology, therapeutic techniques, and evidence-based practices to offer meaningful support. Many people find AI companions helpful for initial conversations, processing emotions, and learning coping strategies. That said, I'm not a replacement for professional mental health care. If you're in crisis or need personalized therapy, please reach out to qualified professionals. What brings you here today?",
                "I'm an AI mental health companion created to offer supportive, non-judgmental conversations. My responses are based on established psychological principles, therapeutic approaches, and research in mental health. While I can provide information, validation, and coping strategies, I'm not a licensed therapist and can't provide clinical diagnosis or treatment. Think of me as a supportive friend who can listen and offer evidence-based suggestions. For professional help, please consult qualified mental health professionals. How can I support you today?"
            ]
            return random.choice(responses)

        # Default empathetic responses for unrecognized input
        else:
            responses = [
                "Thank you for sharing that with me. It takes real courage to open up about what's on your mind. I'm here to listen without judgment and offer support based on what you've shared. Everyone's experiences are unique, and there's no 'right' way to feel. What would be most helpful for you right now - talking through your thoughts, learning some coping strategies, or just having someone acknowledge how you're feeling?",
                "I appreciate you reaching out and sharing what's on your mind. Your feelings and experiences matter, and it's important to have a safe space to express them. I'm trained to provide empathetic support and can draw from evidence-based approaches to help. Whether you're dealing with stress, sadness, anxiety, or just need someone to listen, I'm here. What aspect of what you're going through would you like to focus on or get support with?",
                "You're not alone in this experience - many people go through similar challenges and feelings. It's brave that you're acknowledging them and seeking support. I can offer validation, practical coping strategies, and a listening ear based on psychological research and therapeutic approaches. There's no pressure to share more than you're comfortable with. What feels most important or urgent for you to address right now?",
                "I hear you, and I want you to know that your thoughts and feelings are valid. Everyone deserves understanding and support, especially during difficult times. I'm here to provide that - drawing from established mental health practices and research. Whether you want to process emotions, learn new coping skills, or just have someone bear witness to your experience, I'm here. What would feel most supportive in this moment?",
                "Thank you for trusting me with your thoughts. Mental health challenges are common, and seeking support is a sign of strength and self-awareness. I can offer evidence-based suggestions, validation, and compassionate listening. Research shows that talking about our experiences can help process emotions and reduce feelings of isolation. What would you like to focus on - your current feelings, coping strategies, or just having a safe space to express yourself?"
            ]
            return random.choice(responses)

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        # Use intelligent contextual responses when API key is missing or placeholder
        response_text = get_contextual_response(user_prompt)
        print(f"[INTELLIGENT FALLBACK] {response_text}")
        return ChatResponse(response=response_text)

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
        response = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            print(f"[GEMINI RESPONSE] {response_text}")
            return ChatResponse(response=response_text.strip())
        else:
            raise HTTPException(status_code=500, detail="Invalid response from Gemini API")

    except requests.exceptions.RequestException as e:
        print(f"[API ERROR] {e}")
        # Use intelligent contextual responses when API fails
        response_text = get_contextual_response(user_prompt)
        print(f"[CONTEXTUAL FALLBACK] {response_text}")
        return ChatResponse(response=response_text)
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        # Final fallback
        response_text = "I'm here for you. Sometimes technology has its moments, but that doesn't change the fact that your feelings matter. Would you like to share more about what's on your mind?"
        return ChatResponse(response=response_text)
