from utils.migrator import Migrator
from datetime import datetime

query_chunk_size = 100
source_table = "Temp_Email"
source_query = f"SELECT * FROM {source_table}"
destination_table = 'subscriptions'

# Modify the row for migration
def prepare_data(row):
    return {
        # 'id': row['MerchantBankerID'],
        'client_code': 'XYZ' + row['Investor_Code'],
        'email': row['e-mail'],
        'status': 'Active',
        'updated_by': row['approved_by'],
        'created_at': row['approved_dt'],
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

def subscription(): 
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
    subscription()
