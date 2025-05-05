import cx_Oracle
from utils.config import config

def oracle_connect():
    try:
        port = int(config.oracle.get('port', 1521))  # default Oracle port is 1521
        
        dsn = cx_Oracle.makedsn(
            config.oracle['host'],
            port,
            sid=config.oracle['sid']
        )

        connection = cx_Oracle.connect(
            user=config.oracle['user'],
            password=config.oracle['password'],
            dsn=dsn
        )

        print("Oracle connection successful!")
        return connection

    except cx_Oracle.Error as e:
        print(f"Oracle connection error: {e}")
        return None
