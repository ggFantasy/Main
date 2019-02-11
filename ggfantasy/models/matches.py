from sqlalchemy import Column, String, SMALLINT, TIMESTAMP, DATETIME
from sqlalchemy.dialects.mysql import TINYINT
from ggfantasy.models.engine import Base

from datetime import datetime


class Matches(Base):
    __tablename__ = "matches"
    dateCreated = Column(TIMESTAMP, default=datetime.utcnow())
    dateUpdated = Column(TIMESTAMP)
    matchSid = Column(String, primary_key=True)
    tournamentSid = Column(String)
    bracketSid = Column(String)
    primaryTeam = Column(String)
    secondaryTeam = Column(String)
    scheduledTime = Column(DATETIME)
    state = Column(TINYINT)

    def __init__(self,
                 match_sid,
                 tournament_sid,
                 bracket_sid,
                 primary_team,
                 secondary_team,
                 scheduled_time,
                 state,
                 date_created=None,
                 date_updated=None):
        self.dateCreated = date_created
        self.dateUpdated = date_updated
        self.matchSid = match_sid
        self.tournamentSid = tournament_sid
        self.bracketSid = bracket_sid
        self.primaryTeam = primary_team
        self.secondaryTeam = secondary_team
        self.scheduledTime = scheduled_time
        self.state = state
