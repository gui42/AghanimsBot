from dota2 import Dota


def print_resume_game(game: Dota):
    h_damage = game.highest_damage
    h_nw = game.highest_nw
    first_blood = game.first_blood
    duration = game.duration
    radiant_score = game.radiant_score
    dire_score = game.dire_score
    big_string = f"{'<b><u>Radiant</u></b>' if game.winner=='radiant' else '<b>Radiant</b>'} {radiant_score} : " \
                 f"{dire_score} {'<u><b>Dire</b></u>' if game.winner =='dire' else '<b>Dire</b>'}\n" \
                 f"<b>{h_damage['hero']}</b> did a total of {h_damage['hero_damage']} <b>hero damage</b>\n" \
                 f"<b>First blood</b> was struck at {first_blood[0]} by <b>{first_blood[1]['hero']}</b>\n" \
                 f"The hero with the highest <b>net work</b> was <b>{h_nw['hero']}</b>" \
                 f" with {h_nw['total_gold']} total gold\n" \
                 f"The game lasted {duration[0]+' hour' if duration[0] > 0 else ''} " \
                 f"{duration[1]} minutes and {duration[2]} seconds\n" \
                 f"<a href='{game.OpenDota}'><i>OpenDota</i></a>"
    return big_string


def print_recent_game(steam32):
    this_player, game = Dota.last_game(steam32)
    radiant_score = game.radiant_score
    dire_score = game.dire_score
    duration = game.duration
    big_string = f"<b>{'<u>Radiant</u><' if game.winner == 'radiant' else 'Radiant'}</b> {radiant_score} : " \
                 f"{dire_score} <b>{'<u>Dire</u>' if game.winner == 'dire' else 'Dire'}</b>\n" \
                 f"<b>{this_player['hero']}</b> was playing for the <b>{this_player['team'].title()}</b>\n" \
                 f"<b>K/D/A</b>: {this_player['kills']:02d}/{this_player['deaths']:02d}/{this_player['assists']:02d} " \
                 f"<b>GPM</b>: {this_player['gold_per_min']} <b>XPM</b>: {this_player['xp_per_min']}\n" \
                 f"<b>Net Worth</b>: {this_player['total_gold']} total gold\n" \
                 f"<b>Hero Damage</b>: {this_player['hero_damage']}  " \
                 f"<b>Tower Damage</b>: {this_player['tower_damage']}\n" \
                 f"<b>Last Hits</b>: {this_player['last_hits']} " \
                 f"<b>Level</b>: {this_player['level']}\n" \
                 f"The game lasted {duration[0]+' hours ' if duration[0]>0 else ''}" \
                 f"{duration[1]} minutes and {duration[2]} seconds\n"\
                 f"<a href='{game.OpenDota}'>OpenDota</a>"
    return big_string

