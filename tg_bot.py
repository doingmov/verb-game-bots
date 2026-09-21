import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from dialogflow_client import detect_intent


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте')


def reply_with_dialogflow(update: Update, context: CallbackContext) -> None:
    answer = detect_intent(
        project_id=context.bot_data['project_id'],
        session_id=str(update.effective_user.id),
        text=update.message.text,
    )
    update.message.reply_text(answer)


def main() -> None:
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO,
    )

    updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = os.environ['DIALOGFLOW_PROJECT_ID']

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply_with_dialogflow)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()