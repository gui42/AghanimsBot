import requests
import json
import random
import re


class Dota:
    def __init__(self, id):
        self.__data = request_data(id)
        self.id = id
        self.heroes_raw = self.request_all_heroes()
        self.info_players = self.gather_info()
        self.radiant, self.dire = self.teams()
        self.radiant_score = self.__data['radiant_score']
        self.dire_score = self.__data['dire_score']
        self.OpenDota = f"https://www.opendota.com/matches/{id}"

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
    def request_match_up(id):
        link = f"https://api.opendota.com/api/heroes/{id}/matchups"
        all_match_up = requests.get(link)
        if all_match_up.status_code == 200:
            all_match_up = json.loads(all_match_up.text)
            return all_match_up
        else:
            raise ValueError("Bad request in match_ups")

    @staticmethod
    def match_up_counters(hero_id):
        all_heroes = Dota.request_all_heroes()
        if str(hero_id).isdecimal():
            match_ups = Dota.request_match_up(hero_id)
            this_hero = Dota.hero_info(hero_id, all_heroes)
        else:
            this_hero = Dota.match_hero_per_name(hero_id, all_heroes)
            match_ups = Dota.request_match_up(this_hero['id'])
        relevant_macth_ups = match_ups[:len(match_ups) - 100]
        for matchup in relevant_macth_ups:
            hero = Dota.hero_info(matchup['hero_id'], all_heroes)
            matchup['hero'] = hero['localized_name']
            matchup['attack_type'] = hero['attack_type']
            matchup['roles'] = hero['roles']
            matchup['primary_attr'] = hero['primary_attr']

        return Dota.print_match_up(this_hero, relevant_macth_ups)

    @staticmethod
    def match_hero_per_name(hero, all_heroes):
        # I'm using this regular expression to search for a hero name
        padrao = "[a-z,A-Z]{2,15}\s{0,1}[a-z,A-Z]{0,15}"
        search = re.search(padrao, hero)
        if search:
            search = search.string
            for heroes in all_heroes:
                # so it's easier to get a match
                if heroes['localized_name'].lower().replace(' ', '') == search.lower().replace(' ', ''):
                    return heroes
        else:
            raise NameError("No search result")

    @staticmethod
    def print_match_up(this_hero, matchup):

        first_line = f"Match ups for {this_hero['localized_name']}\n" \
                     f"{matchup[0]['hero']}: {int(matchup[0]['wins'])/int(matchup[0]['games_played'])*100:02.0f}%\n" \
                     f"{matchup[1]['hero']}: {int(matchup[1]['wins'])/int(matchup[1]['games_played'])*100:02.0f}%\n" \
                     f"{matchup[2]['hero']}: {int(matchup[2]['wins'])/int(matchup[2]['games_played'])*100:02.0f}%\n" \
                     f"{matchup[3]['hero']}: {int(matchup[3]['wins'])/int(matchup[3]['games_played'])*100:02.0f}%\n"\
                     f"{matchup[4]['hero']}: {int(matchup[4]['wins'])/int(matchup[4]['games_played'])*100:02.0f}%\n"
        return first_line

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
        info['level'] = player['level']
        info['team'] = 'radiant' if player['isRadiant'] else 'dire'
        # info['lane_efc'] = player['lane_efficiency_pct']  if the match inst parced, this breaks eveything
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
        sec = int(self.__data['first_blood_time'])
        min = 0
        while sec > 60:
            sec -= 60
            min += 1
        return f'First blood time: {min:02d}:{sec:02d}'

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

    def high_scores(self, all_h=False):
        options = [self.highest_amount_of_kills, self.highest_nw, self.highest_damage, self.first_blood]
        if all_h:
            return options
        else:
            rand_num = random.randint(0, 3)
            return options[rand_num]

    @property
    def print_resume(self):
        line = f"{'radiant'.upper() if self.winner == 'radiant'else 'radiant'.title()} {self.radiant_score} " \
                f": {self.dire_score} {'dire'.upper() if self.winner == 'dire' else 'dire'.title()}\n" \
                f"Duration:\t{self.duration}\n" \
                f"{self.high_scores(True)}\n"\
                f"{self.OpenDota}"
        return line


def request_data(id):
    # requesting parse
    requests.post(f" https://api.opendota.com/api/request/{id} ", data={'match': id})
    # requesting for match details
    link = f"https://api.opendota.com/api/matches/{id}"
    r = requests.get(link)
    # checking if the request worked (200 ok)
    if r.status_code == 200:
        data = dict(json.loads(r.text))
        return data
    else:
        raise ValueError('Bad Request in request_data')