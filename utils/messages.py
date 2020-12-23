"""
@Author: Abel Hristodor
@Description: SDA (AZS) Telegram bot made for Romanian churches
@Date: 10/12/2020
@Github: github.com/AbelHristodor/azs-telegram-bot

Contains the messages used by the bot.

"""
WELCOME_MESSAGE = "<i>Bine ati venit in grupul Bisericii Adventiste de Ziua a Saptea din Verona: <strong>$user</strong> </i>"
START_MESSAGE = "<strong>Buna tuturor, eu sunt Toby, si sunt aici sa va ajut cu ce aveti nevoie</strong>\n"
HELP_MESSAGE = """
    Comenzi disponibile:\n
        - /zilnic --> Pentru a configura devotionalul zilnic

        - /dev --> Alege din meniu ce devotional ai vrea sa citesti

        - /majori --> Citeste devotional Majori
        - /tineri --> Citeste devotional Tineri
        - /explo --> Citeste devotional Exploratori

        - /setari --> Arata setarile actuale

        - /ajutor --> Va va arata acest mesaj din nou

    Lista comenzilor este in reactualizare continua.
"""
COMMAND_NOT_FOUND_MESSAGE = "Imi pare rau, nu cred ca inteleg.\nIncearca /ajutor pentru a vedea cum pot sa te ajut!"
DATABASE_ERROR_MESSAGE = "Imi pare rau, se pare ca este o problema cu baza de date, incearca mai tarziu"
START_CONFIGURE_SETTINGS_MESSAGE = """
    Buna, aici vom personaliza setarile mele.
    Ai vrea sa incepi?
"""
CURRENT_SETTINGS_MESSAGE = """
<i> Setari actuale </i>
    Devotional Zilnic:
        Status: <strong>$activat</strong>
        In fiecare zi la ora: $dev_time
        Tip devotional: $dev_type
"""
SETTINGS_SUCCESS = "Setari memorizate. Multumesc\n"
UNKNOWN_CHOICE_MESSAGE = "Nu cred ca inteleg, incearca din nou\n"
AFFIRMATIVE_ANSWER = "Da"
NEGATIVE_ANSWER = "Nu"
DEVOTIONAL_TYPES = ['Majori', 'Tineri', 'Exploratori']
YOUR_CHOICE = "Ati ales <strong>$choice</strong>\n"
QUESTION_RECEIVE_DAILY_DEVOTIONAL = "Vrei sa primesti devotionalul zilnic?\n"
QUESTION_WHICH_DEVOTIONAL = "Ce devotional ati vrea sa primiti?\n"
GOODBYE = "La revedere!\n"
