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
	


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    cursor.close()
	


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit()
    cursor.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(player_id) FROM players;")
    playerCount=cursor.fetchall()
    playerCount=playerCount[0][0]
    cursor.close()
    return playerCount


def registerPlayer(PlayerName, tournamentID=""):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      PlayerName: the player's  name (need not be unique).
      tournamentID: the unique id of the tournament the player is in, not required at this point, will have to build some way to provide ref error.

    """
    db = connect()
    cursor = db.cursor()
    #Different decisiions based on the tournament id. Using 0 as a standard blank tournament that's included in my sql
    if tournamentID != "":
        cursor.execute("INSERT INTO Players (PlayerName, TournamentID) VALUES(%s, %s);", (PlayerName, tournamentID))
    else:
        cursor.execute("INSERT INTO Players (PlayerName, TournamentID) VALUES(%s, %s);", (PlayerName, 0))
    db.commit()
    cursor.close()
	
def playerStandings():
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
	cursor.execute("select * from Scores")
	standings=cursor.fetchall()
	cursor.close()
	return standings


def reportMatch(winner, loser, tournamentID=""):
    """Records the outcome of a single match between two players.
        Args:
            winner:  the id number of the player who won
            loser:  the id number of the player who lost
            tournamentID: the unique id of the tournament the player is in, not required at this point, will have to build some way to provide ref error.
    """

    db = connect()
    cursor = db.cursor()
    #Different decisiions based on the tournament id. Using 0 as a standard blank tournament that's included in my sql
    if tournamentID != "":
        cursor.execute("INSERT INTO Matches (winner, loser, tournamentID) VALUES(%s, %s, %s);", (winner, loser, tournamentID))
    else:
        cursor.execute("INSERT INTO Matches (winner, loser, tournamentID) VALUES(%s, %s, %s);", (winner, loser, 0))
    db.commit()
    cursor.close()
	
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
     return matchesList