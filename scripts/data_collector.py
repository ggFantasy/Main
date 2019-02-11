import requests

from datetime import datetime

from ggfantasy.models.matches import Matches
from ggfantasy.models.teams import Teams
from ggfantasy.models.players import Players


class DataCollector:
    """
        Script queries players endpoint and collects player data from response.
        Parses data into format necessary for model objects
        Stores data to DB
    """

    BASE_URL = "https://api.lolesports.com/api{}"
    LEAGUES_ENDPOINT = "/v1/leagues?slug={}"
    PLAYERS_ENDPOINT = "/v1/players?tournament={}&slug={}"
    LCS_LEAGUE = "lcs"


    players = set()

    def _fetch_data(self):
        url = self.BASE_URL.format(self.LEAGUES_ENDPOINT.format(self.LCS_LEAGUE))
        print(url)
        resp = requests.get(url)
        status_code, resp_data = resp.status_code, resp.json()

        print(status_code)
        if status_code < 300:
            return resp_data
        raise ValueError

    def _convert_str_to_datetime(self, str):
        """Converts strings to date time object. String must be YYYY-MM-DD"""
        return datetime.strptime(str, "%Y-%m-%d") if str else None

    def _capture_current_tournaments(self, tournaments):
        now = datetime.now()
        current_tournaments = list()
        for tournament in tournaments:
            start_date = self._convert_str_to_datetime(tournament.get("startDate", None))
            end_date = self._convert_str_to_datetime(tournament.get("endDate", None))

            if end_date and end_date > now:
                current_tournaments.append(tournament)

        return current_tournaments

    def _collect_matches(self, tournaments):
        for tournament in tournaments:
            tournament_sid = tournament.get("id")
            brackets = tournament.get("brackets")
            for bracket_sid, bracket in brackets.items():
                matches = bracket.get("matches")
                for match_sid, match in matches.items():
                    teams = match.get("input")
                    primary_team_sid = teams[0].get("roster")
                    secondary_team_sid = teams[1].get("roster")
                    state = match.get("state")

                    print("state {}".format(state))
                    state_type = 1 if state == "resolved" else 0

                    new_match = Matches(match_sid, tournament_sid, bracket_sid, primary_team_sid, secondary_team_sid, None, state_type, date_created=datetime.utcnow(), date_updated=datetime.utcnow())
                    Matches.session.add(new_match)
                    Matches.session.commit()

    def _collect_teams(self, teams):
        for team in teams:
            league_sid = team.get("id")
            team_sid = team.get("guid")
            slug = team.get("slug")
            friendly_name = team.get("name")
            acronym = team.get("acronym")

            players = team.get("players")
            for player in players:
                self.players.add(player)

            exists = self._entity_exists(Teams, "teamSid", team_sid)
            if not exists:
                new_team = Teams(league_sid, team_sid, slug, friendly_name, acronym, date_created=datetime.utcnow(), date_updated=datetime.utcnow())
                Teams.session.add(new_team)
                Teams.session.commit()

    def _collect_players(self, tournament_sid):
        while self.players:
            player_sid = self.players.pop()
            exists = self._entity_exists(Players, "leagueSid", player_sid)
            if not exists:
                url = self.BASE_URL.format(self.PLAYERS_ENDPOINT.format(tournament_sid, player_sid))
                resp = requests.get(url)
                status_code, resp_data = resp.status_code, resp.json()
                player_data = resp_data.get("players")[0]
                slug = player_data.get("slug")
                friendly_name = player_data.get("name")
                role_slug = player_data.get("roleSlug")

                teams = player_data.get("teams")
                primary_team = teams[0]
                secondary_team = teams[1] if len(teams) > 1 else None
                print(primary_team, secondary_team)
                new_player = Players(player_sid, slug, friendly_name, role_slug, primary_team, secondary_team, date_created=datetime.utcnow(), date_updated=datetime.utcnow())
                Players.session.add(new_player)
                Players.session.commit()

    def _entity_exists(self, obj, filter, id):
        filter_dict = {filter: id}
        result = obj.query.filter_by(**filter_dict).first()
        return result is not None

    def run(self):
        data = self._fetch_data()
        current_tournaments = self._capture_current_tournaments(data["highlanderTournaments"])
        # self._collect_matches(current_tournaments)
        self._collect_teams(data["teams"])
        print(self.players)
        tournament_sid = current_tournaments[0]["id"]
        self._collect_players(tournament_sid)



if __name__ == "__main__":
    dc = DataCollector()
    dc.run()
