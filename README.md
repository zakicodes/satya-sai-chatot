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

## 5. Improving the bot later

- Add more `training_phrases` for anything the bot misunderstands
- Add Marathi/Hindi phrases if most users type in those languages
- Connect it to WhatsApp Business API for wider reach
- Add a live blood-inventory lookup if you start tracking stock digitally
