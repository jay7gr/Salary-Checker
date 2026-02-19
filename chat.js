/**
 * salary:converter — AI Chat Assistant
 * Self-contained: injects CSS + DOM. Just add <script src="/chat.js"></script> before </body>.
 */
(function() {
    'use strict';

    // --- CSS (inject into <head>) ---
    var style = document.createElement('style');
    style.textContent = [
        /* Pill bubble */
        '.chat-bubble{position:fixed;bottom:32px;right:32px;height:44px;border-radius:22px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);border:none;cursor:pointer;z-index:10002;display:flex;align-items:center;gap:8px;padding:0 18px 0 14px;box-shadow:0 4px 20px rgba(37,99,235,0.3);transition:all 0.3s cubic-bezier(0.4,0,0.2,1);animation:chatBubblePulse 2.5s ease-in-out 1}',
        '.chat-bubble:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(37,99,235,0.4)}',
        /* Brand mark inside pill */
        '.chat-bubble .bubble-brand{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display",sans-serif;font-size:14px;font-weight:800;color:#fff;letter-spacing:-0.3px;line-height:1;pointer-events:none}',
        '.chat-bubble .bubble-brand .brand-colon{color:#93c5fd}',
        '.chat-bubble .bubble-text{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display",sans-serif;font-size:14px;font-weight:600;color:#fff;pointer-events:none;white-space:nowrap}',
        /* Open state: collapse to round close button */
        '.chat-bubble.open{width:44px;height:44px;padding:0;justify-content:center;border-radius:50%;background:linear-gradient(135deg,#dc2626,#ef4444)}',
        '.chat-bubble.open .bubble-brand,.chat-bubble.open .bubble-text{display:none}',
        '.chat-bubble.open .icon-close{display:flex}',
        '.chat-bubble .icon-close{display:none;align-items:center;justify-content:center}',
        '.chat-bubble .icon-close svg{width:20px;height:20px;fill:#fff}',
        '@keyframes chatBubblePulse{0%{box-shadow:0 4px 20px rgba(37,99,235,0.3),0 0 0 0 rgba(59,130,246,0.25)}50%{box-shadow:0 6px 28px rgba(37,99,235,0.45),0 0 0 8px rgba(59,130,246,0)}100%{box-shadow:0 4px 20px rgba(37,99,235,0.3),0 0 0 0 rgba(59,130,246,0)}}',
        /* Chat panel */
        '.chat-panel{position:fixed;bottom:88px;right:32px;width:380px;height:500px;background:var(--card-bg,#fff);border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.15);z-index:10002;display:flex;flex-direction:column;overflow:hidden;border:1px solid var(--border,#e5e5ea);opacity:0;transform:translateY(16px) scale(0.96);pointer-events:none;transition:opacity 0.25s ease,transform 0.25s ease}',
        '.chat-panel.open{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}',
        '[data-theme="dark"] .chat-panel{box-shadow:0 8px 40px rgba(0,0,0,0.5)}',
        '.chat-header{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border,#e5e5ea);flex-shrink:0}',
        '.chat-header-title{font-size:0.85rem;font-weight:600;color:var(--text-primary,#1d1d1f);line-height:1.3}',
        '.chat-header-subtitle{font-size:0.7rem;color:var(--text-secondary,#86868b);margin-top:2px}',
        '.chat-new-btn{background:none;border:none;color:var(--text-secondary,#86868b);cursor:pointer;font-size:0.75rem;padding:4px 8px;border-radius:6px;transition:background 0.15s,color 0.15s;font-family:inherit}',
        '.chat-new-btn:hover{background:var(--tag-bg,#f0f0f2);color:var(--text-primary,#1d1d1f)}',
        '.chat-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;scrollbar-width:thin;scrollbar-color:var(--border,#e5e5ea) transparent}',
        '.chat-messages::-webkit-scrollbar{width:4px}',
        '.chat-messages::-webkit-scrollbar-thumb{background:var(--border,#e5e5ea);border-radius:2px}',
        '.chat-msg{max-width:85%;padding:10px 14px;border-radius:14px;font-size:0.84rem;line-height:1.55;word-wrap:break-word;animation:chatMsgIn 0.2s ease-out}',
        '@keyframes chatMsgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}',
        '.chat-msg-user{align-self:flex-end;background:var(--accent,#2563eb);color:#fff;border-bottom-right-radius:4px}',
        '.chat-msg-ai{align-self:flex-start;background:var(--stat-card-bg,#f5f5f7);color:var(--text-primary,#1d1d1f);border-bottom-left-radius:4px}',
        '.chat-msg-ai strong{font-weight:600}',
        '.chat-msg-ai a{color:var(--accent,#2563eb);text-decoration:underline;text-underline-offset:2px}',
        '.chat-msg-ai ul,.chat-msg-ai ol{padding-left:18px;margin:6px 0}',
        '.chat-msg-ai li{margin-bottom:3px}',
        '.chat-msg-ai code{background:var(--tag-bg,#f0f0f2);padding:1px 5px;border-radius:4px;font-size:0.8rem}',
        '.chat-msg-ai p{margin:0 0 8px 0}',
        '.chat-msg-ai p:last-child{margin-bottom:0}',
        '.chat-typing{display:flex;gap:4px;padding:12px 16px;align-self:flex-start}',
        '.chat-typing-dot{width:8px;height:8px;background:var(--text-secondary,#86868b);border-radius:50%;animation:chatTypingBounce 1.2s ease-in-out infinite}',
        '.chat-typing-dot:nth-child(2){animation-delay:0.15s}',
        '.chat-typing-dot:nth-child(3){animation-delay:0.3s}',
        '@keyframes chatTypingBounce{0%,60%,100%{transform:translateY(0);opacity:0.4}30%{transform:translateY(-6px);opacity:1}}',
        '.chat-input-area{display:flex;gap:8px;padding:12px 16px;border-top:1px solid var(--border,#e5e5ea);flex-shrink:0}',
        '.chat-input{flex:1;border:1px solid var(--input-border,var(--border,#e5e5ea));border-radius:10px;padding:10px 14px;font-size:0.84rem;background:var(--input-bg,var(--card-bg,#fff));color:var(--text-primary,#1d1d1f);outline:none;font-family:inherit;resize:none;max-height:80px;min-height:40px;line-height:1.4;transition:border-color 0.15s,box-shadow 0.15s}',
        '.chat-input::placeholder{color:var(--input-placeholder,var(--text-secondary,#86868b))}',
        '.chat-input:focus{border-color:var(--accent,#2563eb);box-shadow:var(--focus-shadow,0 0 0 3px rgba(37,99,235,0.15))}',
        '.chat-send-btn{width:40px;height:40px;border-radius:10px;background:var(--accent,#2563eb);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background 0.15s,opacity 0.15s;align-self:flex-end}',
        '.chat-send-btn:hover{background:var(--accent-hover,#1d4ed8)}',
        '.chat-send-btn:disabled{opacity:0.5;cursor:default}',
        '.chat-send-btn svg{width:18px;height:18px;fill:#fff}',
        '.chat-error{padding:8px 12px;background:var(--error-bg,#fef2f2);color:var(--error-color,#dc2626);border:1px solid var(--error-border,#fecaca);border-radius:8px;font-size:0.78rem;align-self:center;text-align:center;max-width:90%}',
        '.chat-welcome{text-align:center;padding:20px 16px;color:var(--text-secondary,#86868b);font-size:0.82rem;line-height:1.5}',
        '.chat-welcome-title{font-size:1rem;font-weight:600;color:var(--text-primary,#1d1d1f);margin-bottom:8px}',
        '.chat-suggestions{display:flex;flex-direction:column;gap:6px;margin-top:12px}',
        '.chat-suggestion-btn{background:var(--tag-bg,#f0f0f2);border:1px solid var(--border,#e5e5ea);border-radius:10px;padding:8px 12px;font-size:0.78rem;color:var(--text-primary,#1d1d1f);cursor:pointer;text-align:left;transition:background 0.15s,border-color 0.15s;font-family:inherit}',
        '.chat-suggestion-btn:hover{background:var(--dropdown-hover,rgba(0,0,0,0.04));border-color:var(--accent,#2563eb)}',
        /* Mobile */
        '@media(max-width:768px){',
        '.chat-bubble{bottom:16px;right:16px;height:40px;border-radius:20px;padding:0 14px 0 12px;gap:6px}',
        '.chat-bubble .bubble-brand{font-size:12px}',
        '.chat-bubble .bubble-text{font-size:12px}',
        '.chat-bubble.open{width:40px;height:40px;bottom:12px;right:12px;z-index:10003}',
        '.chat-bubble .icon-close svg{width:18px;height:18px}',
        '.chat-panel{bottom:0;right:0;left:0;top:0;width:100%;height:100%;border-radius:0;border:none}',
        'body.chat-lock{overflow:hidden;position:fixed;width:100%;touch-action:none}',
        '}'
    ].join('\n');
    document.head.appendChild(style);

    // --- Config ---
    var _k = '=0UVBZ3aJFGWDBDUz80b2o3N0E0aD5kTsllRzIWekd0VMZUWl5EZBRUbalnetNXYnh2TVt2XrN3Z';
    var getKey = function() { return atob(_k.split('').reverse().join('')); };

    var SYSTEM_PROMPT = 'You are the AI assistant for Salary Converter (salary-converter.com), a free tool that compares salaries across 100+ cities and 2,000+ neighborhoods worldwide.\n\n## What the Tool Does\n- Users enter their current salary, city, and neighborhood\n- They select a target city and neighborhood\n- The tool calculates an equivalent salary adjusted for cost of living differences, currency exchange, and local taxes\n- It shows: equivalent salary, tax breakdown, estimated rent, affordability verdict with living cost breakdown, and salary ranges by role\n- Users can optionally enter a real salary offer for the target city to get a personalized affordability comparison\n\n## How the COLI Calculation Works\n- Each city has a Cost of Living Index (COLI) with New York City = 100 as the baseline\n- Neighborhoods have multipliers relative to their city (e.g., Manhattan Midtown = 1.25x of NYC base)\n- Formula: Equivalent Salary = Current Salary \u00d7 (Target COLI / Current COLI) \u00d7 Exchange Rate\n- The COLI captures housing, groceries, transport, utilities, and healthcare costs\n- Sources: Numbeo, OECD, and other public datasets\n\n## Tax Methodology\n- Progressive income tax brackets for 45+ countries\n- Social security / mandatory deductions (FICA, NI, CPF, etc.) by country\n- City-level overrides: US state taxes, Canadian provincial taxes, Swiss cantonal taxes, UK council tax\n- Neighborhood-level tax overrides (e.g., London borough-specific council tax)\n\n## Affordability Verdict\n- Shows a detailed breakdown: gross salary \u2192 taxes \u2192 take-home \u2192 minus rent, groceries, utilities, transport, healthcare (optionally childcare) \u2192 disposable income\n- All living costs adjusted by neighborhood multiplier\n- Compares disposable income between current and target cities\n- If user enters a salary offer, verdict uses that real offer instead of the COLI-equivalent\n\n## Supported Regions\nNorth America: NYC, SF, LA, Chicago, Miami, Austin, Seattle, Denver, Boston, DC, Houston, Toronto, Vancouver, Montreal, Mexico City, Cancun, Panama City\nEurope: London, Paris, Amsterdam, Berlin, Munich, Dublin, Brussels, Luxembourg, Zurich, Geneva, Edinburgh, Nice, Madrid, Barcelona, Valencia, Malaga, Lisbon, Porto, Rome, Milan, Athens, Split, Stockholm, Copenhagen, Helsinki, Oslo, Vienna, Prague, Budapest, Warsaw, Krakow, Bucharest, Tallinn, Riga, Istanbul\nAsia: Tokyo, Osaka, Fukuoka, Seoul, Hong Kong, Taipei, Shanghai, Beijing, Shenzhen, Guangzhou, Singapore, Bangkok, Chiang Mai, Phuket, KL, HCMC, Hanoi, Manila, Jakarta, Bali, Phnom Penh, Mumbai, Bangalore, Delhi, Chennai\nOceania: Sydney, Melbourne, Perth, Auckland\nMiddle East: Dubai, Abu Dhabi, Doha, Riyadh, Tel Aviv\nAfrica: Cape Town, Nairobi, Lagos, Cairo, Marrakech, Casablanca\nSouth America: Sao Paulo, Buenos Aires, Bogota, Lima, Santiago, Medellin, Montevideo, San Jose (CR), Playa del Carmen\n\n## Your Personality\n- Helpful, knowledgeable, and concise\n- Give specific numbers and comparisons when possible\n- Use bullet points for clarity\n- Keep responses under 200 words unless the question requires more detail\n- Be honest about limitations (e.g., "taxes are estimates, consult a professional for your specific situation")\n\n## Boundaries\n- You answer questions about: salaries, cost of living, taxes, relocation, the tool itself, currency exchange, affordability, neighborhoods, remote work locations\n- For off-topic questions, politely redirect: "I specialize in salary comparisons and relocation advice. Is there anything salary or relocation related I can help with?"\n- Never provide specific legal, immigration, or visa advice \u2014 suggest consulting a professional\n- Never provide specific investment or financial planning advice';

    // --- State ---
    var chatOpen = false;
    var chatInitialized = false;
    var isStreaming = false;
    var conversationHistory = [];
    var abortController = null;
    var bubble, panel;
    var MAX_HISTORY = 20;

    // --- Helpers ---
    function renderMarkdown(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
            .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
            .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
            .replace(/((?:<li>.*<\/li>\s*)+)/g, function(match) {
                return '<ul>' + match + '</ul>';
            })
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');
    }

    function scrollToBottom() {
        var el = document.getElementById('chatMessages');
        if (el) el.scrollTop = el.scrollHeight;
    }

    function appendMessage(type, text) {
        var messagesEl = document.getElementById('chatMessages');
        var msg = document.createElement('div');
        msg.className = 'chat-msg chat-msg-' + type;
        if (type === 'ai') {
            msg.innerHTML = '<div class="chat-msg-content">' + (text ? renderMarkdown(text) : '') + '</div>';
        } else {
            msg.textContent = text;
        }
        messagesEl.appendChild(msg);
        scrollToBottom();
        return msg;
    }

    function appendError(text) {
        var messagesEl = document.getElementById('chatMessages');
        var err = document.createElement('div');
        err.className = 'chat-error';
        err.textContent = text;
        messagesEl.appendChild(err);
        scrollToBottom();
    }

    function showTyping() {
        var messagesEl = document.getElementById('chatMessages');
        var typing = document.createElement('div');
        typing.className = 'chat-typing';
        typing.innerHTML = '<div class="chat-typing-dot"></div><div class="chat-typing-dot"></div><div class="chat-typing-dot"></div>';
        messagesEl.appendChild(typing);
        scrollToBottom();
        return typing;
    }

    function showWelcome() {
        var messagesEl = document.getElementById('chatMessages');
        messagesEl.innerHTML = '<div class="chat-welcome">' +
            '<div class="chat-welcome-title">Hi! I\'m your salary & relocation assistant.</div>' +
            '<div>Ask me anything about cost of living, taxes, or relocating between cities.</div>' +
            '<div class="chat-suggestions">' +
                '<button class="chat-suggestion-btn" data-q="How does the cost of living index (COLI) work on this tool?">How does the COLI work?</button>' +
                '<button class="chat-suggestion-btn" data-q="What\'s the real difference in take-home pay between New York and London?">NYC vs London take-home pay?</button>' +
                '<button class="chat-suggestion-btn" data-q="Which cities have the lowest cost of living for remote workers earning in USD or GBP?">Best cities for remote workers?</button>' +
            '</div>' +
        '</div>';
        messagesEl.querySelectorAll('.chat-suggestion-btn').forEach(function(btn) {
            btn.addEventListener('click', function() { sendMessage(btn.dataset.q); });
        });
    }

    // --- API ---
    async function streamResponse(messages, typingEl) {
        abortController = new AbortController();
        var response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getKey()
            },
            body: JSON.stringify({
                model: 'llama-3.3-70b-versatile',
                messages: [{ role: 'system', content: SYSTEM_PROMPT }].concat(messages),
                temperature: 0.7,
                max_completion_tokens: 1024,
                stream: true
            }),
            signal: abortController.signal
        });

        if (!response.ok) {
            await response.text().catch(function() { return ''; });
            if (response.status === 429) {
                throw new Error('Rate limit reached. Please try again in a moment.');
            }
            throw new Error('API error: ' + response.status);
        }

        typingEl.remove();
        var msgEl = appendMessage('ai', '');
        var contentEl = msgEl.querySelector('.chat-msg-content');

        var fullText = '';
        var reader = response.body.getReader();
        var decoder = new TextDecoder();
        var buffer = '';

        while (true) {
            var result = await reader.read();
            if (result.done) break;

            buffer += decoder.decode(result.value, { stream: true });
            var lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (var i = 0; i < lines.length; i++) {
                var line = lines[i];
                if (!line.startsWith('data: ')) continue;
                var data = line.slice(6);
                if (data === '[DONE]') break;
                try {
                    var parsed = JSON.parse(data);
                    var delta = parsed.choices && parsed.choices[0] && parsed.choices[0].delta && parsed.choices[0].delta.content;
                    if (delta) {
                        fullText += delta;
                        contentEl.innerHTML = renderMarkdown(fullText);
                        scrollToBottom();
                    }
                } catch (e) { /* skip malformed chunks */ }
            }
        }

        conversationHistory.push({ role: 'assistant', content: fullText });
    }

    async function sendMessage(text) {
        if (!text || !text.trim() || isStreaming) return;
        text = text.trim();

        var welcome = document.querySelector('.chat-welcome');
        if (welcome) welcome.remove();

        appendMessage('user', text);
        conversationHistory.push({ role: 'user', content: text });

        while (conversationHistory.length > MAX_HISTORY) {
            conversationHistory.shift();
        }

        var input = document.getElementById('chatInput');
        input.value = '';
        input.style.height = 'auto';

        var typingEl = showTyping();
        isStreaming = true;
        document.getElementById('chatSend').disabled = true;

        try {
            await streamResponse(conversationHistory.filter(function(m) { return m.role !== 'assistant' || conversationHistory.indexOf(m) < conversationHistory.length; }), typingEl);
        } catch (err) {
            typingEl.remove();
            if (err.name !== 'AbortError') {
                appendError(err.message || 'Sorry, something went wrong. Please try again.');
            }
        } finally {
            isStreaming = false;
            document.getElementById('chatSend').disabled = false;
            document.getElementById('chatInput').focus();
        }
    }

    function clearChat() {
        conversationHistory = [];
        if (abortController) abortController.abort();
        isStreaming = false;
        document.getElementById('chatSend').disabled = false;
        showWelcome();
    }

    // --- DOM ---
    function createPanel() {
        var p = document.createElement('div');
        p.className = 'chat-panel';
        p.innerHTML =
            '<div class="chat-header">' +
                '<div>' +
                    '<div class="chat-header-title">Salary & Relocation Assistant</div>' +
                    '<div class="chat-header-subtitle">Powered by AI</div>' +
                '</div>' +
                '<button class="chat-new-btn" id="chatNewBtn">New Chat</button>' +
            '</div>' +
            '<div class="chat-messages" id="chatMessages"></div>' +
            '<div class="chat-input-area">' +
                '<textarea class="chat-input" id="chatInput" placeholder="Ask about salaries, cost of living..." rows="1"></textarea>' +
                '<button class="chat-send-btn" id="chatSend" aria-label="Send message">' +
                    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>' +
                '</button>' +
            '</div>';
        document.body.appendChild(p);

        document.getElementById('chatNewBtn').addEventListener('click', clearChat);
        document.getElementById('chatSend').addEventListener('click', function() {
            sendMessage(document.getElementById('chatInput').value);
        });

        var chatInput = document.getElementById('chatInput');
        chatInput.addEventListener('input', function() {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 80) + 'px';
        });
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage(chatInput.value);
            }
            e.stopPropagation();
        });
        chatInput.addEventListener('keypress', function(e) {
            e.stopPropagation();
        });

        showWelcome();
        chatInitialized = true;
        return p;
    }

    var scrollY = 0;

    function toggleChat() {
        chatOpen = !chatOpen;
        bubble.classList.toggle('open', chatOpen);
        if (!chatInitialized) {
            panel = createPanel();
        }
        panel.classList.toggle('open', chatOpen);
        // Lock body scroll on mobile when chat is open
        if (window.innerWidth <= 768) {
            if (chatOpen) {
                scrollY = window.pageYOffset;
                document.body.classList.add('chat-lock');
                document.body.style.top = -scrollY + 'px';
            } else {
                document.body.classList.remove('chat-lock');
                document.body.style.top = '';
                window.scrollTo(0, scrollY);
            }
        }
        if (chatOpen) {
            setTimeout(function() {
                var input = document.getElementById('chatInput');
                if (input) input.focus();
            }, 300);
        }
    }

    // --- Init bubble (pill shape) ---
    bubble = document.createElement('button');
    bubble.className = 'chat-bubble';
    bubble.setAttribute('aria-label', 'Open AI chat assistant');
    bubble.innerHTML =
        '<span class="bubble-brand">s<span class="brand-colon">:</span>c</span>' +
        '<span class="bubble-text">Chat</span>' +
        '<span class="icon-close"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg></span>';
    document.body.appendChild(bubble);
    bubble.addEventListener('click', toggleChat);
})();
