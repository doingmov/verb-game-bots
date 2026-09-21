import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll


def echo(event: vk_api.longpoll.Event, vk_client) -> None:
    vk_client.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.getrandbits(31),
    )


def main() -> None:
    load_dotenv()
    vk_session = vk_api.VkApi(token=os.environ['VK_GROUP_TOKEN'])
    vk_client = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_client)


if __name__ == '__main__':
    main()