from utils.mysql import mysql_connect
from utils.mssql import mssql_connect
from utils.config import config
from utils.log   import log

# ------------------------------------------------
# HOW TO ACCESS
# ------------------------------------------------
# from utils.migrate import Migrate
# from datetime import datetime

# source_table = 'Temp_Email'
# destination_table = 'subscriptions'
# query_chunk_size = 100

# column_mapping = {
#     'Investor_Code': 'client_code',
#     'e-mail': 'email',
#     'approved_dt': 'created_at',
# }

# extra_columns = {
#     'status': 'Active',
#     'updated_by': 1,
#     'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
# }

# def Subscription(): 
#     process = Migrate(source_table, destination_table, column_mapping, extra_columns, query_chunk_size)
#     process.migrate()
#     process.close_connections()
# ------------------------------------------------


class Migrate:

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

    """Fetch column names from the source or destination table."""
    def fetch_columns(self, table, is_source=True):
        try:
            query = (
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
                if is_source and config.source_database == "MSSQL"
                else f"SHOW COLUMNS FROM {table}"
            )
            # log.debug(f"⚙️ Query: {query}")

            cursor = self.source_cursor if is_source else self.dest_cursor
            cursor.execute(query)
            columns = [row[0] for row in cursor.fetchall()]
            return columns
        except Exception as e:
            log.error(f"❌ Error fetching columns from {table}: {e}")
            raise

    """Fetch data in chunks from the source table."""
    def fetch_data_chunk(self, columns, offset):
        try:
            column_list = ", ".join([f"[{col}]" if "-" in col else col for col in columns])
            query = (
                f"SELECT {column_list} FROM {self.source_table} ORDER BY (SELECT NULL) "
                f"OFFSET {offset} ROWS FETCH NEXT {self.query_chunk_size} ROWS ONLY"
                if config.source_database == "MSSQL"
                else f"SELECT {column_list} FROM {self.source_table} LIMIT {self.query_chunk_size} OFFSET {offset}"
            )
            # log.debug(f"⚙️ Query: {query}")

            self.source_cursor.execute(query)
            rows = self.source_cursor.fetchall()
            self.total_fetched += len(rows)
            return rows
        except Exception as e:
            log.error(f"❌ Error fetching data chunk from {self.source_table}: {e}")
            raise

    """Truncate the destination table before inserting new data."""
    def truncate_destination_table(self):
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

    """Map source columns to destination columns."""
    def map_columns(self, row, source_columns):
        try:
            mapped_values = [row[source_columns.index(source_col)] if source_col in source_columns else None 
                             for source_col in self.column_mapping.keys()]
            mapped_values.extend(self.extra_columns.values())
            return tuple(mapped_values)
        except Exception as e:
            log.error(f"❌ Error mapping row: {e}")
            raise


    """Insert mapped data into the destination table."""
    def insert_data(self, rows):
        try:
            columns = ", ".join(list(self.column_mapping.values()) + list(self.extra_columns.keys()))
            placeholders = ", ".join(["%s"] * (len(self.column_mapping) + len(self.extra_columns)))
            query = f"INSERT INTO {self.destination_table} ({columns}) VALUES ({placeholders})"

            self.dest_cursor.executemany(query, rows)
            self.dest_conn.commit()
            inserted_count = len(rows)
            self.total_inserted += inserted_count
            # log.debug(f"⚙️ Query: {query}")

        except Exception as e:
            log.error(f"❌ Error inserting data into {self.destination_table}: {e}")
            raise

    """Perform the migration process in chunks."""
    def migrate(self):
        try:
            self.truncate_destination_table()

            source_columns = self.fetch_columns(self.source_table, is_source=True)
            print(f"✅ Source Table Columns: {source_columns}")
            destination_columns = self.fetch_columns(self.destination_table, is_source=False)
            print(f"✅ Destination Table Columns: {destination_columns}")
            print(f"✅ Query Chunk Size: {self.query_chunk_size}")

            offset = sl = 0
            while True:
                rows = self.fetch_data_chunk(source_columns, offset)
                if not rows:
                    break

                mapped_rows = [self.map_columns(row, source_columns) for row in rows]
                self.insert_data(mapped_rows)

                sl = sl + 1
                print(f"✅ Progress [{sl}][{offset} ➝ {self.total_fetched}][{len(rows)}][{self.source_table}({self.total_fetched}) ➝ {self.destination_table}({self.total_inserted})]")
                log.info(f"✅ Progress [{sl}][{offset} ➝ {self.total_fetched}][{len(rows)}][{self.source_table}({self.total_fetched}) ➝ {self.destination_table}({self.total_inserted})]")
                
                offset += self.query_chunk_size

            log.info(f"✅ Migration completed successfully! Total fetched: {self.total_fetched}, Total inserted: {self.total_inserted}")
            print(f"✅ Migration completed successfully! Total fetched: {self.total_fetched}, Total inserted: {self.total_inserted}")
        except Exception as e:
            log.error(f"❌ Migration failed: {e}")
            raise

    """Close database connections."""
    def close_connections(self):
        try:
            self.source_cursor.close()
            self.source_conn.close()
            self.dest_cursor.close()
            self.dest_conn.close()
            log.info("✅ Closed database connections")
            print("✅ Closed database connections")
        except Exception as e:
            log.error(f"❌ Error closing connections: {e}")
            print(f"❌ Error closing connections: {e}")
            raise

"""Run the migration function and handle errors."""
def migrate(migration_func):
    try:
        migration_func()
        log.info("Migration completed successfully")
    except Exception as e:
        log.error(f"❌ Migration failed: {e}")
        print(f"❌ Migration failed: {e}")
