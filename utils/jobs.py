"""
@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot

Contains the messages used by the bot.

"""
import logging
from telegram import ParseMode
from telegram.ext import CallbackContext

from .db_service import get_all_users
from .scraper import Scraper

scraper = Scraper()
logger = logging.getLogger(__name__)


def send_daily_devotional(context: CallbackContext) -> None:
    """ Send daily the devotional """
    users = get_all_users()
    logging.info("Starting job: %s", send_daily_devotional.__name__)
    if users:
        for user in users:
            devotional_type = user["config"][0]["devotional_type"]
            logger.info("Sending devotional of type: %s to chat_id: %d", devotional_type, user["chat_id"])

            context.bot.send_message(chat_id=user["chat_id"], text=scraper.get_devotional(devotional_type), parse_mode=ParseMode.HTML)
