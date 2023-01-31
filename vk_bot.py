import random
import logging

from settings import VK_TOKEN, PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS
from dialogflow import detect_intent_texts

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google.cloud import dialogflow
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
intents_client = dialogflow.IntentsClient(credentials=credentials)

# Включаем логирование
logger = logging.getLogger(__name__)


def answer(event, vk_api):
    session_id = event.user_id
    answer = detect_intent_texts(PROJECT_ID, session_id, event.text, 'ru')
    if not answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id = session_id,
            message = answer.query_result.fulfillment_text,
            random_id = random.randint(1,1000)
        )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    vk_session = vk.VkApi(token=VK_TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)


if __name__  == '__main__':
    main()
