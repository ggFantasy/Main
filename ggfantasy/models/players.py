from sqlalchemy import Column, String, SMALLINT, TIMESTAMP
from ggfantasy.models.engine import Base


class Players(Base):
    __tablename__ = "players"
    dateCreated = Column(TIMESTAMP)
    dateUpdated = Column(TIMESTAMP)
    leagueSid = Column(SMALLINT, primary_key=True)
    slug = Column(String)
    friendlyName = Column(String)
    roleSlug = Column(String)
    primaryTeam = Column(SMALLINT)
    secondaryTeam = Column(SMALLINT)

    def __init__(self,
                 league_sid,
                 slug,
                 friendly_name,
                 role_slug,
                 primary_team,
                 secondary_team,
                 date_created=None,
                 date_updated=None):
        self.leagueSid = league_sid
        self.slug = slug
        self.friendlyName = friendly_name
        self.roleSlug = role_slug
        self.primaryTeam = primary_team
        self.secondaryTeam = secondary_team
        self.dateCreated = date_created
        self.dateUpdated = date_updated
