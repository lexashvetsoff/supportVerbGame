import logging

from settings import TELEGRAM_BOT_TOKEN, PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS
from dialogflow import detect_intent_texts

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

from google.cloud import dialogflow
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
intents_client = dialogflow.IntentsClient(credentials=credentials)

# Включаем логирование
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Отправить сообщение при вызове команды /start."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def answer(update: Update, context: CallbackContext) -> None:
    try:
        session_id = update.message.chat_id
        answer = detect_intent_texts(PROJECT_ID, session_id, update.message.text, 'ru')
        update.message.reply_text(answer.query_result.fulfillment_text)
    except:
        logger.exception()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()
