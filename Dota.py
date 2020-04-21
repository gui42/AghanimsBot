import requests
import json
import ranktier


class Match:
    def __init__(self, match_id, all_heroes=None):
        self.match_id = match_id
        self.__all_heroes = all_heroes if all_heroes else Request.all_heroes()
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
    def request_match(match_id: str, key=None):
        match_id = str(match_id)
        if match_id.isdecimal():
            if key:
                return Request.match(match_id, key)
            else:
                return Request.match(match_id)
        else:
            raise NameError("Match ID has to decimal")


class Player:
    def __init__(self, account_id, all_heroes=None):
        self.__account_id = account_id

        # requests:
        self.all_heroes = all_heroes if all_heroes else Request.all_heroes()
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
    def most_played_heroes(account_id, all_heroes=None):
        most_played = Player.request_heroes(account_id)
        if not all_heroes:
            all_heroes = Request.all_heroes()
        for x in range(0, len(most_played)):
            most_played[x] = Player.add_hero_info(most_played[x], all_heroes=all_heroes)
        return most_played

    @staticmethod
    def add_hero_info(this_hero, all_heroes=None):
        if not all_heroes:
            all_heroes = Request.all_heroes()
        for hero in all_heroes:
            if hero['id'] == int(this_hero['hero_id']):
                this_hero['hero_info'] = hero
        return this_hero

    @staticmethod
    def request_recent_matches(account_id: str, key=None):
        account_id = str(account_id)
        if account_id.isdecimal():
            if key:
                return Request.recent_matches(account_id, key)
            else:
                return Request.recent_matches(account_id)
        else:
            raise NameError('account_id has to be decimal')

    @staticmethod
    def request_heroes(account_id: str, key=None):
        account_id = str(account_id)
        if account_id.isdecimal():
            if key:
                return Request.player_heroes(account_id, key)
            else:
                return Request.player_heroes(account_id)
        else:
            raise NameError("account_id has to be decimal")

    @staticmethod
    def request_player(account_id: str, key=None):
        account_id = str(account_id)
        if account_id.isdecimal():
            if key:
                return Request.player(account_id, key)
            else:
                return Request.player(account_id)
        else:
            raise NameError("account_id has to be decimal")

    @staticmethod
    def request_win_lose(account_id: str, key=None):
        account_id = str(account_id)
        if account_id.isdecimal():
            if key:
                return Request.player_win_lose(account_id, key)
            else:
                return Request.player_win_lose(account_id)
        else:
            raise NameError("account_id has to be decimal")


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


class Request:
    @staticmethod
    def all_heroes(key=None):
        link = "https://api.opendota.com/api/heroes"
        if key:
            link = link+f"?api_key={key}"
        return Request.__request(link)

    @staticmethod
    def match(match_id, key=None):
        link = f"https://api.opendota.com/api/matches/{match_id}"
        if key:
            link = link+f"?api_key={key}"
        return Request.__request(link)

    @staticmethod
    def player_win_lose(account_id, key=None):
        link = f"https://api.opendota.com/api/players/{account_id}/wl"
        if key:
            link = link+f"?api_key={key}"
        return Request.__request(link)

    @staticmethod
    def recent_matches(account_id, key=None):
        link = f"https://api.opendota.com/api/players/{account_id}/recentMatches"
        if key:
            link = link+f"?api_key={key}"
        return Request.__request(link)

    @staticmethod
    def player(account_id, key=None):
        link = f"https://api.opendota.com/api/players/{account_id}"
        if key:
            link = link + f"?api_key={key}"
        return Request.__request(link)

    @staticmethod
    def player_heroes(account_id, key=None):
        link = f"https://api.opendota.com/api/players/{account_id}/heroes"
        if key:
            link = link + f"?api_key={key}"
        return Request.__request(link)

    @staticmethod
    def __request(link):
        this_request = requests.get(link)
        if this_request.status_code == 200:
            if this_request:
                this_request = json.loads(this_request.text)
                return this_request
            else:
                raise ValueError("Null", link)
        else:
            raise ValueError("Bad Request ", link)
