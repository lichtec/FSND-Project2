-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE Tournament (
	TournamentID serial,
	TournamentName varchar(254),
	Sport varchar(254),
	PRIMARY KEY(TournamentID)
);
						
CREATE TABLE Matches (
	MatchID serial,
	Winner integer references Players.PlayerID,
	Loser integer references Players.PlayerID, 
	TournamentID integer references Tournament,
	PRIMARY KEY(MatchID)
);

CREATE TABLE Players (
	PlayerID serial,
	PlayerFName varchar(254),
	PlayerLName varchar(254),
	TournamentID integer references Tournament,
	PRIMARY KEY(PlayerID)
);
