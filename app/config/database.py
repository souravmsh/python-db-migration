import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def config_mysql():
    return {
        'host': os.getenv('MYSQL_HOST'),
        'port': os.getenv('MYSQL_PORT'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE'),
    }

def config_mssql():
    return {
        'DRIVER': os.getenv('MSSQL_DRIVER'),
        'SERVER': os.getenv('MSSQL_SERVER'),
        'PORT': os.getenv('MSSQL_PORT'),
        'DATABASE': os.getenv('MSSQL_DATABASE'),
        'UID': os.getenv('MSSQL_UID'),
        'PWD': os.getenv('MSSQL_PWD'),
        'ENCRYPT': os.getenv('MSSQL_ENCRYPT', 'no'),
    }
