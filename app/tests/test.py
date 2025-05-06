from tests.connection import test_mysql
from tests.connection import test_mssql 
from tests.connection import test_oracle
from tests.schema import schema 
from tests.sample_migrate import sample_migrate 
from tests.client import client 
from tests.subscription import subscription 

def main():
    # print("test database connection...")

    # test MySQL db connection!
    test_mysql()

    # test MSSQL db connection!
    test_mssql()

    # test ORACLE db connection!
    test_oracle()

    # run sample schema
    schema() 

    # test sample migration
    # sample_migrate() 

    # migrate test client
    # client() 

    # migrate test subscription
    # subscription() 

if __name__ == "__main__":
    main()

