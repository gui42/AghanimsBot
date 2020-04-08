import logging
import random
import telegram.ext
from telegram.ext import Updater, CommandHandler
from dota2 import Dota
from printer import print_resume_game


def open_token():
    try:
        with open('token.txt') as f:
            lines = f.read().splitlines()
            print('got it')
            return lines[0]
    except FileNotFoundError as e:
        raise FileNotFoundError("Couldn't find the file")


token = open_token()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def help_(update, context):
    long_string = f"<b>Commands:</b>\n" \
                  f"\n/posdota - Will assign a random Dota 2 position\n" \
                  f"/roll - Returns  a random number between 1 and 100\n" \
                  f"/flip - returns <i>Heads</i> or <i>Tails</i>\n" \
                  f"<a href='https://steamid.xyz/'>Discover your Steam32</a>\n" \
                  f"\n<b>Pulling info from Dota matches:</b>\n" \
                  f"\n/lastmatch <i>steam32</i> - Get's information on the last game of the player\n" \
                  f"/matchup <i>hero</i> - Returns heroes with a high win rate against the <i>hero</>\n" \
                  f"/match <i>match ID</i> - returns some basic status about a match\n" \
                  f"\n<a href='https://steamid.xyz/'>Discover your Steam32</a>\n" \
                  f"Suggestions: aghanimsbot@pm.me"
    context.bot.send_message(chat_id=update.effective_chat.id, text=long_string, disable_web_page_preview=True,
                             parse_mode=telegram.ParseMode.HTML)


def pos_dota(update, context):
    pos = ['hc', 'mid', 'offlaner', 'sup', 'hard sup']
    pos_f = pos[random.randint(0, 4)]
    string = f'Play as {pos_f}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=string)


def roll(update, context):
    rand = random.randint(1, 100)
    context.bot.send_message(chat_id=update.effective_chat.id, text=rand)


def flip_coin(update, context):
    coin = ['tails', 'heads']
    context.bot.send_message(chat_id=update.effective_chat.id, text=coin[random.randint(0, 1)].title())


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot that can get details of Dota 2 matches")


def last_match(update, context):
    error = "Invalid steam 32 ID.\n" \
            "https://steamid.xyz/"
    error2 = "check if the profile is public"
    text = ''.join(context.args)
    try:
        last_game = Dota.last_game(text)
        update.message.reply_text(last_game)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat_id, text=error, disable_web_page_preview=True)
    except NameError:
        update.message.reply_text(error2)


def match_up(update, context):
    text = "".join(context.args)
    try:
        update.message.reply_text(Dota.match_up(text))
    except NameError:
        update.message.reply_text("hero could not be found".title())
    except ValueError:
        update.message.reply_text("No hero name given".title())


def match(update, context):
    user_says = " ".join(context.args)
    user_says = user_says.strip()
    try:
        game = Dota(user_says)
        context.bot.send_message(chat_id=update.effective_chat.id, text=print_resume_game(game),
                                 disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
    except ValueError:
        update.message.reply_text("Invalid Dota2 match ID")


# start and add handlers
flip_coin_handler = CommandHandler('flip', flip_coin)
pos_dota_handler = CommandHandler('dotapos', pos_dota)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(CommandHandler('help', help_))
dispatcher.add_handler(CommandHandler('lastmatch', last_match))
dispatcher.add_handler(CommandHandler('matchup', match_up))
dispatcher.add_handler(CommandHandler("match", match))
dispatcher.add_handler(CommandHandler("roll", roll))
dispatcher.add_handler(flip_coin_handler)
dispatcher.add_handler(pos_dota_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()


#aghanimsbot@pm.me