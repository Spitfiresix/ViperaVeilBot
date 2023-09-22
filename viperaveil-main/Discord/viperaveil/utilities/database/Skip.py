import psycopg2

from viperaveil.utilities.database.Connection import db_connection


class DBSkip:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add(self, server, user):
        """Add a skip"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'INSERT INTO skip (server, "user") VALUES (%s, %s);'
        val = (str(server), str(user))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def clear(self, server):
        """clear the list of skip"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM skip WHERE server= %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def displayUsers(self, server):
        """Return the list of each user"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT "user" FROM skip WHERE server = %s;'
        val = (str(server),)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result
