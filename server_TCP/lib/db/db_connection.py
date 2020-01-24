import json
import os
import mysql.connector


class DataBase(object):

    def __init__(self, config_file='config/db_config.json'):
        self.__HOST = None
        self.__PORT_NUMBER = None
        self.__LOGIN = None
        self.__PASSWORD = None
        self.__DB_NAME = None
        self.__read_config(config_file)
        self.__connection = None
        self.__open_connection()

    def __open_connection(self):
        try:
            self.__connection = mysql.connector.connect(host=self.__HOST, user=self.__LOGIN, passwd=self.__PASSWORD,
                                                        database=self.__DB_NAME)
            if self.__connection.is_connected():
                print(self.__connection)
                db_info = self.__connection.get_server_info()
                print("Successful open connection to MySQL databess... (" + db_info + ")")
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
            raise ConnectionError(e)

    def close_connection(self):
        if self.__connection.is_connected():
            self.__connection.close()
            print("MySQL connection is closed")
        else:
            print("MySQL connection cannot be closed because is closed already")

    def make_query(self, query):
        cursor = self.__connection.cursor()
        cursor.execute(query)
        print("DEBUG make query:" + str(cursor))
        result = cursor.fetchall()
        cursor.close()
        return result

    def __read_config(self, config_file):
        if os.path.isfile(config_file):
            with open(config_file) as json_file:
                config_file = json.load(json_file)
                self.__HOST = config_file['host']
                self.__PORT_NUMBER = config_file['portNumber']
                self.__LOGIN = config_file['login']
                self.__PASSWORD = config_file['passwd']
                self.__DB_NAME = config_file['db_name']
        else:
            raise Exception('Cannot find db_config file ' + config_file)


if __name__ == '__main__':
    db = DataBase('../config/db_config.json')
    print(db.make_query("SELECT * FROM player"))
