import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:

    source_database = os.getenv("SOURCE_DATABASE", "MSSQL")
    destination_database = os.getenv("DESTINATION_DATABASE", "MYSQL")
    query_chunk_size = int(os.getenv("QUERY_CHUNK_SIZE", 1000))
    reference_id = os.getenv("REFERENCE_ID", "MIGAPP01")

    mysql = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': os.getenv('MYSQL_PORT', '3306'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', ''),
    }

    mssql = {
        'DRIVER': os.getenv('MSSQL_DRIVER', '{ODBC Driver 17 for SQL Server}'),
        'SERVER': os.getenv('MSSQL_SERVER', 'localhost'),
        'PORT': os.getenv('MSSQL_PORT', '1433'),
        'DATABASE': os.getenv('MSSQL_DATABASE', ''),
        'UID': os.getenv('MSSQL_UID', 'sa'),
        'PWD': os.getenv('MSSQL_PWD', ''),
        'ENCRYPT': os.getenv('MSSQL_ENCRYPT', 'no'),
    }

    oracle = { 
        'host': os.getenv('ORACLE_HOST', 'localhost'),
        'port': os.getenv('ORACLE_PORT', '1521'), 
        'user': os.getenv('ORACLE_USER', ''),
        'password': os.getenv('ORACLE_PASSWORD', ''),
        'sid': os.getenv('ORACLE_SID', ''),
    }

# Create an instance of the Config class
config = Config()
