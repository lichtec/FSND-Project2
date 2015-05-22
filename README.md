# FSND-Project2

##Description:
Udacity Full Stack Nanodegree Project2. Creating a database to handle Swiss-pairing tournament. Code provides ability to delete players and matches, count the players in the DB, register players, report matches, get the current standings of players, and return a list of pairings.

##Requirements:

* It should be noted to actually use this, you will need to have postgresql installed along with psycopg2.

##Build Dependencies:

* This code requires python 2.7. To run the application you'll need to have tournament.py and you'll need to run tournament.sql to create the tables and the DB. 

##To Run:

1. To run the application you'll need to move tournament.py and tournament.sql to same folder and startup psql.

2. When psql is running, run the following command `CREAT DATABASE tournament;`

3. Once the database has been created run `/c tournament;` to connect to the new database.

4. When connected to tournament, run `/i tournament.sql` to create all the necessary tables and views.

5. You can now run the tournament python methods as necessary. 
