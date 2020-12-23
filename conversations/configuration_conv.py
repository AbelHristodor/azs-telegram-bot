# pylint: disable=unused-argument, line-too-long
"""
@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot

Contains the settings' configurator conversation

"""
import logging
from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

from utils.db_service import chat_id_exists, insert_user, update_user_by_chat_id
from utils.messages import (
    START_CONFIGURE_SETTINGS_MESSAGE,
    SETTINGS_SUCCESS,
    UNKNOWN_CHOICE_MESSAGE,
    DATABASE_ERROR_MESSAGE,
    AFFIRMATIVE_ANSWER,
    NEGATIVE_ANSWER,
    DEVOTIONAL_TYPES,
    QUESTION_RECEIVE_DAILY_DEVOTIONAL,
    QUESTION_WHICH_DEVOTIONAL,
    YOUR_CHOICE,
    GOODBYE
)

logger = logging.getLogger(__name__)
BEGIN, DEVOTIONAL, DEVOTIONAL_TYPE = range(3)


def settings_start(update: Update, context: CallbackContext) -> int:
    """ Sets the user's settings """
    keyboard = [[AFFIRMATIVE_ANSWER, NEGATIVE_ANSWER]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(text=START_CONFIGURE_SETTINGS_MESSAGE, reply_markup=reply_markup)

    return BEGIN


def settings_daily_dev(update: Update, context: CallbackContext) -> int:
    """ Choose to receive or not daily devotional """
    keyboard = [[AFFIRMATIVE_ANSWER, NEGATIVE_ANSWER]]
    if update.message.text == NEGATIVE_ANSWER:
        settings_cancel(update=update, context=context)
        return ConversationHandler.END

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    text = YOUR_CHOICE.replace("$choice", update.message.text) + QUESTION_RECEIVE_DAILY_DEVOTIONAL
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

    return DEVOTIONAL


def settings_choose_daily_dev(update: Update, context: CallbackContext) -> int:
    """ Choose which devotional to receive """
    keyboard = [[DEVOTIONAL_TYPES[0], DEVOTIONAL_TYPES[1]], [DEVOTIONAL_TYPES[2]]]
    if update.message.text == NEGATIVE_ANSWER:
        settings_cancel(update=update, context=context)
        return ConversationHandler.END

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        text=YOUR_CHOICE.replace("$choice", update.message.text) + QUESTION_WHICH_DEVOTIONAL,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

    return DEVOTIONAL_TYPE


def settings_finish(update: Update, context: CallbackContext) -> int:
    """ Settings finish"""
    devotional_type = update.message.text
    chat_id = update.effective_chat.id

    update.message.reply_text(
        text=YOUR_CHOICE.replace("$choice", devotional_type),
        parse_mode=ParseMode.HTML
    )

    if devotional_type not in DEVOTIONAL_TYPES:
        devotional_type = DEVOTIONAL_TYPES[0]

    data = {
        "username": update.effective_user.username,
        "chat_id": chat_id,
        "config": [
            {
                "devotional_type": devotional_type
            }
        ]
    }

    chat_exists = chat_id_exists(chat_id)
    if chat_exists:
        update_data = { "$set": data}
        query = update_user_by_chat_id(chat_id, update_data)
    else:
        query = insert_user(data)

    if query:
        update.message.reply_text(text=SETTINGS_SUCCESS, reply_markup={"remove_keyboard": True}, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text=DATABASE_ERROR_MESSAGE, reply_markup={"remove_keyboard": True}, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def settings_cancel(update: Update, context: CallbackContext) -> int:
    """ Ends the conversation """
    reply_markup = {"remove_keyboard": True}
    update.message.reply_text(text=GOODBYE, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def unknown_choice(update: Update, context: CallbackContext, text: str = UNKNOWN_CHOICE_MESSAGE) -> None:
    """ Handles not recognized commands sent in the chat """
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


configuration_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('zilnic', settings_start, run_async=True)],
    states={
        BEGIN: [MessageHandler(Filters.regex(f'^({AFFIRMATIVE_ANSWER}|{NEGATIVE_ANSWER})$'), settings_daily_dev, run_async=True)],
        DEVOTIONAL: [MessageHandler(Filters.regex(f'^({AFFIRMATIVE_ANSWER}|{NEGATIVE_ANSWER})$'), settings_choose_daily_dev, run_async=True)],
        DEVOTIONAL_TYPE: [MessageHandler(Filters.regex(f'^({DEVOTIONAL_TYPES[0]}|{DEVOTIONAL_TYPES[1]}|{DEVOTIONAL_TYPES[2]})',), settings_finish, run_async=True)]
    },
    fallbacks=[CommandHandler('cancel', settings_cancel, run_async=True)]
)
