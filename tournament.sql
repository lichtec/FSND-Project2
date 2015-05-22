--  Table definitions for the tournament project.
--
--  Put your SQL 'create table' statements in this file; also 'create view'
--  statements if you choose to use it.
--
--  You can write comments in this file by starting them with two dashes, like
--  these lines here.
-- Be sure to have created the DB before running this code to create the tables.

--  We'll drop any old version s of the database to create clean. 
-- THIS WILL DELETE ANY PREVIOUS DATA
DROP DATABASE IF EXISTS tournament;

-- We'll create the database.
CREATE DATABASE Tournament;

-- We'll now connect to the newly created database
\c tournament;

-- Tournaments table holds the tournament info. 
-- It will contain a single record if the user is not using different tournaments. 
CREATE TABLE tournaments
	(tournament_id serial, tournament_name varchar(254), 
	sport varchar(254), PRIMARY KEY(tournament_id));
	
-- Players table holds the player info. This is just the assigned id, 
-- the name, and a tournament id. At this point a user is assigned to 
-- only one tournament.
-- There may be duplicate players if they are in multiple tournaments.
CREATE TABLE players
	(player_id serial, player_name varchar(254) not null, 
	tournament_id serial references tournaments, 
	PRIMARY KEY(player_id));

-- Matches table holds all of the matches. It is an assigned match id, 
-- and the winner and loser player ids, and it references the tournament id
CREATE TABLE matches
	(match_id serial, winner serial references players not null,
	loser serial references players, tournament_id integer 
	references tournaments, PRIMARY KEY(match_id));

-- This view is used to report the scores of the players. It uses a left 
-- join to pull the players data and calculates wins and total matches 
-- from the matches table. The view also returns the tournament id 
-- from the player table but we remove that with the query from 
-- python methods. Tournament_id is returned so that we can look at 
-- only specific tournaments as necessary. The view also orders the 
-- results by players wins descending so we can just quickly pair up players.
CREATE VIEW scores AS
	SELECT a.player_id as ID, a.player_name, 
	(select count(winner) from matches where winner=a.player_id) as wins, 
	(select count(winner) from matches where winner=a.player_id) + 
	(select count(loser) from matches where Loser=a.player_id) as matches, 
  a.tournament_id
FROM
  players a left join matches b on (a.player_id=b.winner)
Group By a.player_id, a.player_name
Order By wins Desc;

-- We'll need at least one tournament to work with even if the user doesn't 
-- want multiple tournaments. The python methods will handle the lack of a 
--tournament id by using this default tournament.
INSERT INTO tournaments (tournament_id) Values(0);
