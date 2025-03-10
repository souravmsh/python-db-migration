from database.mysql import connection_mysql
from database.mssql import connection_mssql

def test_mysql_connection():
    print('MySQL connection testing...')
    connection = connection_mysql()
    if connection:
        print("connected...")
        print(connection)
        connection.close()  # Make sure to close the connection after use.
    else:
        print("Failed MSSQL connection.")
    
def test_mssql_connection():
    print('MSSQL connection testing...')
    connection = connection_mssql()
    if connection:
        print("connected...")
        print(connection)
        connection.close()  # Make sure to close the connection after use.
    else:
        print("Failed MSSQL connection.")