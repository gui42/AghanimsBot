import requests as r
import pandas as pd


def open_token():
    try:
        with open('token.txt') as f:
            lines = f.read().splitlines()
            print("[OK]\tToken")
            return lines[-1]
    except FileNotFoundError:
        print('[FAIL]\tToken')


def OpenDota_key():
    try:
        with open('OpenDotaKey.txt') as f:
            lines = f.read().splitlines()
            return lines[-1]
    except FileNotFoundError:
        return None


def OpenDota_checker():
    try:
        with open('OpenDotaKey.txt'):
            print("[OK]\tOpenDota API key")
    except FileNotFoundError:
        print("[OK]\tFree OpenDota API")


def all_heroes_csv():
    all_heroes = pd.read_csv('Data/all_heroes.csv')
    return all_heroes


def request_and_create_all_heroes():
    all_heroes = r.get("https://api.opendota.com/api/heroes")
    if all_heroes.status_code == 200:
        all_heroes = pd.read_json(all_heroes.text)
        all_heroes.to_csv('Data/all_heroes.csv', index=False)
        print("[OK]\tAll heroes file")
    else:
        print("[FAIL]\tAll heroes file ")
