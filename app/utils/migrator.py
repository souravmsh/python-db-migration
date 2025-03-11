from utils.mysql import mysql_connect
from utils.mssql import mssql_connect
from utils.config import config
from utils.log   import log

class MigrationService:

    # Initialize
    def __init__(self, source_table, destination_table, column_mapping, extra_columns=None, query_chunk_size=None):
        self.source_table = source_table
        self.destination_table = destination_table
        self.column_mapping = column_mapping
        self.extra_columns = extra_columns or {}
        self.query_chunk_size = query_chunk_size if query_chunk_size is not None else config.query_chunk_size
        self.total_fetched = 0
        self.total_inserted = 0
        
        try:
            self.source_conn = mssql_connect() if config.source_database == "MSSQL" else mysql_connect()
            self.dest_conn = mysql_connect() if config.destination_database == "MYSQL" else mssql_connect()
            self.source_cursor = self.source_conn.cursor()
            self.dest_cursor   = self.dest_conn.cursor()
            log.info(f"✅ Initialized connection: {config.source_database} → {config.destination_database}, {self.source_table} → {self.destination_table}.")
            print(f"✅ Initialized connection: {config.source_database} → {config.destination_database}, {self.source_table} → {self.destination_table}.")
        except Exception as e:
            log.error(f"❌ Error initializing connections: {e}")
            print(f"❌ Error initializing connections: {e}")
            raise

    # Truncate the destination table
    def truncate(self, destination_table):
        try:
            query = f"TRUNCATE TABLE {self.destination_table}"
            self.dest_cursor.execute(query)
            self.dest_conn.commit()
            log.info(f"✅ Truncated table {self.destination_table}.")
            print(f"✅ Truncated table {self.destination_table}.")
            # log.debug(f"⚙️ Query: {query}")
        except Exception as e:
            log.error(f"❌ Error truncating {self.destination_table}: {e}")
            raise

    # Count the number of rows in the source table using the provided query
    def count_rows(self, query):
        return self.migrator.count_rows(query)

    def migrate(self, source_table, source_query, destination_table, prepare_data_func, chunk_size):
        # Start the migration process
        print(f"✅ Query Chunk Size: {chunk_size}")
        print(f"✅ Running source query: {source_query}")
        
        # Fetch source data in chunks
        offset = 0
        total_fetched = 0
        total_inserted = 0

        while True:
            rows = self.fetch_data_chunk(source_query, offset, chunk_size)
            if not rows:
                break

            mapped_rows = [prepare_data_func(row) for row in rows]
            self.insert_data(mapped_rows, destination_table)

            total_fetched += len(rows)
            total_inserted += len(mapped_rows)

            # Print progress
            print(f"✅ Progress [{offset // chunk_size + 1}] [{offset} ➝ {total_fetched}] "
                  f"[{len(rows)}] [source table: {source_table}({total_fetched}) ➝ "
                  f"destination table: {destination_table}({total_inserted})]")

            offset += chunk_size
        
        print(f"✅ Migration completed successfully! Total fetched: {total_fetched}, Total inserted: {total_inserted}")
    
    def fetch_data_chunk(self, query, offset, chunk_size):
        # Simulate fetching data with offset and limit
        # You'd use your actual database connection here
        query_with_limit = f"{query} LIMIT {chunk_size} OFFSET {offset}"
        print(f"⚙️ Fetching with query: {query_with_limit}")
        # Return dummy data as an example
        return [{'MerchantBankerID': 1, 'MerchantBankerName': 'Banker1', 'MasterAccount': '123'}] * chunk_size

    def insert_data(self, mapped_rows, destination_table):
        # Insert data into the destination table
        print(f"⚙️ Inserting {len(mapped_rows)} rows into {destination_table}")
        # Simulate database insertion
        pass
