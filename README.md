# FSND-Project2

##Description:
Udacity Full Stack Nanodegree Project2. Creating a database to handle Swiss-pairing tournament. Code provides ability to delete players and matches, count the players in the DB, register players, report matches, get the current standings of players, and return a list of pairings.

##Requirements:

* It should be noted to actually use this, you will need to have postgresql installed along with psycopg2.

##Build Dependencies:

* This code requires python 2.7. To run the application you'll need to have tournament.py and you'll need to run tournament.sql to create the tables and the DB. 

##To Run:

1. To run the application you'll need to move tournament.py and tournament.sql to same folder and start-up psql.

2. When psql is running, run the following command `\i tournament.sql` to create the database and all the necessary tables and views and insert the default tournament.

3. You can now run the tournament python methods as necessary. 

##A Note Regarding Multiple Tournaments
Using multiple tournaments is possible but you can choose not to use it. If you don't specify a tournament then the functions wil reference the default tournament. To add an additional tournament use the NewTournament() function.
