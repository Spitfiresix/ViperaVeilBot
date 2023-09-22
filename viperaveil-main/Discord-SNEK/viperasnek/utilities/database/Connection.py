import psycopg2
import json
import os


class db_connection:
    def __init__(self):
        if (os.environ.get('DEBUG_MODE') == 'True'):
            with open("viperasnek/configurationtesting.json", "r") as config:
                data = json.load(config)
        else:
            with open("viperasnek/configuration.json", "r") as config:
                data = json.load(config)
        self.PostgresHost = data["PostgresHost"]
        self.PostgresLogin = data["PostgresLogin"]
        self.PostgresPassword = data["PostgresPasword"]
        self.PostgresDatabase = data["PostgresDatabase"]

    def getConnection(self):
        return psycopg2.connect(
            host=self.PostgresHost,
            user=self.PostgresLogin,
            password=self.PostgresPassword,
            database=self.PostgresDatabase,
            port='5434',
        )
