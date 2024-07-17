from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Configure sua chave API da OpenAI
openai.api_key = "sk-proj-MCKhGhSeCOMPlpRmAekST3BlbkFJywBIfx9k2CVJwGpjeIGu"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        messages = data['messages']
        model = data['model']
        
        # Log de depuração
        app.logger.info(f"Received messages: {messages} with model: {model}")
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        
        # Log de depuração
        app.logger.info(f"API response: {response}")
        
        return jsonify({"response": response['choices'][0]['message']['content']})
    except Exception as e:
        app.logger.error(f"Erro: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)