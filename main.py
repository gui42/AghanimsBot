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
    string = f'Jogue de {pos_f}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=string)


def roll(update, context):
    rand = random.randint(1, 100)
    if rand == 42:
        context.bot.send_message(chat_id=update.effective_chat.id, text="2A")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=rand)


def flip_coin(update, context):
    coin = ['tails', 'heads']
    context.bot.send_message(chat_id=update.effective_chat.id, text=coin[random.randint(0, 1)].title())


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot that can get details of Dota 2 matches")


def creditos(update, context):
    string = 'Guilherme Hermes - guilherme.hermes@pm.me '
    context.bot.send_message(chat_id=update.effective_chat.id, text=string)


def matchup(update, context):
    text = "".join(context.args)
    update.message.reply_text(Dota.match_up(text))


def start_callback(update, context):
    user_says = " ".join(context.args)
    user_says = user_says.strip()
    try:
        game = Dota(user_says)
        update.message.reply_text(game.print_resume)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid Dota2 match ID")
    except NameError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, for some reason I couldn't reach "
                                                                        "OpenDota right now")


# start and add handlers
creditos_handler = CommandHandler('creditos', creditos)
flip_coin_handler = CommandHandler('flip', flip_coin)
pos_dota_handler = CommandHandler('dotapos', pos_dota)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(CommandHandler('matchup', matchup))
dispatcher.add_handler(CommandHandler("callback", start_callback))
dispatcher.add_handler(CommandHandler("roll", roll))
dispatcher.add_handler(creditos_handler)
dispatcher.add_handler(flip_coin_handler)
dispatcher.add_handler(pos_dota_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
