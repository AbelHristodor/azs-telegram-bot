# AZS - Telegram Bot
Simple telegram bot for SDA churches that helps communicating with members.
At the moment it allowes to request devotionals for children, the youth and adults.

## Bootstrap
Git clone the repo, duplicate and rename ```.env.example``` file in ```.env``` and paste your token in there (check [Telegram's Bot API to get the token](https://core.telegram.org/bots))

When ready run:
```pip install -r requirements.txt```
and then start the bot using:
```python3 main.py```
___
*Make sure you have python 3 and pip installed otherwise run:*
### *On Linux OS*

 ```
  sudo apt-get update
  sudo apt-get install python3-pip
  ```
### On Windows
Check [Python's Official Website](https://www.python.org/)

_____

### Supported features:
- Get Devotionals for the youth, children and adults
- Set up Daily daily devotionals

*Currently under development*

For more information check [Python-Telegram-Bot's Repository](https://core.telegram.org/bots)

To host your bot see [Python-Telegram-Bot - Hosting](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot)
