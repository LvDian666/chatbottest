import os
from flask import Flask, request, jsonify
import requests
import asyncio
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

app = Flask(__name__)

# 从环境变量中获取设置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = os.getenv('OPENAI_API_URL')
MICROSOFT_APP_ID = os.getenv('MICROSOFT_APP_ID')
MICROSOFT_APP_PASSWORD = os.getenv('MICROSOFT_APP_PASSWORD')

settings = BotFrameworkAdapterSettings(MICROSOFT_APP_ID, MICROSOFT_APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

@app.route('/api/messages', methods=['POST'])
def messages():
    if 'application/json' not in request.headers['Content-Type']:
        return jsonify({'error': 'Invalid Content-Type'})

    json_message = request.json
    activity = Activity().deserialize(json_message)

    async def aux_func(turn_context: TurnContext):
        try:
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
        except Exception as e:
            await turn_context.send_activity(f"Error: {str(e)}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(adapter.process_activity(activity, "", aux_func))
    loop.run_until_complete(task)

    return jsonify({'response': 'OK'})

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
