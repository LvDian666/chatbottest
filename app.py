import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = os.getenv('OPENAI_API_URL')
MICROSOFT_APP_ID = os.getenv('MICROSOFT_APP_ID')
MICROSOFT_APP_PASSWORD = os.getenv('MICROSOFT_APP_PASSWORD')

# Bot Framework authentication
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

settings = BotFrameworkAdapterSettings(MICROSOFT_APP_ID, MICROSOFT_APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

@app.route('/api/messages', methods=['POST'])
def messages():
    if 'application/json' in request.headers['Content-Type']:
        json_message = request.json
    else:
        return jsonify({'error': 'Invalid Content-Type'})

    activity = Activity().deserialize(json_message)

    async def aux_func(turn_context: TurnContext):
        user_message = turn_context.activity.text
        openai_response = requests.post(
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
        bot_response = openai_response.json()['choices'][0]['text'].strip()
        await turn_context.send_activity(bot_response)

    task = adapter.process_activity(activity, "", aux_func)
    return jsonify({'response': 'OK'})

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
