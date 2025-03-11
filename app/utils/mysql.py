import mysql.connector
from mysql.connector import Error
from utils.config import config

def mysql_connect():
    
    try:
        port = int(config.mysql.get('port', 3306))  # Convert the port to integer

        connection = mysql.connector.connect(
            host=config.mysql['host'],
            port=port,
            user=config.mysql['user'],
            password=config.mysql['password'],
            database=config.mysql['database']
        )
        
        # Check if the connection is successful
        if connection.is_connected():
            return connection
        else:
            print("MySQL connection failed!")
            return None
    
    except Error as e:
        print(f"MSSQL connection error: {e}")
        return None
