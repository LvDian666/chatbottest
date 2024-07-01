from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('0a63583019b44e6d8b2cd5369cd6deee')
OPENAI_API_URL = os.getenv('https://ldtest.openai.azure.com/openai/deployments/gpt-4o')

@app.route('/api/messages', methods=['POST'])
def get_openai_response():
    user_message = request.json.get('message')
    response = requests.post(
        OPENAI_API_URL,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        },
        json={
            'prompt': user_message,
            'max_tokens': 150
        }
    )

    bot_message = response.json()['choices'][0]['text'].strip()
    return jsonify({'message': bot_message})

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))

