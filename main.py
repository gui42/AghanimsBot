import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dota2 import Dota


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


def help(update, context):
    long_string = f"{'posdota'.title()}: Will assign a random Dota 2 position to play\n" \
                  f"{'roll'.title()}: Returns  a random number between 1 and 100\n" \
                  f"{'flip'.title()}: returns Heads or Tails\n" \
                  f"{'lastmastch'.title()} {'x'*8}: where x are the numbers on your STEAM32 ID " \
                  f"to discover your steam32 ID: https://steamid.xyz/\n" \
                  f"{'matchup'.title()} {'{hero name}'}: Returns a list with the heroes with the" \
                  f" highest win rate against {'{hero name}'}\n" \
                  f"{'match'.title()} {'x'*10}: returns some basic status about a match\n" \
                  f"Suggestions: aghanimsbot@pm.me"
    context.bot.send_message(chat_id=update.effective_chat.id, text=long_string)


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
        update.message.reply_text(error)
    except NameError:
        update.message.reply_text(error2)


def match_up(update, context):
    text = "".join(context.args)
    try:
        update.message.reply_text(Dota.match_up(text))
    except NameError:
        update.message.reply_text('hero not found'.title())

def match(update, context):
    user_says = " ".join(context.args)
    user_says = user_says.strip()
    try:
        game = Dota(user_says)
        context.bot.send_message(chat_id=update.effective_chat.id, text=game.print_resume)
    except ValueError:
        update.message.reply_text("Invalid Dota2 match ID")


# start and add handlers
flip_coin_handler = CommandHandler('flip', flip_coin)
pos_dota_handler = CommandHandler('dotapos', pos_dota)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('lastmatch', last_match))
dispatcher.add_handler(CommandHandler('matchup', match_up))
dispatcher.add_handler(CommandHandler("match", match))
dispatcher.add_handler(CommandHandler("roll", roll))
dispatcher.add_handler(flip_coin_handler)
dispatcher.add_handler(pos_dota_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()


#aghanimsbot@pm.me