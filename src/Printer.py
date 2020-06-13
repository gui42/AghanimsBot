import datetime
import Helpers
from Dota import Match, Hero, Player, Request


def print_match(match_id):
    game = Match(match_id)
    duration = datetime.timedelta(seconds=game.duration)
    first_blood = datetime.timedelta(seconds=game.first_blood_time)
    net_worth = get_highest_net_worth(game)
    most_kills = get_most_kills(game)
    tower_damage = get_highest_tower_damage(game)
    hero_heal = get_highest_hero_healing(game)
    long_string = f"<b>{'<u>Radiant</u>' if game.radiant_win else 'Radiant'}</b> {game.radiant_score} " \
                  f": {game.dire_score} <b>{'Dire' if game.radiant_win else '<u>Dire</u>'}</b>\n" \
                  f"<b>Duration</b>: {duration}\n" \
                  f"<b>First Blood</b>: {first_blood} claimed by " \
                  f"<i>{game.first_blood_claimed['hero_info']['localized_name']}</i>\n" \
                  f"<b>High Scores</b>:\n" \
                  f"" \
                  f"<b>Kills</b>: <i>{most_kills['hero_info']['localized_name']}</i> with " \
                  f"{most_kills['kills']} kills\n" \
                  f"" \
                  f"<b>Net Worth</b>: <i>{net_worth['hero_info']['localized_name']}</i> with " \
                  f"{net_worth['gold_spent']} total gold spent\n" \
                  f"" \
                  f"<b>Tower Damage</b>: <i>{tower_damage['hero_info']['localized_name']}</i> " \
                  f"dealt a total of {tower_damage['tower_damage']} damage to towers\n"
    if hero_heal['hero_healing'] > 4000:
        long_string = long_string+f"" \
                                  f"<b>Healing</b>: <i>{hero_heal['hero_info']['localized_name']}</i> " \
                                  f"healed {hero_heal['hero_healing']}\n"
        long_string = long_string+f"<a href='{game.OpenDota}'>OpenDota</a>\n"
    return long_string


def player_last_match(account_id):
    all_heroes = Request.all_heroes()
    match_id = Player.request_recent_matches(account_id)
    match_id = match_id[0]['match_id']
    game = Match(match_id, all_heroes)
    first_blood_time = datetime.timedelta(seconds=game.first_blood_time)
    in_game = game.get_player(account_id)
    duration = datetime.timedelta(seconds=game.duration)
    long_string = f"<b>{'<u>Radiant</u>' if game.radiant_win else 'Radiant'}</b> {game.radiant_score} : " \
                  f"{game.dire_score} <b>{'Dire' if game.radiant_win else '<u>Dire</u>'}</b>\n" \
                  f"<b>Duration</b>: {duration}\n" \
                  f"<b>First blood</b>: {first_blood_time}\n" \
                  f"<b>{in_game['hero_info']['localized_name']}</b> was playing for the" \
                  f" <b>{'Radiant' if in_game['isRadiant'] else 'Dire'}</b>\n" \
                  f"<b>KDA</b>: {in_game['kills']}/{in_game['deaths']}/{in_game['assists']} " \
                  f"<b>GPM</b>: {in_game['gold_per_min']} <b>XPM</b>: {in_game['xp_per_min']}\n" \
                  f"<b>Hero Damage</b>: {in_game['hero_damage']} <b>CS</b>: " \
                  f"{in_game['last_hits']}/{in_game['denies']}\n" \
                  f"<b>Net Worth</b>: {in_game['gold_spent']}\n" \
                  f"<a href='{game.OpenDota}'>OpenDota</a>"
    return long_string


def print_player_profile(account_id):
    all_heroes = Request.all_heroes()
    player = Player(account_id, all_heroes)
    most_played = player.most_played_heroes(player.account_id, all_heroes)
    persona = player.persona_name
    long_string = f"<b>Player</b>: {persona}\n" \
                  f"<b>Wint rate</b>: {(player.win_rate*100):02.0f}%\n" \
                  f"<b>Wins</b>: {player.wins}\n" \
                  f"<b>Total Games</b>: {player.total_games}\n" \
                  f"<b>Rank</b>: {player.rank_tier_human}\n" \
                  f"<u>Most Played Heroes</u>:\n"
    for x in range(0, 5):
        wr = most_played[x]['win']/most_played[x]['games']
        long_string = long_string + f"<b>{most_played[x]['hero_info']['localized_name']}</b>: - " \
                                    f"<b>WR</b>: {(wr*100):02.0f}% <b>T. Games</b>: {most_played[x]['games']}\n"
    long_string = long_string + f"<a href='{player.OpenDota}'>OpenDota Profile</a>"
    return long_string


def get_highest_net_worth(game: Match):
    first = {'total_gold': 0}
    for player in game.players:
        if player['total_gold'] > first['total_gold']:
            first = player
    return first


def get_most_kills(game: Match):
    first = {'kills': 0}
    for player in game.players:
        if player['kills'] > first['kills']:
            first = player
    return first


def get_highest_tower_damage(game: Match):
    first = {'tower_damage': 0}
    for player in game.players:
        if player['tower_damage'] > first['tower_damage']:
            first = player
    return first


def get_highest_hero_healing(game: Match):
    first = {'hero_healing': 0}
    for player in game.players:
        if player['hero_healing'] > first['hero_healing']:
            first = player
    return first
