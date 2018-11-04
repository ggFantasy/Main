import time
import requests

from datetime import datetime

from util import Util
from ggfantasy.timelord.timelord import TimeLord
from ggfantasy.refinery.refinery import Refinery


class LeagueConfig:
    def __init__(self):
        self.PROD_API = 'https://prod-api.ewp.gg/'
        self.LEAGUES = 'ewp-web-api/v1/leagues'
        self.LEAGUES_SCHEDULES = 'ewp-web-api/v1/schedule?leagues=%5B{}%5D'

    def _get_leagues_url(self):
        return '{}{}'.format(self.PROD_API, self.LEAGUES)

    def _get_schedule_url(self, leagues):
        """
            This version of the function will ask for leagues to plug into url
            Abstracted version should not need this
        :return str:
        """
        return '{}{}'.format(self.PROD_API, self.LEAGUES_SCHEDULES.format(leagues))


class LeagueEnqueuer(LeagueConfig):
    """
        Will fetch upcoming matches in 24 hour period. If there are any,
        it will create a cron job for that match
    """
    def get_leagues(self):
        resp = requests.get(self._get_leagues_url())
        data, status_code = resp.json(), resp.status_code
        if status_code < 400:
            league_ids = list()
            for league in data['leagues']:
                league_ids.append(league['id'])

            return league_ids

    def get_upcoming_matches(self, leagues):
        # Need the time in milliseconds
        start = time.time() * 1000
        end = start + Util.day_to_milliseconds(1)

        upcoming_matches = list()
        for league in leagues:
            resp = requests.get(self._get_schedule_url(league))
            data, status_code = resp.json(), resp.status_code
            if status_code < 400:
                for match in data['schedule']:
                    if match['startTime'] >= start and match['startTime'] <= end:
                        date = datetime.fromtimestamp(match['startTime'] / 1000)
                        print('Upcoming Match: {} vs {} for {} at {}'
                                .format(match['match']['teams']['team1']['name'],
                                    match['match']['teams']['team2']['name'],
                                    match['league']['name'],
                                    date
                                )
                             )
                        date.replace(hour=date.hour - 1)
                        date.replace(minute=date.minute + 30)

                        job_config = {
                            'target': Refinery.get_path(),
                            'date': date
                        }

                        TimeLord(job_config=job_config)
                        upcoming_matches.append(match)
        return upcoming_matches

    def run(self):
        leagues = self.get_leagues()
        self.get_upcoming_matches(leagues)

