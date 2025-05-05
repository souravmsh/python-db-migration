from tests.connection import test_mysql
from tests.connection import test_mssql 
from tests.connection import test_oracle
from tests.migrate import migrate 
from utils.migrator import Migrator

from utils.oracle import oracle_connect

def main():
    # print("test database connection...")

    # test MySQL db connection!
    # test_mysql()

    # test MSSQL db connection!
    # test_mssql()

    # test ORACLE db connection!
    test_oracle()

    # test migration from mysql to mysql
    # migrate() 

if __name__ == "__main__":
    main()

