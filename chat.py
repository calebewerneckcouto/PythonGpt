import os
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Chave da API da OpenAI
openai.api_key = os.getenv("openai.api_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translator')
def translator():
    return render_template('translator.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'messages' not in data or 'model' not in data:
            return jsonify({"error": "Dados inválidos"}), 400

        messages = data['messages']
        model = data['model']
        detected_language = data.get('language', 'pt-BR')

        # Define a mensagem do sistema baseada no idioma detectado
        if detected_language.startswith('pt'):
            system_content = """Você é uma assistente chamada Sophia. Seja simpática, envolvente e natural. 
            Responda SEMPRE em português brasileiro, independente do idioma da mensagem anterior. 
            Use emojis, faça perguntas e mostre empatia. Responda como uma pessoa real."""
        elif detected_language.startswith('en'):
            system_content = """You are an assistant named Sophia. Be friendly, engaging and natural. 
            ALWAYS respond in English, regardless of the language of the previous message. 
            Use emojis, ask questions and show empathy. Respond like a real person."""
        elif detected_language.startswith('es'):
            system_content = """Eres una asistente llamada Sophia. Sé amable, atractiva y natural. 
            SIEMPRE responde en español, independientemente del idioma del mensaje anterior. 
            Usa emojis, haz preguntas y muestra empatía. Responde como una persona real."""
        elif detected_language.startswith('fr'):
            system_content = """Tu es une assistante nommée Sophia. Sois sympathique, engageante et naturelle. 
            Réponds TOUJOURS en français, quelle que soit la langue du message précédent. 
            Utilise des emojis, pose des questions et montre de l'empathie. Réponds comme une vraie personne."""
        else:
            system_content = """You are an assistant named Sophia. Be friendly, engaging and natural. 
            Respond in the same language as the user. Use emojis, ask questions and show empathy."""

        system_message = {
            "role": "system",
            "content": system_content
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
            'pt-BR': 'português brasileiro',
            'en-US': 'English',
            'es-ES': 'español',
            'fr-FR': 'français',
            'de-DE': 'Deutsch',
            'it-IT': 'italiano',
            'ja-JP': '日本語',
            'ko-KR': '한국어',
            'zh-CN': '中文'
        }
        
        target_lang_name = language_map.get(target_language, 'English')

        response = openai.ChatCompletion.create(
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

        translation = response['choices'][0]['message']['content']
        return jsonify({"translation": translation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)