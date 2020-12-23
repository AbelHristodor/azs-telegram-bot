"""
@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot

This module contains serves some methods that interact with the database

"""
import os
import logging
import dotenv
from pymongo.errors import PyMongoError
from pymongo import MongoClient

logger = logging.getLogger(__name__)
dotenv.load_dotenv()

db_client = MongoClient(os.getenv('MONGODB_URI'))
db = db_client.TobyBot.test_bot_collection

def chat_id_exists(chat_id: int) -> bool:
    """ Checks if chat_id exists already in db """
    try:
        result = db.find_one({"chat_id": chat_id})
        if result is None:
            return False
        else:
            return True
    except Exception as db_error:
        logger.exception("Database Error: %s", db_error)


def insert_user(data: dict) -> bool:
    """ Inserts user in db """
    try:
        result = db.insert_one(data)
        if result.inserted_id:
            logger.info("Db insert executed successfully")
            return True
    except PyMongoError as db_error:
        logger.exception("Database Error: %s", db_error)
    return False


def get_all_users() -> list:
    """ Gets all users from the db """
    try:
        result = list(db.find({}))
        return result
    except PyMongoError as db_error:
        logger.exception("Database Error: %s", db_error)
        return []


def update_user_by_chat_id(chat_id, data) -> bool:
    """ Updates user in db """
    try:
        result = db.update_one({"chat_id": chat_id}, data)
        if result.matched_count > 0:
            logger.info("Db update executed successfully")
            return True
    except PyMongoError as db_error:
        logger.exception("Database Error: %s", db_error)
        return False
    return False


def get_user_by_chat_id(chat_id: int) -> dict:
    """ Get one user from db """
    try:
        result = db.find_one({"chat_id": chat_id})
        if result:
            logger.info("Db get executed successfully")
            return result
    except PyMongoError as db_error:
        logger.exception("Database Error: %s", db_error)
        return {}
    return {}
