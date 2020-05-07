import telegram.ext
from telegram.ext import Updater, CommandHandler
import random


def start(update, context):
    text1 = "Welcome to the <b>Aghanim's Bot</b>!\n" \
            "I'm able to get some status on Dota 2 matches or players.\n" \
            "If you want to know more about me, you can use the /help command, " \
            "visit my " \
            "<a href='https://github.com/gui42/AghanimsBot'>GitHub</a> page or " \
            "send me a email at aghanimsbot@pm.me"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text1,
                             parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


def flip(update, context):
    opt = ['Heads', 'Tails']
    context.bot.send_message(chat_id=update.effective_chat.id, text=opt[random.randint(0, 1)])


def roll(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.randint(0, 100))


def random_dota_position(update, context):
    opts = ['Safe Lane', 'Mid Lane', 'Offlane', 'Soft Support', 'Hard Support']
    context.bot.send_message(chat_id=update.effective_chat.id, text=opts[random.randint(0, 4)])


def help_(update, context):
    long_string = f"<b>Commands:</b>\n" \
                  f"\n/posdota - Will assign a random Dota 2 position\n" \
                  f"/roll - Returns  a random number between 1 and 100\n" \
                  f"/flip - returns <i>Heads</i> or <i>Tails</i>\n" \
                  f"\n<b>Pulling info from Dota matches:</b>\n" \
                  f"\n/lastmatch <i>steam32</i> - Get's information on the last game of the player\n" \
                  f"/player <i>steam32</i> - Returns a resume of the player's profile, including rank, most played " \
                  f"heroes and win rate\n" \
                  f"/match <i>match ID</i> - returns some basic status about a match\n" \
                  f"\n<b>If your <i>Steam32 ID</i> ins't working, try logging on" \
                  f" <a href='https://www.opendota.com/'>OpenDota</a> first</b>\n" \
                  f"\n<a href='https://steamid.xyz/'>Discover your Steam32 ID</a>\n" \
                  f"\nIf you want to learn more about me, you can go to my" \
                  f" <a href='https://github.com/gui42/AghanimsBot'>GitHub</a> page\n" \
                  f"\nSuggestions: aghanimsbot@pm.me"
    context.bot.send_message(chat_id=update.effective_chat.id, text=long_string, disable_web_page_preview=True,
                             parse_mode=telegram.ParseMode.HTML)


def dots(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://images2.alphacoders.com/474/474206.jpg")
