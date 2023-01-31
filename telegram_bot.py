import logging
import traceback
import html
import json

from settings import TELEGRAM_BOT_TOKEN, PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS, CHAT_ID
from dialogflow import detect_intent_texts

from telegram import Update, ForceReply, ParseMode
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
    session_id = update.message.chat_id
    answer = detect_intent_texts(PROJECT_ID, session_id, update.message.text, 'ru')
    update.message.reply_text(answer.query_result.fulfillment_text)


def error_handler(update, context):
    """
        Регистрирует ошибку и уведомляет   
        разработчика сообщением telegram.
    """
    logger.error(msg="Исключение при обработке сообщения:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'Возникло исключение при обработке сообщения.\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Отправляем сообщение разработчику
    context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)



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
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()
