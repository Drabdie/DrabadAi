from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
client = openai.OpenAI(api_key="sk-...", base_url="https://openrouter.ai/api/v1")

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Agent</title>
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chat { height: 70vh; background: #161b22; border: 1px solid #30363d; border-radius: 6px; overflow-y: auto; padding: 15px; margin-bottom: 10px; }
        .msg { margin: 8px 0; padding: 10px; border-radius: 4px; }
        .user { background: #238636; margin-left: 15%; color: white; }
        .bot { background: #1f6feb; color: white; margin-right: 15%; }
        input { width: 80%; padding: 10px; background: #0d1117; border: 1px solid #30363d; color: white; border-radius: 4px; }
        button { width: 18%; padding: 10px; background: #238636; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2ea043; }
    </style>
</head>
<body>
    <h2 style="text-align: center;">🤖 AI Agent</h2>
    <div id="chat"></div>
    <input type="text" id="msg" placeholder="Ask anything..." onkeypress="if(event.key==='Enter') send()">
    <button onclick="send()">Send</button>

<script>
async function send() {
    const msg = document.getElementById('msg').value;
    if (!msg) return;
    
    const chat = document.getElementById('chat');
    chat.innerHTML += `<div class="msg user">${msg}</div>`;
    document.getElementById('msg').value = '';
    chat.scrollTop = chat.scrollHeight;
    
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });
        const data = await res.json();
        chat.innerHTML += `<div class="msg bot">${data.reply}</div>`;
        chat.scrollTop = chat.scrollHeight;
    } catch (e) {
        chat.innerHTML += `<div class="msg bot" style="background: #da3633;">Error: ${e}</div>`;
    }
}
</script>
</body>
</html>'''

@app.route('/api/chat', methods=['POST'])
def chat():
    msg = request.json.get('message', '')
    
    try:
        r = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[{"role": "user", "content": msg}],
            temperature=1.0,
            max_tokens=2000
        )
        reply = r.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
