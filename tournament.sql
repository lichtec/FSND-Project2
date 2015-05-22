-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--Be sure to have created the DB before running this code to create the tables.
--CREATE DATABASE Tournament;


CREATE TABLE tournaments
	(tournament_id serial, tournament_name varchar(254), sport varchar(254), PRIMARY KEY(tournament_id));
CREATE TABLE players
	(player_id serial, player_name varchar(254) not null, tournament_id serial references tournaments, PRIMARY KEY(player_id));
CREATE TABLE matches
	(match_id serial, winner serial references players not null, loser serial references players, tournament_id integer references tournaments, PRIMARY KEY(match_id));
CREATE VIEW scores AS
	SELECT
  a.player_id as ID, a.player_name, (select count(winner) from matches where winner=a.player_id) as wins, (select count(winner) from matches where winner=a.player_id) + (select count(loser) from matches where Loser=a.player_id) as matches, a.tournament_id
FROM
  players a left join matches b on (a.player_id=b.winner)
Group By a.player_id, a.player_name
Order By wins Desc;

INSERT INTO tournaments (tournament_id) Values(0);
