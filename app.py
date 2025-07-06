from flask import Flask, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='', static_url_path='')

API_KEY = os.getenv("OPENROUTER_API_KEY")


@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')  # ✅ this serves your landing page

@app.route('/chat.html')
def serve_chat():
    return send_from_directory('', 'chat.html')  # ✅ this serves the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "qwen/qwen2.5-vl-72b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are Healia 👩‍⚕️, a compassionate AI therapist developed by Team MindHeal, that have Ammar. You help people feel calm, listened to, and mentally supported. Be warm, kind, and human-like, and funny."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        res.raise_for_status()
        bot_reply = res.json()['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
