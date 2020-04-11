import logging, random, telegram.ext
from telegram.ext import Updater, CommandHandler
from dota2 import Dota
from printer import print_resume_game, print_recent_game, print_match_ups, print_player_resume


def open_token():
    try:
        with open('token.txt') as f:
            lines = f.read().splitlines()
            print('got it')
            return lines[0]
    except FileNotFoundError as e:
        raise FileNotFoundError("Couldn't find the file")


try:
    all_heroes = Dota.request_all_heroes()
    print('got all heroes')
except ValueError:
    all_heroes = None
    print("bad request at main request all heroes")

token = open_token()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def help_(update, context):
    long_string = f"<b>Commands:</b>\n" \
                  f"\n/posdota - Will assign a random Dota 2 position\n" \
                  f"/roll - Returns  a random number between 1 and 100\n" \
                  f"/flip - returns <i>Heads</i> or <i>Tails</i>\n" \
                  f"\n<b>Pulling info from Dota matches:</b>\n" \
                  f"\n/lastmatch <i>steam32</i> - Get's information on the last game of the player\n" \
                  f"/player <i>steam32</i> - Returns a resume of the player's profile, including rank, most played " \
                  f"heroes and win rate\n" \
                  f"/matchup <i>hero</i> - Returns heroes with a high win rate against the <i>hero</>\n" \
                  f"/match <i>match ID</i> - returns some basic status about a match\n" \
                  f"\n<a href='https://steamid.xyz/'>Discover your Steam32 ID</a>\n" \
                  f"\nIf you want to know more about me, you can go to my" \
                  f" <a href='https://github.com/gui42/AghanimsBot'>GitHub</a> page\n" \
                  f"\nSuggestions: aghanimsbot@pm.me"
    context.bot.send_message(chat_id=update.effective_chat.id, text=long_string, disable_web_page_preview=True,
                             parse_mode=telegram.ParseMode.HTML)


def pos_dota(update, context):
    pos = ['Safe lane', 'Mid lane', 'Offlane', 'Soft Support', 'Hard Support']
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
    long_string = f"Hi, I'm a bot that can help you show off your Dota2 matches to your telegram groups!\n"\
                  f"To learn more about me, you can use <b>/help</b>, visit my "\
                  f"<a href='https://github.com/gui42/AghanimsBot'>GitHub</a> " \
                  f"page or send me a email at aghanimsbot@pm.me"

    context.bot.send_message(chat_id=update.effective_chat.id, text=long_string,
                             disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)


def player_resume(update, context):
    error1 = 'Something went wrong'
    steam_id = ''.join(context.args)
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=print_player_resume(steam_id, all_heroes),
                                 disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error1,
                                 disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)


def last_match(update, context):
    error = "Invalid steam 32 ID.\n" \
            "<a href='https://steamid.xyz/'>Check your ID</a>"

    error2 = "something went wrong".title()

    text = ''.join(context.args)

    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=print_recent_game(text, all_heroes),
                                 disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error, disable_web_page_preview=True,
                                 parse_mode=telegram.ParseMode.HTML)
    except NameError:
        update.message.reply_text(error2)


def match_up(update, context):
    text = "".join(context.args)
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=print_match_ups(text, all_heroes),
                                 disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
    except NameError:
        update.message.reply_text("hero could not be found".title())
    except ValueError:
        update.message.reply_text("No hero name given".title())


def match(update, context):
    user_says = " ".join(context.args)
    user_says = user_says.strip()
    try:
        game = Dota(user_says, all_heroes)
        context.bot.send_message(chat_id=update.effective_chat.id, text=print_resume_game(game),
                                 disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
    except ValueError:
        update.message.reply_text("Invalid Dota2 match ID")


# start and add handlers
flip_coin_handler = CommandHandler('flip', flip_coin)
pos_dota_handler = CommandHandler('dotapos', pos_dota)

dispatcher.add_handler(CommandHandler('player', player_resume))
dispatcher.add_handler(CommandHandler('help', help_))
dispatcher.add_handler(CommandHandler('lastmatch', last_match))
dispatcher.add_handler(CommandHandler('matchup', match_up))
dispatcher.add_handler(CommandHandler("match", match))
dispatcher.add_handler(CommandHandler("roll", roll))
dispatcher.add_handler(flip_coin_handler)
dispatcher.add_handler(pos_dota_handler)
dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()


#aghanimsbot@pm.me
