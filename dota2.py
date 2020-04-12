import requests
import json

# I've add the parameter all_heroes in all functions that needs it
# as it's a request that won't change much, I don't think I need to ask for it again every time
# that is needed, so its a simple change that will result in a faster response time for the bot and
# less requests to OpenDota, so a win/win situation


class Dota:

    def __init__(self, match_id, all_heroes=None):
        self.__data = request_data(match_id)
        self.match_id = match_id

        if not all_heroes:
            self.heroes_raw = self.request_all_heroes()
        else:
            self.heroes_raw = all_heroes

        self.info_players = self.gather_info()
        self.radiant_players, self.dire_players = self.teams()
        self.radiant_score = self.__data['radiant_score']
        self.dire_score = self.__data['dire_score']
        self.OpenDota = f"https://www.opendota.com/matches/{match_id}"

    @staticmethod
    def request_all_heroes():
        # requesting for all the hero data, I couldnt find a way to ask for a specific hero
        link = "https://api.opendota.com/api/heroes"
        r = requests.get(link)
        # checks if request is 200 ok
        if r.status_code == 200:
            heroes_raw = json.loads(r.text)
            return heroes_raw
        else:
            raise ValueError("Bad request in all_heroes")

    @staticmethod
    def request_match_up(hero_id):
        link = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
        all_match_up = requests.get(link)
        if all_match_up.status_code == 200:
            all_match_up = json.loads(all_match_up.text)
            return all_match_up
        else:
            raise ValueError("Bad request in match_ups")

    @staticmethod
    def match_up(hero_id, all_heroes=None):
        if not all_heroes:
            all_heroes = Dota.request_all_heroes()
        if str(hero_id).isdecimal():
            match_ups = Dota.request_match_up(hero_id)
            this_hero = Dota.hero_info(hero_id, all_heroes)
        else:
            this_hero = Dota.match_hero_per_name(hero_id, all_heroes)
            match_ups = Dota.request_match_up(this_hero['id'])

        relevant_match_ups = []
        # gets heroes with at least 25 games and that this_hero has lost more than hald of the time
        for hero in match_ups:
            if hero['games_played'] > 25 and hero['wins'] < (hero['games_played']/2):
                # just calculate the odds, makes it a percentage and turns that into a string, u know, the basic
                hero['odds'] = f"{((1 - (hero['wins']/hero['games_played']))*100):02.0f}"
                relevant_match_ups.append(hero)

        for matchup in relevant_match_ups:
            hero = Dota.hero_info(matchup['hero_id'], all_heroes)
            matchup['hero'] = hero['localized_name']
            matchup['attack_type'] = hero['attack_type']
            matchup['roles'] = hero['roles']
            matchup['primary_attr'] = hero['primary_attr']

        scores = []
        ranked = []
        for matchup in relevant_match_ups:
            scores.append(matchup['odds'])

        # get the odds of each hero, orders and reverses it
        scores = sorted(scores, reverse=True)
        for score in scores:
            for match_up in relevant_match_ups:
                if score == match_up['odds']:
                    ranked.append(match_up)
                    relevant_match_ups.pop(relevant_match_ups.index(match_up))
        
        return this_hero, ranked

    @staticmethod
    def match_hero_per_name(hero, all_heroes):
        # I'm using this regular expression to search for a hero name in the input
        this_hero = None
        for heroes in all_heroes:
            # so it's easier to get a match:
            if heroes['localized_name'].lower().replace(' ', '') == hero.lower().replace(' ', ''):
                this_hero = heroes
                return this_hero
        return None

    @staticmethod
    def best_heroes(steam_id, all_heroes=None):
        if not all_heroes:
            all_heroes = Dota.request_all_heroes()
        all_best_heroes = Dota.request_player_heroes(steam_id)
        for best in all_best_heroes:
            for hero in all_heroes:
                if hero['id'] == int(best['hero_id']):
                    best['localized_name'] = hero['localized_name']
                    best['primary_attr'] = hero['primary_attr']
                    best['roles'] = hero['roles']
                    best['attack_type'] = hero['attack_type']
        return all_best_heroes

    @staticmethod
    def hero_info(hero_id, all_heroes):
        for hero in all_heroes:
            if hero_id == hero["id"]:
                this_hero = hero
                return this_hero

    @property
    def heroes(self):
        heroes = []
        for hero in self.__data['picks_bans']:
            if hero['is_pick']:
                heroes.append(hero)
        return heroes

    def match_hero(self, player):
        for hero in self.heroes_raw:
            if player['hero_id'] == hero['id']:
                return hero

    def info(self, player):
        info = {}
        hero_info = self.match_hero(player)
        info['hero'] = hero_info['localized_name']
        info['id'] = player['hero_id']
        info['xp_per_min'] = player['xp_per_min']
        info['gold_per_min'] = player['gold_per_min']
        info['total_gold'] = player['total_gold']
        info['deaths'] = player['deaths']
        info['assists'] = player['assists']
        info['kills'] = player['kills']
        info['last_hits'] = player['last_hits']
        info['denies'] = player['denies']
        info['level'] = player['level']
        info['team'] = 'radiant' if player['isRadiant'] else 'dire'
        info['hero_damage'] = player['hero_damage']
        info['tower_damage'] = player['tower_damage']
        info['firstblood_claimed'] = player['firstblood_claimed']
        return info

    def gather_info(self):
        players = self.players
        info_players = map(self.info, players)
        info_players = list(info_players)
        return info_players

    def teams(self):
        radiant = []
        dire = []
        for player in self.info_players:
            if player['team'] == 'radiant':
                radiant.append(player)
            else:
                dire.append(player)
        return radiant, dire

    @staticmethod
    def request_player_heroes(account_id):
        player_heroes = requests.get(f"https://api.opendota.com/api/players/{account_id}/heroes")
        if player_heroes.status_code == 200:
            player_heroes = json.loads(player_heroes.text)
            return player_heroes
        else:
            raise ValueError("Bad request in request_player_heroes")

    @staticmethod
    def request_player_recent_matches(steam32):
        link = f"https://api.opendota.com/api/players/{steam32}/recentMatches"
        last_games = requests.get(link)
        if last_games.status_code == 200:
            last_games = json.loads(last_games.text)
            return last_games
        else:
            raise ValueError("Bad recent matches request")

    @staticmethod
    def last_game(steam32, all_heroes=None):

        if not steam32.isdecimal():
            raise ValueError("Invalid Steam32 ID")
        last_games = Dota.request_player_recent_matches(steam32)
        if not last_games:
            raise NameError('Maybe profile set to private')

        last_match = last_games[0]
        last_match_id = last_match['match_id']
        game = Dota(last_match_id, all_heroes)
        this_player = {}
        for player in game.info_players:
            if player['id'] == last_match['hero_id']:
                this_player['hero_id'] = player['id']
                this_player['hero'] = player['hero']
                this_player['kills'] = player['kills']
                this_player['assists'] = player['assists']
                this_player['deaths'] = player['deaths']
                this_player['gold_per_min'] = player['gold_per_min']
                this_player['xp_per_min'] = player['xp_per_min']
                this_player['total_gold'] = player['total_gold']
                this_player['level'] = player['level']
                this_player['last_hits'] = player['last_hits']
                this_player['denies'] = player['denies']
                this_player['tower_damage'] = player['tower_damage']
                this_player['hero_damage'] = player['hero_damage']
                this_player['team'] = player['team']
                this_player['party_size'] = last_match['party_size']
        return this_player, game

    @property
    def players(self):
        return self.__data['players']

    @property
    def duration(self):
        s = self.__data['duration']
        s = int(s)
        h, m = 0, 0
        while s > 3600:
            m -= 3600
            h += 1
        while s > 60:
            m += 1
            s -= 60

        return [h, m, s]

    @property
    def winner(self):
        if self.__data['radiant_win']:
            return 'radiant'
        else:
            return 'dire'

    @property
    def first_blood(self):
        first_blood_info = []
        sec = int(self.__data['first_blood_time'])
        min = 0
        while sec > 60:
            sec -= 60
            min += 1
        time = f'{min:02d}:{sec:02d}'
        first_blood_info.append(time)
        for player in self.info_players:
            if player['firstblood_claimed']:
                first_blood_info.append(player)
        
        return first_blood_info

    @staticmethod
    def request_player(account_id):
        player = requests.get(f"https://api.opendota.com/api/players/{account_id}")
        if player.status_code == 200:
            player = json.loads(player.text)
            return player
        else:
            raise ValueError("Bad request in request_player")

    @staticmethod
    def request_win_loss(account_id):
        wl = requests.get(f"https://api.opendota.com/api/players/{account_id}/wl")
        if wl.status_code == 200:
            wl = json.loads(wl.text)
            return wl
        else:
            raise ValueError("Bad request at request_win_loss")

    @property
    def highest_nw(self):
        first = {"total_gold": '0'}
        for player in self.info_players:
            if int(player['total_gold']) > int(first['total_gold']):
                first = player
        return first

    @property
    def highest_amount_of_kills(self):
        first = {'kills': '0'}
        for player in self.info_players:
            if int(player['kills']) > int(first['kills']):
                first = player
        return first

    @property
    def highest_damage(self):
        first = {'hero_damage': '0'}
        for player in self.info_players:
            if int(player['hero_damage'] > int(first['hero_damage'])):
                first = player
        return first

    @property
    def highest_tower_damage(self):
        first = {'tower_damage': '0'}
        for player in self.info_players:
            if int(player['tower_damage'] > int(first['tower_damage'])):
                first = player
        return first


def request_data(game_id):
    # requesting parse
    game_id = str(game_id)

    if len(game_id) != 10 or not game_id.isdecimal():
        raise ValueError("invalid id in request_match, len or not decimal")

    requests.post(f" https://api.opendota.com/api/request/{game_id} ", data={'match': id})

    # requesting for match details
    link = f"https://api.opendota.com/api/matches/{game_id}"
    r = requests.get(link)

    # checking if the request worked (200 ok)
    if r.status_code == 200:
        data = dict(json.loads(r.text))
        return data
    else:
        print("error on status code", r.status_code)
        raise ValueError('Bad Request in request_data')
