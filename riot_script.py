import sys
import requests

from datetime import datetime
from secrets import api_key

if __name__ == "__main__":
    base_url = 'https://na1.api.riotgames.com'
    # Loads first argument passed in as the id, used to make GET request
    try:
        id = sys.argv[1]
    except IndexError as e:
        warning = "No summoner id provided. Visit lolking.net and search desired username to get summoner ID"
        sample_execution = "Sample execution of script: python riot_script.py 35514150"
        print("{}\n{}".format(warning, sample_execution))
        exit()

    # Base GET request to API
    response = requests.get('{}/lol/summoner/v3/summoners/{}?api_key={}'.format(base_url, id, api_key))

    data = response.json()
    print("Summoner Fetched - {} || ID - {} || Account ID - {}".format(data['name'], data['id'], data['accountId']))

    account_sid = data['accountId']

    # GET Matches List
    matches_response = requests.get('{}/lol/match/v3/matchlists/by-account/{}?api_key={}'.format(base_url, account_sid, api_key))
    matches = matches_response.json()['matches']

    for match in matches:
        # Timestamp originally given down to millisecond, converting to seconds here
        timestamp = match['timestamp'] / 1000
        # Converts timestamp to human readable string
        date = datetime.fromtimestamp(timestamp)

        print("{} played {} on {}".format(data['name'], match['lane'], date))
