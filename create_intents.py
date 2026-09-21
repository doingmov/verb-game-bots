import argparse
import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_texts, answer):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = [
        dialogflow.Intent.TrainingPhrase(
            parts=[dialogflow.Intent.TrainingPhrase.Part(text=text)]
        )
        for text in training_phrases_texts
    ]
    message = dialogflow.Intent.Message(
        text=dialogflow.Intent.Message.Text(text=[answer])
    )
    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    return intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Создаёт интенты в Dialogflow из JSON-файла с фразами'
    )
    parser.add_argument('path', nargs='?', default='questions.json',
                        help='путь к JSON-файлу (по умолчанию questions.json)')
    args = parser.parse_args()

    project_id = os.environ['DIALOGFLOW_PROJECT_ID']

    with open(args.path, 'r', encoding='utf-8') as file:
        intents = json.load(file)

    for display_name, content in intents.items():
        intent = create_intent(
            project_id,
            display_name,
            content['questions'],
            content['answer'],
        )
        print(f'Создан интент: {intent.display_name}')


if __name__ == '__main__':
    main()