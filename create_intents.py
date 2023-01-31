import json
import os
from dotenv import load_dotenv

from dialogflow import create_intent

from google.oauth2 import service_account


def main():
    load_dotenv()

    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    PROJECT_ID = os.environ['PROJECT_ID']

    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

    with open('questions.json', 'r', encoding='utf-8') as file:
        questions_json = file.read()
    
    questions = json.loads(questions_json)

    for question, question_values in questions.items():
        display_name = question 
        training_phrases_parts = question_values['questions']
        message_texts = [question_values['answer']]

        create_intent(PROJECT_ID, display_name, training_phrases_parts, message_texts, credentials)


if __name__ == '__main__':
    main()