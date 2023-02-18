import logging
import traceback
import html
import json
import os
from dotenv import load_dotenv
from functools import partial

from dialogflow import detect_intent_texts

from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

from google.oauth2 import service_account


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Отправить сообщение при вызове команды /start."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def answer(update: Update, context: CallbackContext, project_id, credentials) -> None:
    session_id = update.message.chat_id
    answer = detect_intent_texts(project_id, session_id, update.message.text, 'ru', credentials)
    update.message.reply_text(answer.query_result.fulfillment_text)


def error_handler(update, context, chat_id):
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

    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)



def main():
    load_dotenv()

    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
    PROJECT_ID = os.environ['PROJECT_ID']
    CHAT_ID = os.environ['CHAT_ID']

    CREDENTIALS = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    wrap_answer = partial(answer, project_id=PROJECT_ID, credentials=CREDENTIALS)
    wrap_error_handler = partial(error_handler, chat_id=CHAT_ID)

    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, wrap_answer))
    dispatcher.add_error_handler(wrap_error_handler)

    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()
