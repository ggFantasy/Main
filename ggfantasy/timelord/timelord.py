import os
import time
import requests
from datetime import datetime
from crontab import CronTab
from util import ROOT_DIR

from pprint import PrettyPrinter



# Cron job setup
cron = CronTab(user=True)

# For now, use endpoint to grab leagues
# But after, it will use the database to check for leagues
base_url = 'https://prod-api.ewp.gg/'
leagues_url = '{}ewp-web-api/v1/leagues'.format(base_url)
schedules_url = '{}ewp-web-api/v1/schedule?leagues=%5B{}%5D'

printer = PrettyPrinter()

def day_to_milliseconds(days):
    return days * 24 * 60 * 60 * 1000

def get_leagues():
    resp = requests.get(leagues_url)
    data, status_code = resp.json(), resp.status_code
    if status_code < 400:
        league_ids = list()
        for league in data['leagues']:
            # Here it should save id, name, and maybe region to db
            league_ids.append(league['id'])

        return league_ids

def get_upcoming_matches(leagues):
    start = time.time() * 1000
    end = start + day_to_milliseconds(7)

    upcoming_matches = list()
    for league in leagues:
        url = schedules_url.format(base_url, league)
        resp = requests.get(url)
        data, status_code = resp.json(), resp.status_code
        if status_code < 400:
            for blob in data['schedule']:
                if blob['startTime'] >= start and blob['startTime'] <= end:
                    date = datetime.fromtimestamp(blob['startTime']/1000)
                    # TODO Turn this into Log statements instead of print
                    print('Upcoming Match: {} vs {} for {} at {}'.format(blob['match']['teams']['team1']['name'],
                                                                         blob['match']['teams']['team2']['name'],
                                                                         blob['league']['name'],
                                                                         date))
                    # Config for new cron job
                    command = '{}/venv/bin/python'.format(ROOT_DIR)
                    job = cron.new(command='{} {}/ggfantasy/refinery/refinery.py'.format(command, ROOT_DIR))

                    # Sets cron job to kick off 30 minutes before game start
                    job.day.on(date.day)
                    job.hour.on(date.hour - 1)
                    job.minute.on(30)
                    for task in cron:
                        # TODO Turn this into Log statements instead of print
                        print(task)
                    upcoming_matches.append(blob)
    return upcoming_matches

def push_to_queue(matches):
    start_times = list()
    for match in matches:
        start_times.append(match['startTime'])
    # Replace this to push to queue
    print(start_times)


if __name__ == "__main__":
    print("Initiating Timelord...")
    leagues = get_leagues()
    matches = get_upcoming_matches(leagues)
    push_to_queue(matches)