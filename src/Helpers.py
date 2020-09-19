import requests as r
import pandas as pd
import json


def init_bot():
    try:
        config = open('./Data/config.txt', 'r')
        config = eval(config.read())
        print('[OK]\tConfig File')
        return config

    except FileNotFoundError:
        print("Config file not found.")
        bot_token = input("Telegram bot token: ")
        if input("Free OpenDota? (Y/n)") in ('N', 'n'):
            openDota_token = input("OpenDota Token: ")
        else:
            openDota_token = 'free'
        config = {'token': bot_token, 'openDota': openDota_token}
        file = open('./Data/config.txt', 'w')
        file.write(json.dumps(config))
        file.close()
        print('[OK]\tConfig file created')
        return config


def openDotaKey():
    config =eval(open('/Data/config.txt', 'r').read())
    if config['openDota'] == 'free':
        return None
    else: 
        return config['openDota']


def all_heroes_csv():
    all_heroes = pd.read_csv('./Data/all_heroes.csv')
    return all_heroes


def request_and_create_all_heroes():
    all_heroes = r.get("https://api.opendota.com/api/heroes", timeout=30)
    if all_heroes.status_code == 200:
        all_heroes = pd.read_json(all_heroes.text)
        all_heroes.to_csv('./Data/all_heroes.csv', index=False)
        print("[OK]\tAll heroes file")
    else:
        print("[FAIL]\tAll heroes file ")
