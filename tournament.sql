-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE Tournament
	(TournamentID serial, TournamentName varchar(254), Sport varchar(254), PRIMARY KEY(TournamentID))
;

CREATE TABLE Players
	(PlayerID serial, PlayerFName varchar(254), PlayerLName varchar(254), TournamentID integer references Tournament, PRIMARY KEY(PlayerID))
;

CREATE TABLE Matches
	(MatchID serial, Winner serial references Players, Loser serial references Players, TournamentID integer references Tournament, PRIMARY KEY(MatchID))
;

CREATE VIEW Scores AS
	SELECT
  a.PlayerID as ID, a.PlayerFName, a.PlayerLName, (select count(winner) from matches where winner=a.PlayerID) as Wins, (select count(Loser) from matches where Loser=a.PlayerID) as Losses
FROM
  Players a left join Matches b on (a.PlayerID=b.Winner)
Group By a.PlayerID, a.PLayerFName, a.PlayerLName; 
