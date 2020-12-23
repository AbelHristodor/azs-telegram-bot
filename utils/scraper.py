"""
@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot

This module contains the scraper used to scrape data from the web.
At the moment it is used for scraping devotional.

"""
import os
import datetime
import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

load_dotenv()


class Scraper():
    """ Scraper main class"""

    def __init__(self) -> None:
        """ Init method """
        self.today = None

    def initialize(self, url:str) -> None:
        """ Initializes the connection to a website and sets the current date"""
        self.today = datetime.date.today().strftime("%d-%m-%Y")
        return requests.get(url)

    def get_devotional(self, dev_type:str = "Majori") -> str:
        """ Scrapes the devotional """
        if dev_type:
            subject = ""
            url = f"{os.getenv('MY_BIBLE_URL')}/{self.today}"
            if dev_type == "Tineri":
                subject = "Tineri"
            elif dev_type == "Exploratori":
                subject = "Exploratori"
                url += "/pathfinder"

            page = self.initialize(url=url)
            soup = bs(page.content, 'html.parser')
            divs = soup.find_all("div", class_="content")
            res = []
            for x in divs:
                for i in x.find_all("p"):
                    res.append(i.get_text() + " ")

            res.insert(0, f"<strong>{self.today}\nDevotional {subject}:</strong>\n")
            res[1] = "<i>" + res[1] + "</i>\n"
            res = [x + "\n" for x in res]
            res = ''.join(res)

        if dev_type == 'Majori':
            page = self.initialize(url=os.getenv('VIATASISANATATE_URL'))
            soup = bs(page.content, 'html.parser')
            data = soup.find("div", {"id": "articol-cms"})
            verset = data.p.get_text()
            verset = data.text.replace(verset, f"<i>{verset}</i>\n")

            res = f"<strong>{self.today}\nDevotional Majori:</strong>\n" + verset

        return res
