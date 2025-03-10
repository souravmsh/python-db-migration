from tests.connection import test_mysql_connection
from tests.connection import test_mssql_connection 

def main():
    print("test database connection...")

    # test MySQL db connection!
    test_mysql_connection()

    # test MSSQL db connection!
    test_mssql_connection()

if __name__ == "__main__":
    main()

