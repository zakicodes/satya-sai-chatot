from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot_engine import BloodBankBot
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # allows your website (different domain) to call this API

bot = BloodBankBot()


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
    reply = bot.get_response(user_message)
    return jsonify({"reply": reply})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
