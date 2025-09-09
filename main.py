import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_rosters():
    league_id = os.getenv("LEAGUE_ID")

    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"  # Example API endpoint
    response = requests.get(url)

    # Check the status code
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        print(data)
    else:
        print(f"Error: {response.status_code}")

def get_players():
    url = f"https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        with open("players.json", "w") as f:
            json.dump(data, f, indent=2)
            f.close()
        del data
        print(data)
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    # get_rosters()

    with open("last-run.txt","w") as f:
        f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()

    with open("last-run.txt", "r") as f:
        last_run = f.read()
        datetime_object = datetime.strptime(last_run, '%Y-%m-%d %H:%M:%S')
        date_difference = datetime.today() - datetime_object
        print(date_difference.days)
