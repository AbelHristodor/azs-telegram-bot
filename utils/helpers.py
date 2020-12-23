"""
@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot

Contains some helper functions.
"""
import os
import logging
import dotenv
from .db_service import get_user_by_chat_id

dotenv.load_dotenv()
logger = logging.getLogger(__name__)

def get_current_settings(chat_id):
    """ Gets current settings for user """
    user = get_user_by_chat_id(chat_id)
    dev_type = user["config"][0]["devotional_type"]
    dev_time = "{}:{}".format(os.getenv("DAILY_DEVOTIONAL_HOUR"), os.getenv("DAILY_DEVOTIONAL_MINUTE"))
    settings = {
        "dev_status": "Activat" if dev_type else "Dezactivat",
        "dev_type": dev_type,
        "dev_time": dev_time
    }

    return settings
