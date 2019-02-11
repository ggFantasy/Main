CREATE TABLE players (
    DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    DateUpdated TIMESTAMP DEFAULT NULL,
    LeagueSid smallint,
    Slug varchar(36),
    FriendlyName varchar(36),
    RoleSlug varchar(36),
    PrimaryTeam smallint,
    SecondaryTeam smallint
);