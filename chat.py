import os
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Chave da API da OpenAI
openai.api_key = "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"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'messages' not in data or 'model' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        messages = data['messages']
        model = data['model']

        system_message = {
            "role": "system",
            "content": """Você é uma assistente chamada Sophia. Seja simpática, envolvente e natural. Responda como uma pessoa real, com emojis, perguntas e empatia. Adapte o idioma conforme o do usuário."""
        }

        conversation = [system_message] + messages

        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=0.8,
            max_tokens=500
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
