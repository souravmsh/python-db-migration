from utils.mysql import mysql_connect
from utils.mssql import mssql_connect

def test_mysql():
    print('MySQL connection testing...')
    conn = mysql_connect()
    print(conn)
    if conn:
        print("connected...")
        print(conn)
        conn.close()  # Make sure to close the connection after use.
    else:
        print("Failed MSSQL connection.")
    
def test_mssql():
    print('MSSQL connection testing...')
    conn = mssql_connect()
    if conn:
        print("connected...")
        print(conn)
        conn.close()  # Make sure to close the connection after use.
    else:
        print("Failed MSSQL connection.")