import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Carrega a chave da OpenAI de uma variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'messages' not in data or 'model' not in data:
            raise ValueError("Os campos 'messages' e 'model' são obrigatórios.")

        messages = data['messages']
        model = data['model']

        app.logger.info(f"Received messages: {messages} with model: {model}")

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )

        reply = response['choices'][0]['message']['content']
        app.logger.info(f"API response: {reply}")

        return jsonify({"response": reply})
    
    except Exception as e:
        app.logger.error(f"Erro: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
