/**
 * Shri Satya Sai Blood Centre — Floating Chat Widget
 *
 * How to use:
 * Add this single line before </body> on any page of your website:
 *
 *   <script src="chat-widget.js" data-api="https://YOUR-BACKEND-URL/chat"></script>
 *
 * Replace YOUR-BACKEND-URL with your deployed app.py URL (see README).
 * That's it — no other HTML/CSS needed, this script builds everything.
 */

(function () {
  const scriptTag = document.currentScript;
  const API_URL = scriptTag.getAttribute("data-api") || "http://localhost:5000/chat";

  // ---------- Styles ----------
  const style = document.createElement("style");
  style.textContent = `
    :root {
      --ssb-red: #B3232D;
      --ssb-red-dark: #8C1B23;
      --ssb-cream: #FBF7F4;
      --ssb-ink: #241A1A;
      --ssb-line: #E6D9D6;
    }
    #ssb-bubble {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--ssb-red), var(--ssb-red-dark));
      box-shadow: 0 8px 24px rgba(140,27,35,0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 999998;
      transition: transform 0.2s ease;
    }
    #ssb-bubble:hover { transform: scale(1.06); }
    #ssb-bubble svg { width: 28px; height: 28px; }

    #ssb-window {
      position: fixed;
      bottom: 96px;
      right: 24px;
      width: 340px;
      max-width: calc(100vw - 32px);
      height: 460px;
      max-height: calc(100vh - 140px);
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 16px 48px rgba(0,0,0,0.2);
      display: none;
      flex-direction: column;
      overflow: hidden;
      z-index: 999999;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    #ssb-window.ssb-open { display: flex; }

    #ssb-header {
      background: linear-gradient(135deg, var(--ssb-red), var(--ssb-red-dark));
      color: #fff;
      padding: 14px 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    #ssb-header .ssb-title { font-size: 14px; font-weight: 600; margin: 0; }
    #ssb-header .ssb-sub { font-size: 11px; opacity: 0.9; margin: 1px 0 0; }
    #ssb-close {
      margin-left: auto;
      cursor: pointer;
      background: none;
      border: none;
      color: #fff;
      font-size: 18px;
      line-height: 1;
    }

    #ssb-messages {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      background: #fff;
    }
    .ssb-msg {
      max-width: 82%;
      padding: 9px 12px;
      border-radius: 12px;
      font-size: 13px;
      line-height: 1.4;
    }
    .ssb-bot {
      background: var(--ssb-cream);
      border: 1px solid var(--ssb-line);
      color: var(--ssb-ink);
      align-self: flex-start;
      border-bottom-left-radius: 3px;
    }
    .ssb-user {
      background: var(--ssb-red);
      color: #fff;
      align-self: flex-end;
      border-bottom-right-radius: 3px;
    }

    #ssb-quick {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      padding: 0 12px 8px;
      background: #fff;
    }
    #ssb-quick button {
      background: #fff;
      border: 1px solid var(--ssb-red);
      color: var(--ssb-red);
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 11px;
      cursor: pointer;
    }
    #ssb-quick button:hover { background: var(--ssb-red); color: #fff; }

    #ssb-input-row {
      display: flex;
      gap: 6px;
      padding: 8px;
      border-top: 1px solid var(--ssb-line);
    }
    #ssb-input {
      flex: 1;
      border: 1px solid var(--ssb-line);
      border-radius: 999px;
      padding: 8px 14px;
      font-size: 13px;
      outline: none;
    }
    #ssb-input:focus { border-color: var(--ssb-red); }
    #ssb-send {
      background: var(--ssb-red);
      color: #fff;
      border: none;
      border-radius: 999px;
      padding: 0 16px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
    }
    #ssb-send:hover { background: var(--ssb-red-dark); }

    @media (max-width: 420px) {
      #ssb-window { right: 16px; bottom: 88px; width: calc(100vw - 32px); }
      #ssb-bubble { right: 16px; }
    }
  `;
  document.head.appendChild(style);

  // ---------- Bubble button ----------
  const bubble = document.createElement("div");
  bubble.id = "ssb-bubble";
  bubble.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C12 2 5 10.5 5 15C5 18.87 8.13 22 12 22C15.87 22 19 18.87 19 15C19 10.5 12 2 12 2Z"
        fill="white"/>
    </svg>
  `;
  document.body.appendChild(bubble);

  // ---------- Chat window ----------
  const win = document.createElement("div");
  win.id = "ssb-window";
  win.innerHTML = `
    <div id="ssb-header">
      <div>
        <p class="ssb-title">Shri Satya Sai Blood Centre</p>
        <p class="ssb-sub">Cidco &middot; Open 24 hours</p>
      </div>
      <button id="ssb-close">&times;</button>
    </div>
    <div id="ssb-messages">
      <div class="ssb-msg ssb-bot">Welcome to Shri Satya Sai Blood Centre, Cidco. How can I help you today?</div>
    </div>
    <div id="ssb-quick">
      <button data-q="Where are you located?">Address</button>
      <button data-q="I want to donate blood">Donate blood</button>
      <button data-q="What are your timings?">Timings</button>
      <button data-q="How can I contact you?">Contact</button>
    </div>
    <div id="ssb-input-row">
      <input id="ssb-input" type="text" placeholder="Type your message..." />
      <button id="ssb-send">Send</button>
    </div>
  `;
  document.body.appendChild(win);

  // ---------- Behavior ----------
  const messagesEl = win.querySelector("#ssb-messages");
  const inputEl = win.querySelector("#ssb-input");

  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "ssb-msg ssb-" + sender;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function sendMessage(text) {
    const message = (text !== undefined ? text : inputEl.value).trim();
    if (!message) return;
    addMessage(message, "user");
    inputEl.value = "";

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });
      const data = await res.json();
      addMessage(data.reply, "bot");
    } catch (err) {
      addMessage("Sorry, I couldn't reach the server. Please try again shortly.", "bot");
    }
  }

  bubble.addEventListener("click", () => {
    win.classList.toggle("ssb-open");
    if (win.classList.contains("ssb-open")) inputEl.focus();
  });
  win.querySelector("#ssb-close").addEventListener("click", () => {
    win.classList.remove("ssb-open");
  });
  win.querySelector("#ssb-send").addEventListener("click", () => sendMessage());
  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
  win.querySelectorAll("#ssb-quick button").forEach((btn) => {
    btn.addEventListener("click", () => sendMessage(btn.getAttribute("data-q")));
  });
})();
