from utils.migrator import Migrator
from datetime import datetime
from utils.config import config

query_chunk_size = 2
source_table = "TERMINAL_INFO"
destination_table = 'trading_work_stations'
source_query = f"SELECT ti.*, bi.BRANCH_NAME FROM TERMINAL_INFO ti LEFT JOIN BRANCH_INFO bi ON ti.BRANCH_CD = bi.BRANCH_CD"

def get_exchange(exchange):
    if exchange == 1:
        return "CSE"
    else:
        return "DSE"

# Modify the row for migration
def prepare_data(row):
    return {
        'terminal_name': row['TERMINAL_CD'],
        'branch_id': row['BRANCH_CD'],
        'branch_name': row['BRANCH_NAME'],
        'exchange_id': get_exchange(1),
        'trader_name': row['USER_ID'],
        'status': 'Active',
        'created_at': row['EFFECT_FDT'],
        'updated_at': row['ACTION_DT'],
        'ref_no': config.reference_id,
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
