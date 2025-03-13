from tests.connection import test_mysql
from tests.connection import test_mssql 
from app.tests.migrate import subscription 
from utils.config import config

def main():
    print("test database connection...")

    # test MySQL db connection!
    # test_mysql()

    # test MSSQL db connection!
    # test_mssql()

    # test migration from mysql to mysql
    subscription()

if __name__ == "__main__":
    main()

