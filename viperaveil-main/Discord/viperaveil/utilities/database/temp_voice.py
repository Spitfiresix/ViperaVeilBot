
from viperaveil.utilities.database.Connection import db_connection

class DBTempVoice:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add(self, id, server):
        """Add a channel id and server id to table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO tempvoice (id, server) VALUES ('{id}', '{server}');"
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get(self, server):
        """Gets all temp channels in server"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM tempvoice WHERE server = '{server}';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result
    
    def get_all(self):
        """Gets all temp channel ids in table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT id FROM tempvoice;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result
    
    def delete(self, id):
        """Removes voice channel by id from table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM tempvoice WHERE id = '{id}';"
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        mydb.close()