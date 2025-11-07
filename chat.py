import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cliente OpenAI com a nova sintaxe
client = OpenAI(api_key=os.getenv("openai.api_key"))

@app.route('/')
def chat_page():
    return render_template('chat.html')

@app.route('/translator')
def translator_page():
    return render_template('translator.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        user_message = data['message']
        detected_language = data.get('language', 'pt-BR')

        # Define a mensagem do sistema baseada no idioma detectado
        if detected_language.startswith('pt'):
            system_content = """Você é uma assistente chamada Sophia. Seja simpática, envolvente e natural. 
            Responda SEMPRE em português brasileiro. Use emojis, faça perguntas e mostre empatia. 
            Responda como uma pessoa real em conversas casuais."""
        elif detected_language.startswith('en'):
            system_content = """You are an assistant named Sophia. Be friendly, engaging and natural. 
            ALWAYS respond in English. Use emojis, ask questions and show empathy. 
            Respond like a real person in casual conversations."""
        elif detected_language.startswith('es'):
            system_content = """Eres una asistente llamada Sophia. Sé amable, atractiva y natural. 
            SIEMPRE responde en español. Usa emojis, haz preguntas y muestra empatía. 
            Responde como uma persona real en conversaciones informales."""
        else:
            system_content = """You are an assistant named Sophia. Be friendly, engaging and natural. 
            Respond in the same language as the user. Use emojis, ask questions and show empathy."""

        # Nova sintaxe da OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
            temperature=0.8,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'target_language' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        text = data['text']
        target_language = data['target_language']
        
        # Mapa de idiomas para instruções
        language_map = {
            'pt': 'português brasileiro',
            'pt-BR': 'português brasileiro',
            'en': 'English',
            'en-US': 'English',
            'es': 'español',
            'es-ES': 'español',
            'fr': 'français',
            'fr-FR': 'français',
            'de': 'Deutsch',
            'de-DE': 'Deutsch',
            'it': 'italiano',
            'it-IT': 'italiano',
            'ja': '日本語',
            'ja-JP': '日本語',
            'ko': '한국어',
            'ko-KR': '한국어',
            'zh': '中文',
            'zh-CN': '中文'
        }
        
        target_lang_name = language_map.get(target_language, 'English')

        # Nova sintaxe da OpenAI
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following text to {target_lang_name}. Only provide the translation, no explanations."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        translation = response.choices[0].message.content
        return jsonify({"translation": translation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)