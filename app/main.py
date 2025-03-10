import time
from migrations.migrate import Migrate
from migrations.tables.client import Client

def main():
    print("Starting data migration process")
    time.sleep(1000)
    # Run migration for the Client table
    Migrate(Client)

if __name__ == "__main__":
    main()

