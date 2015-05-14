#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
deleteStatement = "DELETE FROM {0};"
countStatement = "SELECT COUNT({0}) FROM {1};"
insertStatement = "INSERT INTO {0} ({1}) VALUES({2});"

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Matches;")
    db.commit()
    cursor.close()
	


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Players;")
    db.commit()
    cursor.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(PlayerId) FROM Players;")
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
    if tournamentID != "":
        cursor.execute("INSERT INTO Players (PlayerName, TournamentID) VALUES(%s, %s);", (PlayerName, tournamentID))
    else:
        cursor.execute("INSERT INTO Players (PlayerName, TournamentID) VALUES(%s, %s);", (PlayerName, 0))
    #cursor.execute(statement)
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
	cursor.execute("select * from Scores")
	standings=cursor.fetchall()
	#print standings
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
     #print standings
     matchesList = []
     if(standings.len() % 2 == 0):
         while(standings.len()>0):
             player1=standings.pop()
             player2=standings.pop()
             matchesList.append((player1[0], player1[1], player2[0], player[1]))
    else:
        while(standings.len()>1):
             player1=standings.pop()
             player2=standings.pop()
             matchesList.append((player1[0], player1[1], player2[0], player[1]))
        player1=standings.pop()