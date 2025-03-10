import mysql.connector
from config.database import config_mysql
from mysql.connector import Error

def connection_mysql():
    config = config_mysql()
    
    try:
        port = int(config.get('port', 3306))  # Convert the port to integer

        connection = mysql.connector.connect(
            host=config['host'],
            port=port,
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        # Check if the connection is successful
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
        else:
            print("Failed to connect to MySQL database")
            return None
    
    except Error as e:
        print(f"Error: {e}")
        return None
