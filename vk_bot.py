import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import Event, VkEventType, VkLongPoll

from dialogflow_client import detect_intent
from logs_handler import TelegramLogsHandler

logger = logging.getLogger('vk_bot')


def reply_with_dialogflow(event: Event, vk_client, project_id: str) -> None:
    answer, is_fallback = detect_intent(
        project_id=project_id,
        session_id=f'vk-{event.user_id}',
        text=event.text,
    )
    if is_fallback:
        return
    
    vk_client.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.getrandbits(31),
    )


def main() -> None:
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO,
        )
    logger.addHandler(
        TelegramLogsHandler(
            os.environ['LOGS_BOT_TOKEN'],
            os.environ['LOGS_CHAT_ID'],
            )
        )

    try:

        project_id = os.environ['DIALOGFLOW_PROJECT_ID']

        vk_session = vk_api.VkApi(token=os.environ['VK_GROUP_TOKEN'])
        vk_client = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        logger.info('Бот VK запущен')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply_with_dialogflow(event, vk_client, project_id)
    except Exception:
        logger.exception('Бот VK упал')
        raise


if __name__ == '__main__':
    main()