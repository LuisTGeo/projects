from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Constants
PROJECT_ID = "postgres"  # Replace with your project ID
DATABASE_URL = f"postgresql://postgres:mysecretpassword@localhost:5432/{PROJECT_ID}"  # Replace with your DB credentials


# Initialize database engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Create the database and table
def create_database():
    Base.metadata.create_all(engine)
    print(f"Created in database.")


# Load DataFrame to PostgreSQL
def load_dataframe_to_postgresql(df: pd.DataFrame, table_name: str):
    session = Session()
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Data loaded into {table_name} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


# Main function to execute the code
def load_postgresql_from_csv(table_name: str, csv_path: str = "../../hotel_datasets_train.csv"):
    create_database()
    # ../../ hotel_datasets_train.csv
    # Load the dataset from the CSV file
    df = pd.read_csv(csv_path)
    # Drop rows with missing values
    df = df.dropna()
    # Print the shape of the DataFrame
    print(df.shape)
    # Add a new column 'id' based on the DataFrame index
    df["id"] = df.index + 1
    # Display the updated DataFrame
    print(df)
    load_dataframe_to_postgresql(df, table_name=table_name)


if __name__ == "__main__":
    TABLE_NAME = "hotel_data"
    load_postgresql_from_csv(table_name=TABLE_NAME)
