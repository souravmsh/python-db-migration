from utils.migrator import Migrator
from datetime import datetime

query_chunk_size = 100
source_table = "Temp_Email"
source_query = f"SELECT * FROM {source_table}"
destination_table = 'subscriptions'

def prepare_data(row):
    # Modify the row for migration
    return {
        'id': row['MerchantBankerID'],
        'name': row['MerchantBankerName'],
        'bo_prefix': "00",
        'master_code': row['MasterAccount'],
        'client_alias': row['ClientAlias'],
        'master_boid': row['MasterBOID'],
        'contact_person_name': row['ContactPerson'] if row['ContactPerson'] else 'N/A',
        'contact_person_number': row['Cellphone'] if row['Cellphone'] else 'N/A',
        'address': row["Address"],
        'cell_phone': row["OfficePhone"],
        'email': row["Email"],
        'default_commission': row['MBankDefaultCommission'],
        'management_fee': 0,
        'interest_rate': 0,
        'status': 'Active'
    }

def Bank(): 
    # Initialize the migration service
    migrator = Migrator()
    # Truncate the destination table before inserting new data
    migrator.truncate(destination_table)
    
    # Print chunk size and table information
    print(f"✅ Query Chunk Size: {query_chunk_size}")
    print(f"✅ Source Table: {source_table}")
    
    # In the real method, you'd fetch columns from source and destination tables.
    # Here we're simulating the column fetch
    print(f"✅ Destination Table: {destination_table}")
    
    # Run the source query to count the available rows
    source_data_count = migrator.count_rows(source_query)
    print(f"✅ Total Rows in Source Table: {source_data_count}")
    
    # Perform the migration in chunks
    migrator.migrate(
        source_query, 
        destination_table, 
        prepare_data,  # Pass the prepare_data function (closure method)
        query_chunk_size
    )
