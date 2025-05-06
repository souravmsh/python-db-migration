from utils.migrator import Migrator
from datetime import datetime

query_chunk_size = 100
source_table = 'SE_CLIENT'
source_query = f"SELECT * FROM {source_table}"
destination_table = "clients"

# Modify the row for migration
def prepare_data(row):

    mobile = str(row['TEL_NO'])[-11:] if row['TEL_NO'] else None
    current_dt = datetime.now()
    
    return {
        'name': row['CLIENT_NAME'],
        'client_code': row['CLIENT_CODE'],
        'boid': row['BO_ACCOUNT'],
        'mobile': mobile,
        'email': row['E_MAIL'] if row['E_MAIL'] else None,
        'bank_name': row['BANK_INFO'] if row['BANK_INFO'] else None,
        'bank_account': row['BANK_ACNO'] if row['BANK_ACNO'] else None,
        'status': row['STATUS'] if row['STATUS'] else 'Active',
        'created_at': row['ACTION_DT'] or current_dt,
        'updated_at': row['CDBL_SETUPDT'] or current_dt,
    }

def client(): 
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
    client()
