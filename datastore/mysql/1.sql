CREATE TABLE matches (
    DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    DateUpdated TIMESTAMP DEFAULT NULL,
    MatchSid varchar(36),
    TournamentSid varchar(36),
    BracketSid varchar(36),
    PrimaryTeam varchar(36),
    SecondaryTeam varchar(36),
    State tinyint,
    ScheduledTime datetime
);