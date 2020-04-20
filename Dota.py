import requests
import json
import ranktier


class Match:
    def __init__(self, match_id, all_heroes=None):
        self.match_id = match_id
        self.__all_heroes = all_heroes if all_heroes else self.request_all_heroes()
        self.__data = self.request_match(match_id)
        self.__players = self.match_players_with_hero_info()

    def get_player(self, account_id):
        for player in self.players:
            if player['account_id']:
                if player['account_id'] == int(account_id):
                    return player

    def match_players_with_hero_info(self):
        raw_players = self.raw_players
        for player in raw_players:
            for hero in self.__all_heroes:
                if player['hero_id'] == hero['id']:
                    player['hero_info'] = hero
        return raw_players

    # properties
    @property
    def first_blood_claimed(self):
        for player in self.players:
            if player['firstblood_claimed']:
                return player

    @property
    def OpenDota(self):
        return f"https://www.opendota.com/matches/{self.match_id}"

    @property
    def radiant_players(self):
        radiant = []
        for player in self.players:
            if player['isRadiant']:
                radiant.append(player)
        return radiant

    @property
    def dire_players(self):
        dire = []
        for player in self.players:
            if not player['isRadiant']:
                dire.append(player)
        return dire

    @property
    def players(self):
        return self.__players

    @property
    def dire_score(self):
        return self.__data['dire_score']

    @property
    def radiant_score(self):
        return self.__data['radiant_score']

    @property
    def picks_bans(self):
        return self.__data['picks_bans']

    @property
    def first_blood_time(self):
        return self.__data['first_blood_time']

    @property
    def raw_players(self):
        return self.__data['players']

    @property
    def game_mode(self):
        return self.__data['game_mode']

    @property
    def duration(self):
        return self.__data['duration']

    @property
    def radiant_win(self):
        return self.__data['radiant_win']

    # static methods
    @staticmethod
    def request_all_heroes():
        all_heroes = requests.get("https://api.opendota.com/api/heroes")
        if all_heroes.status_code == 200:
            all_heroes = json.loads(all_heroes.text)
            return all_heroes
        else:
            raise ValueError(all_heroes.status_code)

    @staticmethod
    def request_match(match_id):
        data = requests.get(f"https://api.opendota.com/api/matches/{match_id}")
        if data.status_code == 200:
            data = json.loads(data.text)
            return data
        else:
            raise ValueError(data.status_code)


class Player:
    def __init__(self, account_id, all_heroes=None):
        self.__account_id = account_id

        # requests:
        self.all_heroes = all_heroes if all_heroes else Match.request_all_heroes()
        self.__data = self.request_player(account_id)
        self.win_lose = self.request_win_lose(account_id)

        self.total_games = self.win_lose['win']+self.win_lose['lose']
        self.win_rate = (self.win_lose['win']/self.total_games)
        self.OpenDota = f"https://www.opendota.com/players/{account_id}"

    # properties
    @property
    def wins(self):
        return self.win_lose['win']

    @property
    def last_games(self):
        return self.request_recent_matches(self.account_id)

    @property
    def last_game_id(self):
        match_id = self.request_recent_matches(self.account_id)
        return match_id[0]['match_id']

    @property
    def account_id(self):
        return self.__account_id

    @property
    def rank_tier_human(self):
        return ranktier.Rank(self.rank_tier)

    @property
    def rank_tier(self):
        return self.__data['rank_tier']

    @property
    def persona_name(self):
        return self.__data['profile']['personaname']

    @property
    def plus(self):
        return self.__data['profile']['plus']

    # static methods
    @staticmethod
    def request_recent_matches(account_id):
        recent_matches = requests.get(f"https://api.opendota.com/api/players/{account_id}/recentMatches")
        if recent_matches.status_code == 200:
            recent_matches = json.loads(recent_matches.text)
            return recent_matches
        else:
            raise ValueError(f"{recent_matches.status_code} in recente_matches")

    @staticmethod
    def most_played_heroes(account_id, all_heroes=None):
        most_played = Player.request_heroes(account_id)
        if not all_heroes:
            all_heroes = Match.request_all_heroes()
        for x in range(0, len(most_played)):
            most_played[x] = Player.add_hero_info(most_played[x], all_heroes=all_heroes)
        return most_played

    @staticmethod
    def add_hero_info(this_hero, all_heroes=None):
        if not all_heroes:
            all_heroes = Match.request_all_heroes()
        for hero in all_heroes:
            if hero['id'] == int(this_hero['hero_id']):
                this_hero['hero_info'] = hero
        return this_hero

    @staticmethod
    def request_heroes(account_id):
        heroes = requests.get(f"https://api.opendota.com/api/players/{account_id}/heroes")
        if heroes.status_code == 200:
            heroes = json.loads(heroes.text)
            return heroes
        else:
            raise ValueError(heroes.status_code)

    @staticmethod
    def request_player(account_id):
        player = requests.get(f"https://api.opendota.com/api/players/{account_id}")
        if player.status_code == 200:
            player = json.loads(player.text)
            return player
        else:
            raise ValueError(player.status_code)

    @staticmethod
    def request_win_lose(account_id):
        win_lose = requests.get(f"https://api.opendota.com/api/players/{account_id}/wl")
        if win_lose.status_code == 200:
            win_lose = json.loads(win_lose.text)
            return win_lose
        else:
            raise ValueError(win_lose.status_code)


class Hero:

    def __init__(self, hero):
        self.__data = hero

    # properties
    @property
    def id(self):
        return self.__data['id']

    @property
    def legs(self):
        return self.__data['legs']

    @property
    def localized_name(self):
        return self.__data['localized_name']

    @property
    def name(self):
        return self.__data['name']

    @property
    def roles(self):
        return self.__data['roles']

    @property
    def attack_type(self):
        return self.__data['attack_type']

    @property
    def primary_attr(self):
        return self.__data['primary_attr']

    # static methods
    @staticmethod
    def add_hero_info(to_be_addedd: dict, all_heroes ):
        for hero in all_heroes:
            if to_be_addedd['hero_id'] == hero['id']:
                to_be_addedd['hero_info'] = hero
        return to_be_addedd

    @staticmethod
    def match_up_with_hero_info(hero_name: str, all_heroes=None):
        hero = Hero.get_hero_by_name(hero_name, all_heroes)
        match_up = Hero.request_match_up(hero['id'])
        for match in match_up:
            match = Hero.add_hero_info(match, all_heroes)
        return match_up

    @staticmethod
    def get_hero_by_name(hero_name: str, all_heroes=None):
        hero_name = hero_name.replace(' ', '').lower()

        if not all_heroes:
            all_heroes = Match.request_all_heroes()

        for hero in all_heroes:
            if hero_name == str(hero['localized_name']).replace(' ', '').lower():
                return hero
        return NameError(f"Hero {hero_name} not found")

    @staticmethod
    def request_match_up(hero_id):
        match_ups = requests.get(f'https://api.opendota.com/api/heroes/{hero_id}/matchups')
        if match_ups.status_code == 200:
            match_ups = json.loads(match_ups.text)
            return match_ups
        else:
            raise ValueError(match_ups.status_code)
