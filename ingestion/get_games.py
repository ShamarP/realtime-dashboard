import requests
import datetime
import pandas as pd
import json

def get_todays_game_pks(date_str=None):
    """
    Fetch the list of gamePk values for all MLB games on a given date.
    If date_str is None, defaults to today's date in YYYY-MM-DD format.
    """
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    game_pks = []
    # The JSON structure: data['dates'] is a list; usually it has one item (for that date).
    for date_block in data.get("dates", []):
        for game in date_block.get("games", []):
            game_pk = game.get("gamePk")
            if game_pk is not None:
                game_pks.append(game_pk)

    return game_pks

todays_games = get_todays_game_pks()
print(f"Today's games (gamePk values): {todays_games}")

url = "https://statsapi.mlb.com/api/v1.1/game/777704/feed/live"
resp = requests.get(url)
data = resp.json()
with open("test.json", "w") as f:
    json.dump(data, f, indent=2)