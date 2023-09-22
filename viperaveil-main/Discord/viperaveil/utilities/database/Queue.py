import psycopg2
import datetime
import random

from viperaveil.utilities.database.Connection import db_connection


class DBQueue:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add(
            self,
            server,
            isPlaying,
            requester,
            textChannel,
            voiceChannel,
            track,
            title,
            duration,
            thumb,
            index):
        """Add a song in the queue"""
        t1 = datetime.datetime.now()
        # print("DB QUEUE add", t1)
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'INSERT INTO queue (server, "isPlaying", requester, "textChannel", "voiceChannel", track, title, duration, thumb, index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        val = (
            str(server),
            isPlaying,
            requester,
            str(textChannel),
            str(voiceChannel),
            track,
            title,
            duration,
            thumb,
            index)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        # print("DB QUEUE add", datetime.datetime.now() - t1)

    def remove(self, server, index):
        """Remove the song from the queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE server = %s AND index = %s;"
        val = (str(server), index)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def removeFormer(self, server):
        """Remove the former song (index = -1) from the queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE server = %s AND index = -1;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updatePlayingToFormer(self, server):
        """update the playing track to former track SET (index = -1)"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        # query = f'UPDATE queue SET "isPlaying"= false, index = 0 WHERE server = %s AND "isPlaying"= true;'
        query = f'UPDATE queue SET index = -1, "isPlaying" = false WHERE index = 0 and server = %s;'
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateCurrentToFormerVV(self, server):
        """update the playing track to former track"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        # query = f'UPDATE queue SET "isPlaying"= false, index = 0 WHERE server = %s AND "isPlaying"= true;'
        query = f'UPDATE queue SET index = (case index when -1 then 0 when 0 then -1 else index end) WHERE index in (-1,0) and server = %s;'
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateRemoveOneToEach(self, server, indexFrom, indexTo):
        """remove 1 to each track between 2 indexes"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE queue SET index = index -1 WHERE server = %s AND index > %s AND index <= %s;"
        val = (str(server), indexFrom, indexTo)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def updateAddOneToEach(self, server, indexFrom, indexTo):
        """add 1 to each track between 2 indexes"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE queue SET index = index +1 WHERE server = %s AND index >= %s AND index < %s;"
        val = (str(server), indexTo, indexFrom)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        mycursor.close()
        mydb.close()

    def getFutureIndex(self, server):
        """Return the max index of a server's queue"""
        # t1 = datetime.datetime.now()
        # print("DB QUEUE getFutureIndex", t1)
        mydb = self.db_connection.getConnection()
        # print("connection_id", mydb._cnx.connection_id)
        mycursor = mydb.cursor()
        query = f"SELECT MAX(index) FROM queue WHERE server= %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        mydb.close()
        # print("DB QUEUE getFutureIndex", datetime.datetime.now() - t1)
        # print(result[0][0])
        return result[0][0]

    def getNextIndex(self, server):
        """Return the next index of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT MIN(index) FROM queue WHERE server = %s AND index > 0;'
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result[0][0]

    def getIndexFromFakeIndex(self, server, index):
        """Return the real index from a fake index (1 to x)"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT index FROM queue WHERE server = %s AND "isPlaying" = false AND index != 0 ORDER BY index ASC LIMIT 1 OFFSET %s;'
        val = (str(server), index)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result[0][0]

    def getCurrentSong(self, server):
        """Return the playing song of a server's queue (index = 0)"""
        try:
            mydb = self.db_connection.getConnection()
            mycursor = mydb.cursor()
            query = f'SELECT id, server, "isPlaying", requester, "textChannel", "voiceChannel", track, title, duration, thumb, index FROM queue WHERE server= %s AND index = 0;'
            val = (str(server), )
            mycursor.execute(query, val)
            result = mycursor.fetchall()
            mycursor.close()
            mydb.close()
            return result[0]
        except BaseException:
            return None

    def getNextSong(self, server):
        """Return the next song of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        # query = f'SELECT * FROM queue WHERE server= %s AND "isPlaying" = false AND index != 0 ORDER BY index ASC LIMIT 1;'
        query = f'SELECT id, server, "isPlaying", requester, "textChannel", track, title, duration, thumb,\
             index FROM queue WHERE server= %s AND index > 0 ORDER BY index ASC LIMIT 1;'
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) == 0:
            return None
        return result[0]

    def getRandomSong(self, server):
        """Return a random song from the server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT id, server, "isPlaying", requester, "textChannel", track, title, duration, thumb,\
             index FROM queue WHERE server = %s AND index > 0 ORDER BY index ASC;'
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) == 0:
            return None
        result = result[random.randint(0, len(result) - 1)]
        return result

    def countQueueItems(self, server):
        """Return the size of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT COUNT(*) FROM queue WHERE server = %s AND index >= 0;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result[0][0]

    def countPlayingItems(self):
        """Return the size of a server's queue playing track"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT COUNT(*) FROM queue WHERE index = 0;'
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result[0][0]

    def queueSizeAndDuration(self, server):
        """Return the queue duration of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT SUM(duration), COUNT(*) FROM queue WHERE server = %s AND index >= 0;'
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if result[0][0] is None:
            return None
        return result[0]

    def setIsPlaying(self, server, index):
        """Set the track to isPLaying SET (index = 0)"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'UPDATE queue SET "isPlaying" = true, index = 0 WHERE id = (select id from queue where server = %s AND index= %s LIMIT 1);'
        val = (str(server), index)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def clear(self, server):
        """Clear all the queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE server = %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def clearFutureTracks(self, server):
        """Clear all the queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'DELETE FROM queue WHERE server = %s AND index > 0;'
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def display(self, server):
        """Return the content of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT * FROM queue WHERE server = %s AND index >= 0 ORDER BY index ASC;'
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result

    def displayFormer(self, server):
        """Return the previously played track of a server's queue (index = -1)"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE server = %s AND index = -1;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) == 0:
            return None
        return result[0]

    def displaySpecific(self, server, index):
        """Return the content of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE server= %s AND index= %s LIMIT 1;"
        val = (str(server), index)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) == 0:
            return None
        return result[0]

    def displayAllPlaying(self):
        """Return the content of a server's queue"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f'SELECT * FROM queue WHERE index = 0;'
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) == 0:
            return None
        return result
