from sqlalchemy import create_engine, inspect

# Constants
PROJECT_ID = "postgres"  # Replace with your project ID
DATABASE_URL = f"postgresql://postgres:mysecretpassword@localhost:5432/{PROJECT_ID}"  # Replace with your DB credentials
TABLE_NAME = "hotel_data"
# Initialize database engine
engine = create_engine(DATABASE_URL)


# Function to get table schema using SQLAlchemy Inspector
def get_table_schema(engine, table_name):
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    print(f"Schema for table '{table_name}':")
    for column in columns:
        print(f"Column: {column['name']}, Type: {column['type']}")


# Get schema for the specified table
get_table_schema(engine, TABLE_NAME)
