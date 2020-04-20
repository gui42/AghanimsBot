from telegram.ext import Updater, CommandHandler
import random


def start(update, context):
    text1 = 'It works!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text1, disable_web_page_preview=True)


def flip(update, context):
    opt = ['Heads', 'Tails']
    context.bot.send_message(chat_id=update.effective_chat.id, text=opt[random.randint(0, 1)])


def roll(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.randint(0, 100))


def random_dota_position(update, context):
    opts = ['Safe Lane', 'Mid Lane', 'Offlane', 'Soft Support', 'Hard Support']
    context.bot.send_message(chat_id=update.effective_chat.id, text=opts[random.randint(0, 4)])