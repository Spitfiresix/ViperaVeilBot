from viperaveil.utilities.database.Connection import db_connection


class DBExtLog:

    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def add(self, update_type, channel_id, video_id, server):
        """Add a update_type, channel_id and video_id to table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO external_log (update_type, channel_id, video_id, server) VALUES ('{update_type}', '{channel_id}', '{video_id}', '{server}');"
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get_by_server(self, server):
        """Gets all records by server"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM external_log WHERE server = '{server}';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result
    
    def get_by_video_id(self, video_id):
        """Gets all entries by video id in server"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM external_log WHERE video_id = '{video_id}';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result
    
    def get_all(self):
        """Gets all channel_ids in table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT channel_id FROM external_log;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result
    
    def delete(self, channel_id):
        """Removes entry by channel_id from table"""
        mydb = self.db_connection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM external_log WHERE channel_id = '{channel_id}';"
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        mydb.close()