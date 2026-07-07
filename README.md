# Shri Satya Sai Blood Centre — Chatbot

A simple chatbot that answers common questions (address, timings, donation
process, eligibility, contact) using the data in `chatbot_data.json`.

## Files

- `chatbot_data.json` — all the bot's knowledge (edit this to update answers)
- `chatbot_engine.py` — matches user messages to the right response
- `app.py` — Flask web server that exposes the bot as an API
- `static/index.html` — the chat widget people will actually see and use
- `requirements.txt` — Python packages needed

## 1. Run it on your own computer first

1. Install Python 3.9+ if you don't have it.
2. Open a terminal in this folder and install the packages:
   ```
   pip install -r requirements.txt
   ```
3. Test it in the terminal (no web needed):
   ```
   python chatbot_engine.py
   ```
   Type messages and see replies. Type `quit` to stop.

4. Run the full web version:
   ```
   python app.py
   ```
   Then open your browser to **http://localhost:5000** — you'll see the
   chat widget talking to your bot.

## 2. Update the bot's answers

Everything the bot knows lives in `chatbot_data.json`. To change an
answer or add a new question it should understand, edit that file:

- `training_phrases` — example things a user might type
- `responses` — what the bot replies with

No code changes needed — just edit the JSON and restart `app.py`.

## 3. Put it on a live website (so anyone can use it)

Right now the bot only runs on your computer. To make it public, you
need to host `app.py` somewhere online. Easiest free/cheap options:

### Option A: Render.com (recommended, free tier available)
1. Create a free account at https://render.com
2. Push this folder to a GitHub repository
3. In Render, click "New +" → "Web Service", connect your GitHub repo
4. Set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py`
5. Deploy. Render will give you a URL like
   `https://satya-sai-bot.onrender.com`

### Option B: PythonAnywhere (also free tier)
Good if you prefer uploading files directly instead of using GitHub.

### After hosting the backend
Open `static/index.html` and change this line near the bottom:
```js
const API_URL = "http://localhost:5000/chat";
```
to your live URL, e.g.:
```js
const API_URL = "https://satya-sai-bot.onrender.com/chat";
```

## 4. Add the floating chat widget to your website

`static/chat-widget.js` is a self-contained floating chat bubble
(bottom-right corner of the page). It builds its own HTML/CSS — you
don't need to write any of that yourself.

**Step 1:** Upload `chat-widget.js` to your website's files (anywhere,
e.g. the same folder as your homepage).

**Step 2:** Add this one line just before `</body>` on every page you
want the bubble to appear on:
```html
<script src="chat-widget.js" data-api="https://YOUR-BACKEND-URL/chat"></script>
```
Replace `YOUR-BACKEND-URL` with your live Render (or PythonAnywhere)
URL from Step 3 below, keeping the `/chat` at the end.

That's it. A red chat bubble will appear in the corner, and clicking
it opens the chat window with quick-reply buttons for Address,
Donate blood, Timings, and Contact.

**Try it locally first:** with `app.py` running, open
`http://localhost:5000/demo` — this loads a stand-in webpage with the
widget embedded, exactly as it would look on your real site.

## 6. Upgrade to AI-powered answers (optional, free)

By default the bot only matches your training phrases. To make it genuinely
understand *any* question — while still knowing your real business facts —
you can connect it to a free AI model via Groq.

**Step 1: Get a free API key**
1. Go to https://console.groq.com and sign up (no credit card needed)
2. Go to "API Keys" → "Create API Key"
3. Copy the key (starts with `gsk_...`)

**Step 2: Add it as an environment variable**

Locally, before running `python app.py`:
```
# Windows PowerShell
$env:GROQ_API_KEY="gsk_your_key_here"
python app.py

# Mac/Linux
export GROQ_API_KEY="gsk_your_key_here"
python app.py
```

On Render: go to your service → "Environment" tab → "Add Environment
Variable" → Key: `GROQ_API_KEY`, Value: your key → Save. Render will
redeploy automatically.

**That's it.** Once the key is set, `/health` will show `"ai_enabled": true`,
and the bot will start answering naturally using the AI, while still
grounded in your address, hours, and donation info from `chatbot_data.json`.
If the key is ever removed or the API is unreachable, it automatically
falls back to the free local matching engine — the bot never goes offline.
