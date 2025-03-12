from utils.mysql import mysql_connect
from utils.mssql import mssql_connect
from utils.config import config
from utils.log import log

class Migrator:

    def __init__(self):
        self.total_fetched = 0
        self.total_inserted = 0
        
        try:
            # Automatically decide source and destination DB from config/env
            self.source_conn = mssql_connect() if config.source_database == "MSSQL" else mysql_connect()
            self.dest_conn = mysql_connect() if config.destination_database == "MYSQL" else mssql_connect()
            
            # Configure cursors to return dictionaries
            if config.source_database == "MSSQL":
                self.source_cursor = self.source_conn.cursor()
            else:
                self.source_cursor = self.source_conn.cursor(dictionary=True)
                
            if config.destination_database == "MYSQL":
                self.dest_cursor = self.dest_conn.cursor(dictionary=True)
            else:
                self.dest_cursor = self.dest_conn.cursor()

        except Exception as e:
            log.error(f"❌ Error initializing connections: {e}")
            print(f"❌ Error initializing connections: {e}")
            raise

    def truncate(self, table_name=None):
        """Truncate the specified table in destination database"""
        try:
            target_table = table_name or self.destination_table
            if not target_table:
                raise ValueError("No table specified for truncation")
                
            query = f"TRUNCATE TABLE {target_table}"
            self.dest_cursor.execute(query)
            self.dest_conn.commit()
            log.info(f"✅ Truncated table {target_table}")
            print(f"✅ Truncated table {target_table}")
        except Exception as e:
            log.error(f"❌ Error truncating {target_table}: {e}")
            print(f"❌ Error truncating {target_table}: {e}")
            raise

    def count_rows(self, query):
        """Count total rows for the given query in source database"""
        try:
            count_query = f"SELECT COUNT(*) FROM ({query}) AS count_table"
            self.source_cursor.execute(count_query)
            result = self.source_cursor.fetchone()
            total_rows = result[0] if config.source_database == "MSSQL" else result['COUNT(*)']
            log.info(f"✅ Total rows in source query: {total_rows}")
            print(f"✅ Total rows in source query: {total_rows}")
            return total_rows
        except Exception as e:
            log.error(f"❌ Error counting rows of source query: {e}")
            print(f"❌ Error counting rows of source query: {e}")
            raise

    def fetch_data_chunk(self, query, offset, chunk_size):
        """Fetch a chunk of data from source database"""
        try:
            if config.source_database == "MSSQL":
                if "ORDER BY" not in query.upper():
                    query += " ORDER BY (SELECT NULL)"
                query_with_limit = f"{query} OFFSET {offset} ROWS FETCH NEXT {chunk_size} ROWS ONLY"
                self.source_cursor.execute(query_with_limit)
                columns = [column[0] for column in self.source_cursor.description]
                rows = [dict(zip(columns, row)) for row in self.source_cursor.fetchall()]
            else:  # MySQL
                query_with_limit = f"{query} LIMIT {chunk_size} OFFSET {offset}"
                self.source_cursor.execute(query_with_limit)
                rows = self.source_cursor.fetchall()  # Already dictionaries due to cursor config
                
            # log.debug(f"✅ Fetched {len(rows)} rows with query: {query_with_limit}")
            return rows
        except Exception as e:
            log.error(f"❌ Error fetching data chunk: {e}")
            raise

    def insert_data(self, mapped_rows, destination_table):
        """Insert mapped rows into destination table"""
        try:
            if not mapped_rows:
                return
                
            columns = list(mapped_rows[0].keys())
            placeholders = ','.join(['%s'] * len(columns))
            query = f"INSERT INTO {destination_table} ({','.join(columns)}) VALUES ({placeholders})"
            
            self.dest_cursor.executemany(query, [tuple(row.values()) for row in mapped_rows])
            self.dest_conn.commit()
            
            # log.debug(f"✅ Inserted {len(mapped_rows)} rows into {destination_table}")
        except Exception as e:
            log.error(f"❌ Error inserting data: {e}")
            raise

    def migrate(self, source_table, source_query, destination_table, prepare_data_func, chunk_size):
        """Perform the migration process"""
        try:

            self.source_table = source_table
            self.source_query = source_query
            self.destination_table = destination_table
            self.prepare_data_func = prepare_data_func
            self.query_chunk_size = chunk_size if chunk_size is not None else config.query_chunk_size

            log.info(f"✅ Initialized connection: {config.source_database} → {config.destination_database}, {self.source_table} → {self.destination_table}.")
            print(f"✅ Initialized connection: {config.source_database} → {config.destination_database}, {self.source_table} → {self.destination_table}.")
            print(f"✅ Query Chunk Size: {chunk_size}")
            print(f"✅ Running source query: {source_query}")
            
            # count total rows from source_query
            self.count_rows(source_query)

            offset  = sl = 0
            self.total_fetched = 0
            self.total_inserted = 0

            while True:
                rows = self.fetch_data_chunk(source_query, offset, chunk_size)
                if not rows:
                    break

                mapped_rows = [prepare_data_func(row) for row in rows]
                self.insert_data(mapped_rows, destination_table)

                fetched_count = len(rows)
                inserted_count = len(mapped_rows)
                self.total_fetched += fetched_count
                self.total_inserted += inserted_count
                sl = sl + 1

                progress_msg = (f"✅ Progress [{sl}][{offset} ➝ {self.total_fetched}][{len(rows)}][{self.source_table}({self.total_fetched}) ➝ {self.destination_table}({self.total_inserted})]")

                print(progress_msg)
                log.info(progress_msg)

                offset += chunk_size

            final_msg = (f"✅ Migration Done - Total fetched: {self.total_fetched}, Total inserted: {self.total_inserted}")
            
            print(final_msg)
            log.info(final_msg)
        

        except Exception as e:
            log.error(f"❌ Migration failed: {e}")
            print(f"❌ Migration failed: {e}")
            raise
        finally:
            self.source_cursor.close()
            self.dest_cursor.close()
            self.source_conn.close()
            self.dest_conn.close()
            log.info("✅ Closed database connections")
            print("✅ Closed database connections")