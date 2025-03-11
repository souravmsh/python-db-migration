# migrations/tables/Bank.py

from app.migrations.process import Migrate

# Define the column mapping for the Bank table migration
column_mapping = {
    'investor_column1': 'bank_column1',
    'investor_column2': 'bank_column2',
    # Add the column mappings here
}

def migrate_bank():
    # Initialize migration for the Bank table
    bank_migration = Migrate('investor', 'bank', column_mapping)
    bank_migration.migrate()
    bank_migration.close_connections()
