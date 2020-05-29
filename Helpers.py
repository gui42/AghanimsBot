def open_token():
    with open('token.txt') as f:
        lines = f.read().splitlines()
        print("[OK]\tToken")
        return lines[-1]


def open_OpenDota_key():
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
