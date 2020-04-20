import telegram.ext
import BasicDota
from telegram.ext import Updater, CommandHandler

import printer


def main():
    updater = Updater(open_token(), use_context=True)

    # setting up the dispatcher and handlers and whatnot
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', BasicDota.start))
    dispatcher.add_handler(CommandHandler('flip', BasicDota.flip))
    dispatcher.add_handler(CommandHandler('roll', BasicDota.roll))
    dispatcher.add_handler(CommandHandler('dotapos', BasicDota.random_dota_position))
    dispatcher.add_handler(CommandHandler('match', match))
    dispatcher.add_handler(CommandHandler('lastmatch', last_match))
    dispatcher.add_handler(CommandHandler('profile', player_profile))

    updater.start_polling()


def match(update, context):
    match_id = ''.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=printer.print_match(match_id),
                             parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


def last_match(update, context):
    player_id = ''.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=printer.print_last_match(player_id),
                             parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


def player_profile(update, context):
    account_id = ''.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=printer.print_player_profile(account_id),
                             parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


def open_token():
    with open('token.txt') as f:
        lines = f.read().splitlines()
        return lines[0]


if __name__ == '__main__':
    main()
