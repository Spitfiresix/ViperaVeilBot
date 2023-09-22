import psycopg2

from viperaveil.utilities.database.Connection import db_connection

import datetime


class DBPickup:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_match(self, type, players, ranked = False):
        """Add a new match to matches table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `matches` (`type`, `players`, `ranked`, `outcome`) VALUES (%s, %s, %s, %s);"
        val = (type, players, ranked, False)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()