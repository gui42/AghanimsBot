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
    text = ''.join(context.args)
    try:
        last_game = Dota.last_game(text)
        update.message.reply_text(last_game)
    except ValueError:
        update.message.reply_text(error)


def matchup(update, context):
    text = "".join(context.args)
    update.message.reply_text(Dota.match_up(text))


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

dispatcher.add_handler(CommandHandler('lastmatch', last_match))
dispatcher.add_handler(CommandHandler('matchup', matchup))
dispatcher.add_handler(CommandHandler("match", match))
dispatcher.add_handler(CommandHandler("roll", roll))
dispatcher.add_handler(flip_coin_handler)
dispatcher.add_handler(pos_dota_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()


#aghanimsbot@pm.me