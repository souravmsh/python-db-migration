from database.mysql import connection_mysql
from database.mssql import connection_mssql

class Migrate:
    def __init__(self, source_table, target_table, column_mapping, default_values=None, chunk_size=1000):
        self.source_table = source_table
        self.target_table = target_table
        self.column_mapping = column_mapping
        self.default_values = default_values or {}
        self.chunk_size = chunk_size
        self.mssql_conn = connection_mssql()
        self.mysql_conn = connection_mysql()
        self.mssql_cursor = self.mssql_conn.cursor()
        self.mysql_cursor = self.mysql_conn.cursor()

    def fetch_columns(self, table, is_source=True):
        if is_source:
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
        else:
            query = f"SHOW COLUMNS FROM {table}"

        cursor = self.mssql_cursor if is_source else self.mysql_cursor
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def fetch_data_chunk(self, columns, offset):
        column_list = ", ".join(columns)
        query = f"SELECT {column_list} FROM {self.source_table} ORDER BY (SELECT NULL) OFFSET {offset} ROWS FETCH NEXT {self.chunk_size} ROWS ONLY"
        self.mssql_cursor.execute(query)
        return self.mssql_cursor.fetchall()

    def map_columns(self, source_row):
        target_row = []
        for source_col, target_col in self.column_mapping.items():
            if source_col in self.default_values:
                # If the column is missing in the source but has a default value, use it
                target_row.append(self.default_values[source_col])
            else:
                # Otherwise, map the source column to the target column
                source_index = self.mssql_cursor.description.index((source_col,))
                target_row.append(source_row[source_index])
        return tuple(target_row)

    def insert_data(self, rows):
        columns = ", ".join(self.column_mapping.values())
        placeholders = ", ".join(["%s"] * len(self.column_mapping))
        insert_query = f"INSERT INTO {self.target_table} ({columns}) VALUES ({placeholders})"
        self.mysql_cursor.executemany(insert_query, rows)
        self.mysql_conn.commit()

    def migrate(self):
        source_columns = self.fetch_columns(self.source_table, is_source=True)
        offset = 0

        while True:
            rows = self.fetch_data_chunk(source_columns, offset)
            if not rows:
                break  # No more data to fetch

            mapped_rows = [self.map_columns(row) for row in rows]
            self.insert_data(mapped_rows)
            print(f"✅ Inserted {len(rows)} rows from {self.source_table} to {self.target_table}.")
            offset += self.chunk_size

        print("✅ Migration completed!")

    def close_connections(self):
        self.mssql_cursor.close()
        self.mssql_conn.close()
        self.mysql_cursor.close()
        self.mysql_conn.close()


def migrate(migration_func):
    # Run the given migration function
    migration_func()
