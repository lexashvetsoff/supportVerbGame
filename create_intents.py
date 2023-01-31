import json

from settings import PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS
from dialogflow import create_intent

from google.cloud import dialogflow
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
intents_client = dialogflow.IntentsClient(credentials=credentials)


def main():
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions_json = file.read()
    
    questions = json.loads(questions_json)

    # Получаем ключи
    for question in questions:
        display_name = question 
        training_phrases_parts = questions[display_name]['questions']
        message_texts = [questions[display_name]['answer']]

        create_intent(PROJECT_ID, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()