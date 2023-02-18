import random
import logging
import os
from dotenv import load_dotenv

from dialogflow import detect_intent_texts

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google.oauth2 import service_account


logger = logging.getLogger(__name__)


def answer(event, vk_api, project_id, credentials):
    session_id = event.user_id
    answer = detect_intent_texts(project_id, session_id, event.text, 'ru', credentials)
    if not answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id = session_id,
            message = answer.query_result.fulfillment_text,
            random_id = random.randint(1,1000)
        )


def main():
    load_dotenv()

    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    VK_TOKEN = os.environ['VK_TOKEN']
    PROJECT_ID = os.environ['PROJECT_ID']

    CREDENTIALS = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    vk_session = vk.VkApi(token=VK_TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api, PROJECT_ID, CREDENTIALS)


if __name__  == '__main__':
    main()
