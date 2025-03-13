from tests.connection import test_mysql
from tests.connection import test_mssql 
from tests.migrate import migrate 
from utils.config import config

def main():
    print("test database connection...")

    # test MySQL db connection!
    # test_mysql()

    # test MSSQL db connection!
    # test_mssql()

    # test migration from mysql to mysql
    migrate()

if __name__ == "__main__":
    main()

