from dota2 import Dota
import ranktier


def print_resume_game(game: Dota):
    h_damage = game.highest_damage
    h_nw = game.highest_nw
    first_blood = game.first_blood
    duration = game.duration
    radiant_score = game.radiant_score
    dire_score = game.dire_score
    winner = game.winner
    big_string = f"<b>{'<u>Radiant</u>' if winner=='radiant' else 'Radiant'}</b> {radiant_score} : " \
                 f"{dire_score} <b>{'<u>Dire</u>' if winner =='dire' else 'Dire'}</b>\n" \
                 f"<b>{h_damage['hero']}</b> did a total of {h_damage['hero_damage']} <b>hero damage</b>\n" \
                 f"<b>First blood</b> was struck at {first_blood[0]} by <b>{first_blood[1]['hero']}</b>\n" \
                 f"The hero with the highest <b>net work</b> was <b>{h_nw['hero']}</b>" \
                 f" with {h_nw['total_gold']} total gold\n" \
                 f"The game lasted {duration[0]+' hours ' if duration[0] > 0 else ''}" \
                 f"{duration[1]} minutes and {duration[2]} seconds\n" \
                 f"<a href='{game.OpenDota}'><i>OpenDota</i></a>"
    return big_string


def print_recent_game(steam32, all_heroes=None):
    this_player, game = Dota.last_game(steam32, all_heroes)
    radiant_score = game.radiant_score
    dire_score = game.dire_score
    duration = game.duration
    big_string = f"<b>{'<u>Radiant</u><' if game.winner == 'radiant' else 'Radiant'}</b> {radiant_score} : " \
                 f"{dire_score} <b>{'<u>Dire</u>' if game.winner == 'dire' else 'Dire'}</b>\n" \
                 f"<b>{this_player['hero']}</b> was playing for the <b>{this_player['team'].title()}</b>\n" \
                 f"<b>K/D/A</b>: {this_player['kills']:02d}/{this_player['deaths']:02d}/{this_player['assists']:02d} " \
                 f"<b>GPM</b>: {this_player['gold_per_min']} <b>XPM</b>: {this_player['xp_per_min']}\n" \
                 f"<b>Net Worth</b>: {this_player['total_gold']} total gold\n" \
                 f"<b>Hero Damage</b>: {this_player['hero_damage']}\n" \
                 f"<b>Tower Damage</b>: {this_player['tower_damage']}\n" \
                 f"<b>Creep Score</b>: {this_player['last_hits']}/{this_player['denies']} " \
                 f"<b>Level</b>: {this_player['level']}\n" \
                 f"The game lasted {duration[0]+' hours ' if duration[0]>0 else ''}" \
                 f"{duration[1]} minutes and {duration[2]} seconds\n"\
                 f"<a href='{game.OpenDota}'>OpenDota</a>"
    return big_string


def print_match_ups(hero_id, all_heroes=None):
    this_hero, match_ups = Dota.match_up(hero_id, all_heroes)
    big_string = f"<u>Counters for <b>{this_hero['localized_name']}</b></u>:\n"
    for x in range(0, 5):
        big_string = big_string+f"<b>{match_ups[x]['hero']}</b>: " \
                                f"{'<i>'+match_ups[x]['odds']+'</i>'}%\n"
    return big_string


def print_player_resume(steam_id, all_heroes=None):
    win_lose = Dota.request_win_loss(steam_id)
    player = Dota.request_player(steam_id)
    best_heroes = Dota.best_heroes(steam_id, all_heroes)
    if win_lose and player and best_heroes:
        rank = player['rank_tier']
        rank = ranktier.Rank(rank)
        win_lose['odds'] = win_lose['win']/(win_lose['win']+win_lose['lose'])
        big_string = f"<b>Player</b>:{player['profile']['personaname']} {'<b>D+</b>'if player['profile']['plus'] else ''}:\n" \
                     f"<b>Wins</b>: {win_lose['win']}\n" \
                     f"<b>Win%</b>: {(win_lose['odds']*100):02.02f}%\n" \
                     f"<b>Total games</b>: {win_lose['win']+win_lose['lose']}\n" \
                     f"<b>Rank</b>: <i>{rank}</i>\n" \
                     f"<u>Most Played Heroes</u>:\n"
        for x in range(0, 5):
            big_string = big_string+f"<b>{best_heroes[x]['localized_name']}</b> - <b>WR</b>: " \
                                    f"{((best_heroes[x]['win']/best_heroes[x]['games'])*100):02.02f}% " \
                                    f"<b>T. Games</b>: {best_heroes[x]['games']}\n"
        big_string = big_string+f"<a href='https://www.opendota.com/players/{steam_id}'>OpenDota profile</a>"
        return big_string
    else:
        raise ValueError("win_loss = null or player = null or best_heroes = null")
