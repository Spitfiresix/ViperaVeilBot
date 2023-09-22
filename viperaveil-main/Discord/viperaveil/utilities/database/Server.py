import psycopg2

from viperaveil.utilities.database.Connection import db_connection


class DBServer:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add(self, server, prefix, loop, loopQueue, shuffle, djRole, volume):
        """Add a server"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'INSERT INTO public.server (server, prefix, loop, "loopQueue", shuffle, "djRole", volume) VALUES (%s, %s, %s, %s, %s, %s, %s);'
        val = (str(server), prefix, loop, loopQueue, shuffle, djRole, volume)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def remove(self, server):
        """Remove a server"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM 'server' WHERE 'server'= %s LIMIT 1;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def clearMusicParameters(self, server, loop, loopQueue, shuffle):
        """Set the track to isPLaying"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'UPDATE server SET loop= %s, "loopQueue" = %s, shuffle = %s WHERE server = %s;'
        val = (loop, loopQueue, shuffle, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def display(self):
        """Return the content of servers"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT server, prefix, loop, "loopQueue", shuffle, "djRole", volume, message FROM server;'
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result

    def displayServer(self, server):
        """Return the content of servers"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT server, prefix, loop, "loopQueue", shuffle, "djRole", volume, message FROM server WHERE server= %s;'
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result[0]

    def updateLoop(self, server, loop):
        """Set the track to isPLaying"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE server SET loop = %s WHERE server = %s;"
        val = (loop, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateLoopQueue(self, server, loopQueue):
        """Set the track to isPLaying"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'UPDATE server SET "loopQueue"= %s WHERE server = %s;'
        val = (loopQueue, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateShuffle(self, server, shuffle):
        """Set the track to isPLaying"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'UPDATE server SET shuffle= %s WHERE server = %s;'
        val = (shuffle, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateVolume(self, server, volume):
        """Sets volume for guild"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'UPDATE server SET volume= %s WHERE server = %s;'
        val = (volume, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateMessage(self, server, message):
        """Sets embed message id for guild"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'UPDATE server SET message= %s WHERE server = %s;'
        val = (str(message), str(server))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
