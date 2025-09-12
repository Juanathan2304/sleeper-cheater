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

def get_players_from_api():
    url = f"https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        with open("players.json", "w") as f:
            json.dump(data, f, indent=2)
            f.close()
        del data
        return data
    else:
        print(f"Error: {response.status_code}")

def get_players_from_file():
    with open("players.json", "r") as f:
        data = json.load(f)
        f.close()
        return data

def set_player_last_run():
    with open("last-run.txt","w") as f:
        f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        f.close()

def get_days_since_player_grab():
    with open("last-run.txt", "r") as f:
        last_run = f.read()
        datetime_object = datetime.strptime(last_run, '%Y-%m-%d %H:%M:%S')
        date_difference = datetime.today() - datetime_object
        return date_difference.days
    
def write_ai_response_to_file(response):
    with open("response.txt", "w") as f:
        f.write(response)
        f.close()
    
def ping_ai(prompt):
    api_key = os.getenv("AI_API_KEY")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" 

    payload = {
        "contents" : [
            {
                "parts":[
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

        # 5. Parse and print the response
        data = response.json()
        if data.get("candidates"):
            return (data["candidates"][0]["content"]["parts"][0]["text"])
        else:
            return ("No candidates found in the response.")

    except requests.exceptions.RequestException as e:
        return (f"An error occurred: {e}")

if __name__ == "__main__":

    print("Welcome to the Fantasy Football AI Assistant!")
    while (True):
        print("1. Get Players\n2. Get Roster\n3. Get AI Advice\n4. Exit")
        selection = input("Please select an option (1-4): ")
        print(selection)
        if (selection == "4"):
            break

    if get_days_since_player_grab() > 1:
        refresh = input("It's been more than a day since player data was last grabbed. Press R to refresh player data, or any other key to continue with existing data: ")
        if refresh.lower() == "r":
            get_players_from_api()
            set_player_last_run()
            print("Player data refreshed.")
        else:
            print("Continuing with existing player data.")

    rosters = get_rosters()
    for roster in rosters:
        if roster["owner_id"] == os.getenv("USER_ID"):
            user_roster = roster
            break
    
    all_players = get_players_from_file()

    roster_full = []
    for player in all_players.keys():
        if player in user_roster["players"]:
            roster_full.append(all_players[player])
    write_ai_response_to_file(ping_ai("With the provided player data, give me step by step instructions to win my fantasy football league this year. Be very specific and detailed.\n\nMy Roster:\n" + json.dumps(roster_full)))
