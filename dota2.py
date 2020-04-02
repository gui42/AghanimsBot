import requests
import json
import random
import re
import datetime


class Dota:
    def __init__(self, id):
        self.__data = request_data(id)
        self.id = id
        self.heroes_raw = self.request_heroes()
        self.info_players = self.gather_info()
        self.radiant, self.dire = self.teams()
        self.radiant_score = self.__data['radiant_score']
        self.dire_score = self.__data['dire_score']
        self.dotabuff = f"https://www.dotabuff.com/matches/{id}"

    @staticmethod
    def get_match_id_from_user_input(id):
        standard = "[0-9]{10}"
        match_id = re.search(standard, id)
        if not match_id:
            raise ValueError("Invalid match ID")
        else:
            return match_id

    @staticmethod
    def request_heroes():
        link = "https://api.opendota.com/api/heroes"
        r = requests.get(link)
        heroes_raw = json.loads(r.text)
        return heroes_raw

    @staticmethod
    def get_matchup(hero_id):
        hero = Dota.get_hero(hero_id)
        if not hero:
            raise ValueError("not possible to get hero")
        print(hero_id)
        link = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
        r = requests.get(link)
        matchup_all = json.loads(r.text)
        heroes = Dota.request_heroes()
        matchup = []
        for match in range(0, 5):
            for hero in range(0, len(heroes) - 1):
                if matchup_all[match]['hero_id'] == heroes[hero]['id']:
                    this = matchup_all[match]
                    that = heroes[hero]
                    odds = int(this['wins']) / int(this['games_played'])
                    odds = f"{(odds * 100):02.0f}%"
                    matchup.append({'hero': that['localized_name'], 'odds': odds})
                if heroes[hero]['id'] == hero_id:
                    this_hero = heroes[hero]
        return matchup

    @staticmethod
    def get_hero(hero_id):
        hero_id = str(hero_id)
        standard = "[0-9]{1,3}"
        id = re.search(standard, hero_id)
        if id:
            id = id.string
            all_heroes = Dota.request_heroes()
            for hero in all_heroes:
                if id == str(hero['id']):
                    return [hero]
        else:
            standard = "[a-z,A-Z]{2,10}\s{0,1}[a-z,A-Z]{0,20}"
            id = re.search(standard, hero_id)
            if id:
                id = id.string
                all_heroes = Dota.request_heroes()
                for hero in all_heroes:
                    if id.lower() == hero['localized_name'].lower():
                        return hero

    @staticmethod
    def print_machup(hero_id):
        hero_id = str(hero_id)
        this = Dota.get_hero(hero_id)
        matchup = Dota.get_matchup(hero_id)
        lines = []
        first_line = f"{this} match ups:\n"
        lines.append(first_line)
        for opponent in matchup:
            line = f"{opponent['hero']}  {opponent['odds']}\n"
            lines.append(line)

        matchup = f"{lines[0]}{lines[1]}{lines[2]}{lines[3]}{lines[4]}"
        return  matchup

    def get_heroes(self):
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
        info['level'] = player['level']
        info['team'] = 'radiant' if player['isRadiant'] else 'dire'
        #info['lane_efc'] = player['lane_efficiency_pct']  if the match inst parced, this breaks eveything
        info['hero_damage'] = player['hero_damage']
        info['tower_damage'] = player['tower_damage']
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

        if h > 0:
            return f'{h:02d}:{m:02d}:{s:02d}'
        else:
            return f'{m:02d}:{s:02d}'

    @property
    def winner(self):
        if self.__data['radiant_win']:
            return 'radiant'
        else:
            return 'dire'

    @property
    def first_blood(self):
        sec =int(self.__data['first_blood_time'])
        min = 0
        while sec > 60:
            sec -= 60
            min += 1
        return f'First blood time: {min}:{sec}'

    @property
    def highest_nw(self):
        first = {"total_gold": '0'}
        for player in self.info_players:
            if int(player['total_gold']) > int(first['total_gold']):
                first = player
        return f"{first['hero']} had a NW of {first['total_gold']}"

    @property
    def highest_amount_of_kills(self):
        first = {'kills': '0'}
        for player in self.info_players:
            if int(player['kills']) > int(first['kills']):
                first = player
        return f"{first['hero']} got {first['kills']} kills!"

    @property
    def highest_damage(self):
        first = {'hero_damage': '0'}
        for player in self.info_players:
            if int(player['hero_damage'] > int(first['hero_damage'])):
                first = player
        return f"{first['hero']} dealt {first['hero_damage']} total hero damage!"

    @property
    def highest_tower_damage(self):
        first = {'tower_damage': '0'}
        for player in self.info_players:
            if int(player['tower_damage'] > int(first['tower_damage'])):
                first = player
        return f"{first['hero']} dealt {first['tower_damage']} damage to towers!"

    def high_scores(self, opt= None):
        options = [self.highest_amount_of_kills, self.highest_nw, self.highest_damage, self.first_blood]
        if opt:
            return options[opt]
        else:
            rand_num = random.randint(0, 3)
            return options[rand_num]

    @property
    def print_resume(self):
        line = f"{'radiant'.upper() if self.winner == 'radiant'else 'radiant'.title()} {self.radiant_score} " \
                f": {self.dire_score} {'dire'.upper() if self.winner == 'dire' else 'dire'.title()}\n" \
                f"Duration:\t{self.duration}\n" \
                f"{self.high_scores()}\n"\
                f"{self.dotabuff}"
        return line


def request_data(id):
    requests.post(f" https://api.opendota.com/api/request/{id} ", data={'match': id})
    link = f"https://api.opendota.com/api/matches/{id}"
    r = requests.get(link)
    if r.status_code == 200:
        data = dict(json.loads(r.text))
        return data
    else:
        raise ValueError('Bad Request')
