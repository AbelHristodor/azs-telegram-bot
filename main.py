""" AZS Telegram Bot

This is a telegram bot that helps people find everything they need in one single place.
It is made using telegram's api wrapper "python-telegram-bot" (see github.com/python-telegram-bot)
At the moment it supports the commands found in the HELP_MESSAGE (see messages.py)

@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot
"""
import os
import datetime
import logging
import pytz
import dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler ,Filters, CallbackContext, CallbackQueryHandler
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError

from utils.helpers import get_current_settings
from utils.scraper import Scraper
from utils.jobs import send_daily_devotional
from utils.messages import (
    WELCOME_MESSAGE,
    START_MESSAGE,
    COMMAND_NOT_FOUND_MESSAGE,
    HELP_MESSAGE,
    DEVOTIONAL_TYPES,
    CURRENT_SETTINGS_MESSAGE,
    CHURCH_ADDRESS
)

from conversations.configuration_conv import configuration_conversation_handler


dotenv.load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

scraper = Scraper()

def start(update: Update, context: CallbackContext) -> None:
    """ Start function """
    context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE, parse_mode=ParseMode.HTML)
    help_message(update=update, context=context)


def devotional_menu(update: Update, context: CallbackContext) -> None:
    """ Shows the main menu of the bot """
    keyboard = [
        [
            InlineKeyboardButton(DEVOTIONAL_TYPES[0], callback_data="1"),
            InlineKeyboardButton(DEVOTIONAL_TYPES[1], callback_data="2")
        ],
        [InlineKeyboardButton(DEVOTIONAL_TYPES[2], callback_data="3")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Devotional:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """ Handles the choice made by the user in the start function """
    query = update.callback_query
    query.answer()
    if query.data == "1":
        query.edit_message_text(scraper.get_devotional(), parse_mode=ParseMode.HTML)
    if query.data == "2":
        query.edit_message_text(scraper.get_devotional(dev_type=DEVOTIONAL_TYPES[1]), parse_mode=ParseMode.HTML)
    if query.data == "3":
        query.edit_message_text(scraper.get_devotional(dev_type=DEVOTIONAL_TYPES[2]), parse_mode=ParseMode.HTML)


def devotional_majori(update: Update, context: CallbackContext) -> None:
    """ Sends adults' devotional to the chat """
    update.message.reply_text(scraper.get_devotional(), parse_mode=ParseMode.HTML)


def devotional_tineri(update: Update, context: CallbackContext) -> None:
    """ Sends younger people's devotional for  to the chat """
    update.message.reply_text(scraper.get_devotional(dev_type=DEVOTIONAL_TYPES[1]), parse_mode=ParseMode.HTML)


def devotional_exploratori(update: Update, context: CallbackContext) -> None:
    """ Sends children's devotional to the chat """
    update.message.reply_text(scraper.get_devotional(dev_type=DEVOTIONAL_TYPES[2]), parse_mode=ParseMode.HTML)


def show_settings(update: Update, context: CallbackContext) -> None:
    """ Gets current settings """
    settings = get_current_settings(chat_id=update.effective_chat.id)

    msg = CURRENT_SETTINGS_MESSAGE.replace("$activat", settings["dev_status"])
    msg = msg.replace("$dev_type", settings["dev_type"]).replace("$dev_time", settings["dev_time"])

    update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)


def welcome_new_user(update: Update, context: CallbackContext) -> None:
    """ Sends a welcome message to the users that enter a group """
    for new_user_obj in update.message.new_chat_members:
        try:
            new_user = "@" + new_user_obj['username']
        except KeyError as key_error:
            logger.warning(
                'Username of new chat member not found, using - first_name\n%s',
                key_error
            )
            new_user = new_user_obj['first_name']

        context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE.replace("$user", str(new_user)), parse_mode=ParseMode.HTML)


def help_message(update: Update, context: CallbackContext) -> None:
    """ Sends the help message to the chat """
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_MESSAGE, parse_mode=ParseMode.HTML)


def church_address(update: Update, context: CallbackContext) -> None:
    """ Sends the address of the church to the chat """
    context.bot.send_message(chat_id=update.effective_chat.id, text=CHURCH_ADDRESS, parse_mode=ParseMode.HTML)


# Must be added last
def unknown(update: Update, context: CallbackContext, text: str = COMMAND_NOT_FOUND_MESSAGE) -> None:
    """ Handles not recognized commands sent in the chat """
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


def error_callback(update: Update, context: CallbackContext) -> None:
    """ Error Handling """
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        logger.exception("Update %s caused 'Unauthorized' error: %s", update, context.error)
    except BadRequest:
        # handle malformed requests - read more below!
        logger.exception("Update %s caused 'BadRequest' error: %s", update, context.error)
    except TimedOut:
        # handle slow connection problems
        logger.exception("Update %s caused 'TimedOut' error: %s", update, context.error)
    except NetworkError:
        # handle other connection problems
        logger.exception("Update %s caused 'Network' error: %s", update, context.error)
    except ChatMigrated as chat_migrated:
        logger.exception("Update %s caused 'ChatMigrated' error: %s\nChat Migrated, new id is: %d", update, context.error, chat_migrated.new_chat_id)
    except TelegramError:
        # handle all other telegram related errors
        logger.exception("Update %s caused 'TelegramError' error: %s", update, context.error)


def error_handler(update: Update, context: CallbackContext, message: str) -> None:
    """ Handles generic errors """
    context.bot.sendMessage(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)


def main() -> None:
    """ Main function """
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    queuer = updater.job_queue
    dispatcher = updater.dispatcher

    dispatcher.add_handler(configuration_conversation_handler) # /setari
    dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    dispatcher.add_handler(CommandHandler('dev', devotional_menu, run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('ajutor', help_message, run_async=True))
    dispatcher.add_handler(CommandHandler('majori', devotional_majori, run_async=True))
    dispatcher.add_handler(CommandHandler('tineri', devotional_tineri, run_async=True))
    dispatcher.add_handler(CommandHandler('explo', devotional_exploratori, run_async=True))
    dispatcher.add_handler(CommandHandler('adresa', church_address, run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_new_user, run_async=True))
    dispatcher.add_handler(CommandHandler('setari', show_settings, run_async=True))

    # Command not recognized error handler
    dispatcher.add_handler(MessageHandler(Filters.command, unknown, run_async=True))

    # Error Handler
    dispatcher.add_error_handler(error_callback)

    queuer.run_daily(
        callback=send_daily_devotional,
        time=datetime.time(
            hour=int(os.getenv("DAILY_DEVOTIONAL_HOUR")),
            minute=int(os.getenv("DAILY_DEVOTIONAL_MINUTE")),
            tzinfo=pytz.timezone("Europe/Rome")
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
