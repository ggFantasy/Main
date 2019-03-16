import requests
import json

from datetime import datetime

from flask_restful import Resource, reqparse, fields, marshal
from ggfantasy.models.players import Players
from ggfantasy.models.matches import Matches
from ggfantasy.models.teams import Teams

import json

parser = reqparse.RequestParser()
parser.add_argument("Sid", dest="sid", type=str, required=True)

players_fields = {
    "leagueSid": fields.String,
    "slug": fields.String,
    "friendlyName": fields.String,
    "roleSlug": fields.String,
    "primaryTeam": fields.String
}

teams_fields = {
    "leagueSid": fields.String,
    "teamSid": fields.String,
    "slug": fields.String,
    "friendlyName": fields.String,
    "acronym": fields.String,
    "players": fields.Nested(players_fields),
    "dateCreated": fields.String,
    "dateUpdated": fields.String
}

resource_fields = {
    "matchSid": fields.String,
    "tournamentSid": fields.String,
    "bracketSid": fields.String,
    "primaryTeam": fields.Nested(teams_fields),
    "secondaryTeam": fields.Nested(teams_fields),
    "scheduledTime": fields.String,
    "state": fields.String,
    "dateCreated": fields.String,
    "dateUpdated": fields.String
}


class MatchDetails(Resource):
    def get(self):
        args = parser.parse_args()
        match = Matches.query.filter_by(matchSid=args['sid']).first()
        response_obj = self._convert_to_dict(match)

        primary_team = self._fetch_team(match.primaryTeam)
        secondary_team = self._fetch_team(match.secondaryTeam)

        primary_players = self._fetch_players(primary_team.leagueSid)
        secondary_players = self._fetch_players(secondary_team.leagueSid)

        primary_team.players = primary_players
        secondary_team.players = secondary_players

        response_obj["primaryTeam"] = primary_team
        response_obj["secondaryTeam"] = secondary_team

        return marshal(response_obj, resource_fields)

    def _convert_to_dict(self, match):
        return {key: getattr(match, key) for key in match.KEYS}

    def _fetch_players(self, team_id):
        return Players.query.filter_by(primaryTeam=team_id).all()

    def _fetch_team(self, acronym):
        return Teams.query.filter_by(acronym=acronym).first()