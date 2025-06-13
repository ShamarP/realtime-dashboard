import json
import pandas as pd

def get_players(json_path):
    with open(json_path) as f:
        mlb_data = json.load(f)


    players = []
    
    if 'gameData' in mlb_data and 'players' in mlb_data['gameData']:
        players_dict = mlb_data['gameData']['players']

        for player_key, player_info in players_dict.items():
            players.append(player_info)
    
    df = pd.DataFrame(players)
    return df
