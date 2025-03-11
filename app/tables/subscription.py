from utils.migrate import Migrate
from datetime import datetime

source_table = 'Temp_Email'
destination_table = 'subscriptions'
query_chunk_size = 100

column_mapping = {
    'Investor_Code': 'client_code',
    'e-mail': 'email',
    # 'approved_by': 'updated_by',
    'approved_dt': 'created_at',
}

extra_columns = {
    'status': 'Active',
    'updated_by': 1,
    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

def Subscription(): 
    process = Migrate(source_table, destination_table, column_mapping, extra_columns, query_chunk_size)
    process.migrate()
    process.close_connections()
