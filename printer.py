from dota2 import Dota


def print_resume_game(game: Dota):
    h_damage = game.highest_damage
    h_nw = game.highest_nw
    first_blood = game.first_blood
    duration = game.duration
    big_string = f"{'<b><u>Radiant</u></b>' if game.winner=='radiant' else '<b>Radiant</b>'} {game.radiant_score} : " \
                 f"{game.dire_score} {'<u><b>Dire</b></u>' if game.winner =='dire' else '<b>Dire</b>'}\n" \
                 f"<b>{h_damage['hero']}</b> did a total of {h_damage['hero_damage']} <b>hero damage</b>\n" \
                 f"<b>First blood</b> was struck at {first_blood[0]} by <b>{first_blood[1]['hero']}</b>\n" \
                 f"The hero with the highest <b>net work</b> was <b>{h_nw['hero']}</b>" \
                 f" with {h_nw['total_gold']} total gold\n" \
                 f"The game lasted for{duration[0]+' hour' if duration[0] > 0 else ''} " \
                 f"{duration[1]} minutes and {duration[2]} seconds\n" \
                 f"<a href='{game.OpenDota}'><i>OpenDota</i></a>"
    return big_string
