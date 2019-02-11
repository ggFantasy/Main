from sqlalchemy import Column, String, SMALLINT, TIMESTAMP
from ggfantasy.models.engine import Base


class Teams(Base):
    __tablename__ = "teams"
    dateCreated = Column(TIMESTAMP)
    dateUpdated = Column(TIMESTAMP)
    leagueSid = Column(SMALLINT, primary_key=True)
    teamSid = Column(String)
    slug = Column(String)
    friendlyName = Column(String)
    acronym = Column(String)

    def __init__(self,
                 league_sid,
                 team_sid,
                 slug,
                 friendly_name,
                 acronym,
                 date_created=None,
                 date_updated=None):
        self.leagueSid = league_sid
        self.teamSid = team_sid
        self.slug = slug
        self.friendlyName = friendly_name
        self.acronym = acronym
        self.dateCreated = date_created
        self.dateUpdated = date_updated
