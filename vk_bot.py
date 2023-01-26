import os
import random
from dotenv import load_dotenv

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google.cloud import dialogflow
from google.oauth2 import service_account

load_dotenv()
VK_TOKEN = os.environ['VK_TOKEN']
PROJECT_ID = os.environ['PROJECT_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
intents_client = dialogflow.IntentsClient(credentials=credentials)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            'session': session,
            'query_input': query_input
        }
    )

    return response


def answer(event, vk_api):
    session_id = event.user_id
    answer = detect_intent_texts(PROJECT_ID, session_id, event.text, 'ru')
    vk_api.messages.send(
        user_id = session_id,
        message = answer.query_result.fulfillment_text,
        random_id = random.randint(1,1000)
    )


def main():
    vk_session = vk.VkApi(token=VK_TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)


if __name__  == '__main__':
    main()
