--SQL Scratch
SELECT
  a.PlayerID as ID, a.PlayerFName, a.PlayerLName, (select count(winner) from matches where winner=a.PlayerID) as Wins, (select count(Loser) from matches where Loser=a.PlayerID) as Losses
FROM
  Players a left join Matches b on (a.PlayerID=b.Winner)
Group By a.PlayerID, a.PLayerFName, a.PlayerLName;