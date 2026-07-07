"""
AI-powered chatbot for Shri Satya Sai Blood Centre.
 
Instead of only matching fixed phrases, this calls an AI model (via Groq's
free API) so it can genuinely understand and answer any question a visitor
asks — while staying grounded in your real business facts (address, hours,
donation process, etc.) which are fed to it as context every time.
 
Requires an environment variable: GROQ_API_KEY
Get a free key at https://console.groq.com (no credit card needed).
See README.md for setup steps.
"""
 
import json
import os
import requests
 
DATA_PATH = os.path.join(os.path.dirname(__file__), "chatbot_data.json")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"  # free tier on Groq, fast + capable
 
 
def _load_business_context() -> str:
    """Turn chatbot_data.json into plain-text reference material for the AI."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    info = data.get("business_info", {})
    lines = [
        f"Business name: {info.get('name')} ({info.get('branch')} branch)",
        f"Category: {info.get('category')}",
        f"City: {info.get('city')}, {info.get('state')}",
        f"Address: {info.get('address')}",
        f"Phone: {info.get('phone')}",
        f"Hours: {info.get('hours')}",
        f"Google rating: {info.get('rating')} ({info.get('review_count')} reviews)",
        f"Facebook: {info.get('facebook')}",
        f"Facilities: {', '.join(info.get('facilities', []))}",
        "",
        "Known question-and-answer topics (use these as ground truth facts,",
        "but you don't have to repeat them word-for-word — answer naturally):",
    ]
 
    for intent in data.get("intents", []):
        example_q = intent["training_phrases"][0] if intent["training_phrases"] else ""
        example_a = intent["responses"][0] if intent["responses"] else ""
        lines.append(f"- Q: {example_q}\n  A: {example_a}")
 
    return "\n".join(lines)
 
 
BUSINESS_CONTEXT = _load_business_context()
 
SYSTEM_PROMPT = f"""You are the helpful chat assistant for Shri Satya Sai Blood Centre,
a blood donation centre in Cidco, Chhatrapati Sambhajinagar, Maharashtra.
 
Here are the real facts about this business — always stay accurate to these,
never invent details that aren't here or in the conversation:
 
{BUSINESS_CONTEXT}
 
Guidelines:
- Be warm, concise, and helpful — like a knowledgeable staff member, not a corporate script.
- Answer general questions about blood donation even if not explicitly listed above
  (e.g. "does donating blood hurt", "is it safe"), using accurate general medical
  knowledge, but always defer specifics about this centre to a phone call.
- For anything urgent, an emergency, or specific medical eligibility you're not
  certain about, direct the person to call 09168104104 rather than guessing.
- If someone asks something totally unrelated to the blood centre or blood
  donation (e.g. sports scores, unrelated general trivia), politely redirect
  them back to how you can help with blood donation topics — don't just refuse
  outright, but don't go down unrelated rabbit holes either.
- Keep answers short — a few sentences at most, this is a chat widget, not an essay.
- Never make up medical guarantees or diagnoses.
"""
 
 
class BloodBankBot:
    """AI-backed bot using Groq's free API. Falls back to a plain message on error."""
 
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY", "")
 
    def get_response(self, user_message: str, history: list | None = None) -> str:
        if not user_message.strip():
            return "Please type a message so I can help you."
 
        if not self.api_key:
            return (
                "The chatbot's AI isn't configured yet — please set the "
                "GROQ_API_KEY environment variable (see README.md)."
            )
 
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history or [])
        messages.append({"role": "user", "content": user_message})
 
        try:
            response = requests.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": 400,
                    "messages": messages,
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException:
            return (
                "Sorry, I'm having trouble reaching my AI service right now. "
                "Please call us directly at 09168104104 for immediate help."
            )
 
    def get_business_info(self) -> dict:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("business_info", {})
 
 
if __name__ == "__main__":
    bot = BloodBankBot()
    print("Shri Satya Sai Blood Centre AI Bot (type 'quit' to exit)\n")
    conversation = []
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            print("Bot: Thank you! Take care.")
            break
        reply = bot.get_response(user_input, history=conversation)
        print("Bot:", reply)
        conversation.append({"role": "user", "content": user_input})
        conversation.append({"role": "assistant", "content": reply})
 


