import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import Event, VkEventType, VkLongPoll

from dialogflow_client import detect_intent


def reply_with_dialogflow(event: Event, vk_client, project_id: str) -> None:
    answer = detect_intent(
        project_id=project_id,
        session_id=f'vk-{event.user_id}',
        text=event.text,
    )
    vk_client.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.getrandbits(31),
    )


def main() -> None:
    load_dotenv()
    project_id = os.environ['DIALOGFLOW_PROJECT_ID']

    vk_session = vk_api.VkApi(token=os.environ['VK_GROUP_TOKEN'])
    vk_client = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_with_dialogflow(event, vk_client, project_id)


if __name__ == '__main__':
    main()