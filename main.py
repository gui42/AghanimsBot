import telegram.ext
import src.BasicDota as BasicDota
import src.Printer as Printer
from telegram.ext import Updater, CommandHandler
from src.Helpers import request_and_create_all_heroes, init_bot

def main():
    config = init_bot()
    updater = Updater(config['token'], use_context=True)
    print(f"[OK]\t{'Free' if config['openDota'] == 'free' else 'Paid'} OpenDota API")
    request_and_create_all_heroes()

    # setting up the dispatcher and handlers and whatnot
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', BasicDota.start))
    dispatcher.add_handler(CommandHandler('flip', BasicDota.flip))
    dispatcher.add_handler(CommandHandler('roll', BasicDota.roll))
    dispatcher.add_handler(CommandHandler('help', BasicDota.help_))
    dispatcher.add_handler(CommandHandler('dotapos', BasicDota.random_dota_position))
    dispatcher.add_handler(CommandHandler('match', match))
    dispatcher.add_handler(CommandHandler('lastmatch', last_match))
    dispatcher.add_handler(CommandHandler('player', player_profile))

    print('[OK]\tPolling')
    updater.start_polling()


def match(update, context):
    error1 = f"Need a match ID"
    error2 = "Something went wrong..."
    match_id = ''.join(context.args)

    if match_id == '':
        context.bot.send_message(chat_id=update.effective_chat.id, text=error1,
                                 parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        return
    try:
        long_string = Printer.print_match(match_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=long_string,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error2,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except NameError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid Dota 2 match ID")


def last_match(update, context):
    error_value = "something went wrong..."
    error_name = "Invalid player ID"
    account_id = ''.join(context.args)
    if account_id == '':
        context.bot.send_message(chat_id=update.effective_chat.id, text="<i>Steam32 ID</i> necessary",
                                 parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        return
    try:
        long_string = Printer.player_last_match(account_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=long_string,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except ValueError as error:
        if error.args[1] == 404:
            error_value = "Profile not found"
        elif error.args[1] > 500:
            error_value = "OpenDota seems to be down"
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_value,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except NameError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_name,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


def player_profile(update, context):
    error_value = "something went wrong"
    account_id = ''.join(context.args)
    if account_id == '':
        context.bot.send_message(chat_id=update.effective_chat.id, text="<i>Steam 32 ID</i> necessary",
                                 parse_mode=telegram.ParseMode.HTML)
        return        
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=Printer.print_player_profile(account_id),
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except ValueError as error:
        if error.args[1] > 500:
            error_value= "OpenDota seems to be down"
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_value,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except NameError:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid steam 32 ID')
        
                                                                                                                                                                        

if __name__ == '__main__':
    main()
