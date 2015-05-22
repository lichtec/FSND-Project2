#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# 

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
		conn = psycopg2.connect("dbname=tournament")
		return conn
    except psycopg2.Error as e:
		print e

def newTournament(tournament_name="", sport=""):
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tournaments (tournament_name, sport) VALUES(%s, %s);", (tournament_name, sport))
    db.commit()
    cursor.execute("SELECT tournament_id FROM tournaments ORDER BY tournament_id DESC")
    newTournamentID = cursor.fetchone()
    cursor.close()
    db.close()
    return "New Tournament ID is {0}".format(newTournamentID[0])

def listTournaments():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tournaments;")
    tournaments = cursor.fetchall()
    cursor.close()
    db.close()
    return tournaments


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    cursor.close()
    db.close()
	


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit()
    cursor.close()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(player_id) FROM players;")
    playerCount=cursor.fetchall()
    playerCount=playerCount[0][0]
    cursor.close()
    db.close()
    return playerCount


def registerPlayer(player_name, tournament_id=""):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      player_name: the player's  name (need not be unique).
      tournament_id: the unique id of the tournament the player is in, not required at this point, will have to build some way to provide ref error.

    """
    db = connect()
    cursor = db.cursor()
    #Different decisiions based on the tournament id. Using 0 as a standard blank tournament that's included in my sql
    if tournament_id != "":
        cursor.execute("INSERT INTO Players (player_name, tournament_id) VALUES(%s, %s);", (player_name, tournament_id))
    else:
        cursor.execute("INSERT INTO Players (player_name, tournament_id) VALUES(%s, %s);", (player_name, 0))
    db.commit()
    cursor.close()
    db.close()
	
def playerStandings(tournament_id=""):
    """Returns a list of the players and their win records, sorted by wins.
        The first entry in the list should be the player in first place, or a player
        tied for first place if there is currently a tie.
    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    #playerStandings utilizes the the scores view to show current standings
    if tournament_id == "":
        cursor.execute("SELECT id, player_name, wins, matches FROM scores WHERE tournament_id=0;")
    else:
        cursor.execute("SELECT id, player_name, wins, matches FROM scores WHERE tournament_id=%s;", (tournament_id))
    standings=cursor.fetchall()
    cursor.close()
    db.close()
    return standings


def reportMatch(winner, loser, tournament_id=""):
    """Records the outcome of a single match between two players.
        Args:
            winner:  the id number of the player who won
            loser:  the id number of the player who lost
            tournament_id: the unique id of the tournament the player is in, not required at this point, will have to build some way to provide ref error.
    """

    db = connect()
    cursor = db.cursor()
    #Different decisiions based on the tournament id. Using 0 as a standard blank tournament that's included in my sql
    if tournament_id != "":
        cursor.execute("INSERT INTO Matches (winner, loser, tournament_id) VALUES(%s, %s, %s);", (winner, loser, tournament_id))
    else:
        cursor.execute("INSERT INTO Matches (winner, loser, tournament_id) VALUES(%s, %s, %s);", (winner, loser, 0))
    db.commit()
    cursor.close()
    db.close()
	
def swissPairings():
     """Returns a list of pairs of players for the next round of a match.
  
     Assuming that there are an even number of players registered, each player
     appears exactly once in the pairings.  Each player is paired with another
     player with an equal or nearly-equal win record, that is, a player adjacent
     to him or her in the standings.
  
     Returns:
       A list of tuples, each of which contains (id1, name1, id2, name2)
         id1: the first player's unique id
         name1: the first player's name
         id2: the second player's unique id
         name2: the second player's name
     """
     db = connect()
     cursor = db.cursor()
     cursor.execute("select * from Scores")
     standings=cursor.fetchall()
     matchesList = []
     if(len(standings) % 2 == 0):
         while(len(standings)>0):
             player1=standings.pop()
             player2=standings.pop()
             matchesList.append((player1[0], player1[1], player2[0], player2[1]))
     #Code to handle a possible bi
     else:
        while(len(standings)>1):
             player1=standings.pop()
             player2=standings.pop()
             matchesList.append((player1[0], player1[1], player2[0], player2[1]))
        player1=standings.pop()
        matchesList.append((player1[0], player1[1], 0, 'BI'))
        reportMatch(player1[0], 0)
     db.close()
     return matchesList