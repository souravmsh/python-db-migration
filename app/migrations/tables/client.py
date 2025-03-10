from migrations.migrate import Migrate

# Define the column mapping for the Client table
column_mapping = {
    'investor_column1': 'client_column1',
    'investor_column2': 'client_column2',
    # Add the column mappings here
}

# Define default values for columns that are not present in the source table
default_values = {
    'client_column3': 'default_value',  # This column will be filled with 'default_value' if it's not in the source
}

def client():
    # Initialize migration for the Client table
    client_migration = Migrate('investor', 'client', column_mapping, default_values)
    client_migration.migrate()
    client_migration.close_connections()
