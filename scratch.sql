--SQL Scratch
SELECT
  a.PlayerID as ID, a.PlayerFName, a.PlayerLName, (select count(winner) from matches where winner=a.PlayerID) as Wins, (select count(Loser) from matches where Loser=a.PlayerID) as Losses
FROM
  Players a left join Matches b on (a.PlayerID=b.Winner)
Group By a.PlayerID, a.PLayerFName, a.PlayerLName;

SELECT MatchID
FROM Matches
WHERE Winner = {0} OR Loser = {0};

INSERT INTO Tournament
	(TournamentName, Sport)
VALUES
	('Test1', 'Chess'),
	('Test2', 'Badmitton'),
	('Test3', 'Soccer')
;

INSERT INTO Players
	(PlayerFName, PlayerLName, TournamentID)
VALUES
	('Chris', 'Chess', 1),
	('Chris', 'Lichter', 1),
	('Chris', 'Test', 1)
;

INSERT INTO Matches
	(Winner, Loser, TournamentID)
VALUES
	('1', '2', 1),
	('2', '3', 1),
	('1', '3', 1)
;