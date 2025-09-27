import os
from flask import Flask, request, jsonify, render_template
import openai
from datetime import datetime

app = Flask(__name__)

# Carrega a chave da OpenAI de uma variável de ambiente
openai.api_key = "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"

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

        # Adiciona contexto para tornar a conversa mais natural
        system_message = {
            "role": "system", 
            "content": """Você é uma assistente inteligente e prestativa chamada Sophia. Responda de forma natural e conversacional, como uma pessoa real. 
            
            IMPORTANTE:
            - Seja empática e engajada na conversa
            - Quando perguntarem sobre horas, datas ou tempo, forneça a informação atual de forma útil
            - Mostre personalidade e interesse genuíno no usuário
            - Use emojis ocasionalmente para tornar a conversa mais vibrante
            - Faça perguntas de volta para manter a conversa fluindo
            - Adapte seu idioma ao do usuário (português ou inglês)
            - Seja útil, mas também amigável e com um toque pessoal"""
        }

        # Insere a mensagem do sistema no início
        messages_with_context = [system_message] + messages

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages_with_context,
            temperature=0.8,  # Mais criatividade nas respostas
            max_tokens=500   # Respostas mais longas e completas
        )

        reply = response['choices'][0]['message']['content']
        app.logger.info(f"API response: {reply}")

        return jsonify({"response": reply})
    
    except Exception as e:
        app.logger.error(f"Erro: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)