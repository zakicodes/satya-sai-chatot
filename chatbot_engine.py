"""
Core chatbot logic for Shri Satya Sai Blood Centre.
Loads chatbot_data.json and matches user input to the closest training
phrase using simple word-overlap scoring (no heavy ML libraries needed,
so it installs instantly on any computer).
"""

import json
import random
import re
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "chatbot_data.json")
CONFIDENCE_THRESHOLD = 0.2  # below this, use fallback response

STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "do", "does", "did", "i", "you",
    "your", "my", "me", "to", "of", "for", "please", "can", "could",
    "what", "where", "when", "how", "will", "would", "it", "this", "that",
}


def tokenize(text: str):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return [w for w in words if w not in STOPWORDS]


class BloodBankBot:
    def __init__(self, data_path: str = DATA_PATH):
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        # Pre-tokenize every training phrase once, up front.
        self.phrase_tokens = []   # list of token-sets
        self.phrase_intents = []  # matching intent index for each phrase

        for idx, intent in enumerate(self.data["intents"]):
            for phrase in intent["training_phrases"]:
                tokens = set(tokenize(phrase))
                if tokens:
                    self.phrase_tokens.append(tokens)
                    self.phrase_intents.append(idx)

    def _score(self, user_tokens: set, phrase_tokens: set) -> float:
        if not user_tokens or not phrase_tokens:
            return 0.0
        overlap = len(user_tokens & phrase_tokens)
        union = len(user_tokens | phrase_tokens)
        return overlap / union if union else 0.0

    def get_response(self, user_message: str) -> str:
        if not user_message.strip():
            return "Please type a message so I can help you."

        user_tokens = set(tokenize(user_message))

        best_score = 0.0
        best_intent_idx = None
        for tokens, intent_idx in zip(self.phrase_tokens, self.phrase_intents):
            score = self._score(user_tokens, tokens)
            if score > best_score:
                best_score = score
                best_intent_idx = intent_idx

        if best_intent_idx is None or best_score < CONFIDENCE_THRESHOLD:
            return random.choice(self.data["fallback"]["responses"])

        responses = self.data["intents"][best_intent_idx]["responses"]
        return random.choice(responses)

    def get_business_info(self) -> dict:
        return self.data.get("business_info", {})


if __name__ == "__main__":
    # Quick terminal test — run: python chatbot_engine.py
    bot = BloodBankBot()
    print("Shri Satya Sai Blood Centre Bot (type 'quit' to exit)\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            print("Bot: Thank you! Take care.")
            break
        print("Bot:", bot.get_response(user_input))

