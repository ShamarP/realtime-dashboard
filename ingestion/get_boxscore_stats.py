import json
import pandas as pd

def get_boxscore_player_stats(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    boxscore = data.get('liveData', {}).get('boxscore', {})
    teams = boxscore.get('teams', {})
    
    all_player_stats = []
    
    for team_type in ['away', 'home']:
        if team_type in teams:
            team_data = teams[team_type]
            players = team_data.get('players', {})
            
            team_info = team_data.get('team', {})
            team_id = team_info.get('id')
            team_name = team_info.get('name')
            
            for player_key, player_data in players.items():
                person = player_data.get('person', {})
                player_id = person.get('id')
                player_name = person.get('fullName')
                
                position = player_data.get('position', {})
                jersey_number = player_data.get('jerseyNumber')
                
                stats = player_data.get('stats', {})
                batting_stats = stats.get('batting', {})
                pitching_stats = stats.get('pitching', {})
                fielding_stats = stats.get('fielding', {})
                
                player_record = {
                    'team_type': team_type,
                    'team_id': team_id,
                    'team_name': team_name,
                    
                    'player_id': player_id,
                    'player_name': player_name,
                    'jersey_number': jersey_number,
                    'position_code': position.get('code'),
                    'position_name': position.get('name'),
                    'position_abbreviation': position.get('abbreviation'),
                    
                    **{f'batting_{k}': v for k, v in batting_stats.items()},
                    **{f'pitching_{k}': v for k, v in pitching_stats.items()},
                    **{f'fielding_{k}': v for k, v in fielding_stats.items()}
                }

                all_player_stats.append(player_record)

    combined_df = pd.DataFrame(all_player_stats)
    
    return combined_df

