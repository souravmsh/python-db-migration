from utils.migrator import Migrator
from datetime import datetime

query_chunk_size = 100
source_table = 'subscriptions'
source_query = f"SELECT * FROM {source_table}"
destination_table = "subscriptions_temp"

# Modify the row for migration
def prepare_data(row):
    return {
        'id': row['id'],
        'client_code': row['client_code'],
        'email': row['email'],
        'status': row['status'],
        'updated_by': row['updated_by'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }

def sample_migrate(): 
    # Initialize the migration service
    migrator = Migrator()
    # Truncate the destination table before inserting new data
    migrator.truncate(destination_table)
    # Perform the migration in chunks
    migrator.migrate(
        source_table, 
        source_query, 
        destination_table, 
        prepare_data,  # Pass the prepare_data function (closure method)
        query_chunk_size
    )

if __name__ == "__main__":
    sample_migrate()
