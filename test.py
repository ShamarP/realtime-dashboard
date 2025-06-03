import json
import pandas as pd

with open("test.json") as f:
    mlb_data = json.load(f)

pitch_data_list = []

all_plays = mlb_data.get("liveData", {}).get("plays", {}).get("allPlays", [])

for play in all_plays:
    play_events = play.get("playEvents", [])
    pitcher_id = play.get("matchup", {}).get("pitcher", {}).get("id")
    batter_id = play.get("matchup", {}).get("batter", {}).get("id")
    play_id = play.get("playId")
    for event in play_events:
        if "pitchData" in event:
            pitch_data = event["pitchData"].copy()

            # Flatten coordinates if present
            coordinates = pitch_data.pop("coordinates", {})
            breaks = pitch_data.pop("breaks", {})
            pitch_data.update(coordinates)
            pitch_data.update(breaks)

            # Add extra context
            pitch_data["pitcherId"] = pitcher_id
            pitch_data["batterId"] = batter_id
            pitch_data["playId"] = play_id
            pitch_data["eventType"] = event.get("details", {}).get("type", {}).get("description")
            pitch_data["pitchType"] = event.get("details", {}).get("type", {}).get("description")
            pitch_data["callCode"] = event.get("details", {}).get("call", {}).get("code")
            pitch_data["callDesc"] = event.get("details", {}).get("call", {}).get("description")

            pitch_data_list.append(pitch_data)


# Create DataFrame
df = pd.DataFrame(pitch_data_list)
df.to_csv("pitch_data.csv", index=False)

# Display the DataFrame
print(df)