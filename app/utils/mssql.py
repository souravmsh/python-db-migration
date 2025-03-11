import pyodbc
from utils.config import config

def mssql_connect():
    try:
        # Attempting to establish the connection to MSSQL server
        port = config.mssql.get('PORT', 1433)
        encrypt = config.mssql.get('ENCRYPT', 'no')

        connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"  # Correct driver name
            f"SERVER={config.mssql['SERVER']},{port};"  # Including port
            f"DATABASE={config.mssql['DATABASE']};"
            f"UID={config.mssql['UID']};"
            f"PWD={config.mssql['PWD']};"
            f"Encrypt={encrypt};"
        )
        return connection
    except pyodbc.Error as e:
        # Handle errors that occur during the connection attempt
        print(f"MySQL connection error: {e}")
        return None
    