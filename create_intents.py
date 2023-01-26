import json
import os
from dotenv import load_dotenv

from google.cloud import dialogflow
from google.oauth2 import service_account

load_dotenv()

PROJECT_ID = os.environ['PROJECT_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
intents_client = dialogflow.IntentsClient(credentials=credentials)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions_json = file.read()
    
    questions = json.loads(questions_json)

    # Получаем ключи
    for question in questions:
        print(question)
        display_name = question 
        print(display_name)
        training_phrases_parts = questions[display_name]['questions']
        print(training_phrases_parts)
        message_texts = [questions[display_name]['answer']]
        print(message_texts)

        create_intent(PROJECT_ID, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()