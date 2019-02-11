CREATE TABLE teams (
    DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    DateUpdated TIMESTAMP DEFAULT NULL,
    LeagueSid smallint,
    TeamSid varchar(36),
    Slug varchar(36),
    FriendlyName varchar(36),
    Acronym varchar(12)
);