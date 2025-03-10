import pyodbc
from config.database import config_mssql

def connection_mssql():
    config = config_mssql()
    try:
        # Attempting to establish the connection to MSSQL server
        port = config.get('PORT', 1433)
        encrypt = config.get('ENCRYPT', 'no')

        connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"  # Correct driver name
            f"SERVER={config['SERVER']},{port};"  # Including port
            f"DATABASE={config['DATABASE']};"
            f"UID={config['UID']};"
            f"PWD={config['PWD']};"
            f"Encrypt={encrypt};"
        )
        print("Successfully connected to MSSQL database")
        
        return connection
    except pyodbc.Error as e:
        # Handle errors that occur during the connection attempt
        print(f"Error: Unable to connect to MSSQL database: {e}")
        return None
    