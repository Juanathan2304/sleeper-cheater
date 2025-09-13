import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_rosters():
    league_id = os.getenv("LEAGUE_ID")

    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"  
    response = requests.get(url)

    # Check the status code
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        return (data)
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    rosters = get_rosters()
    print(rosters)