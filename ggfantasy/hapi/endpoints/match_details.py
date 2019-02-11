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

teams_fields = {
    "leagueSid": fields.String,
    "teamSid": fields.String,
    "slug": fields.String,
    "friendlyName": fields.String,
    "acronym": fields.String,
    "dateCreated": fields.String,
    "dateUpdated": fields.String
}

resource_fields = {
    "matchSid": fields.String(attribute="match_sid"),
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
        primary_team = Teams.query.filter_by(acronym=match.primaryTeam).first()
        secondary_team = Teams.query.filter_by(acronym=match.secondaryTeam).first()
        match.primaryTeam = primary_team
        match.secondaryTeam = secondary_team
        print(match.primaryTeam, match.secondaryTeam)
        print(primary_team, secondary_team)
        return marshal(match, resource_fields)
