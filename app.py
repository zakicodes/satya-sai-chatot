"""
Flask API for the Shri Satya Sai Blood Centre chatbot.
Run with: python app.py
Serves:
  - GET  /                -> the landing page (with chat widget)
  - POST /chat            -> {"message": "..."} -> {"reply": "..."}

Uses the AI engine (chatbot_ai_engine.py) if ANTHROPIC_API_KEY is set,
otherwise falls back to the free local matching engine (chatbot_engine.py).
"""

from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import secrets

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))
CORS(app, supports_credentials=True)  # allows your website (different domain) to call this API

USE_AI = bool(os.environ.get("GROQ_API_KEY"))

if USE_AI:
    from chatbot_ai_engine import BloodBankBot
    bot = BloodBankBot()
else:
    from chatbot_engine import BloodBankBot
    bot = BloodBankBot()

MAX_HISTORY_TURNS = 8  # keep last N message pairs per visitor, to limit token usage


@app.route("/")
def home():
    return send_from_directory("static", "landing.html")


@app.route("/chat-widget-demo")
def chat_only():
    return send_from_directory("static", "index.html")


@app.route("/demo")
def demo():
    return send_from_directory("static", "demo-website.html")


@app.route("/chat-widget.js")
def widget_script():
    return send_from_directory("static", "chat-widget.js")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = data.get("message", "")

    if USE_AI:
        history = session.get("history", [])
        reply = bot.get_response(user_message, history=history)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": reply})
        session["history"] = history[-(MAX_HISTORY_TURNS * 2):]
    else:
        reply = bot.get_response(user_message)

    return jsonify({"reply": reply})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "ai_enabled": USE_AI})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
