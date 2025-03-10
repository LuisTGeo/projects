import pandas as pd
import sqlite3

import pandas as pd
import sqlite3


def csv_to_sqlite(csv_file, db_name, table_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Connect to the SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Infer the schema based on the DataFrame columns and data types
    def create_table_from_df(df, table_name):
        # Get column names and types
        col_types = []
        for col in df.columns:
            dtype = df[col].dtype
            if dtype == 'int64':
                col_type = 'INTEGER'
            elif dtype == 'float64':
                col_type = 'REAL'
            else:
                col_type = 'TEXT'
            col_types.append(f'"{col}" {col_type}')

        # Create the table schema
        col_definitions = ", ".join(col_types)
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({col_definitions});'
        # print(create_table_query)

        # Execute the table creation query
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created with schema: {col_definitions}")

    # Create table schema
    create_table_from_df(df, table_name)

    # Insert CSV data into the SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()
    print(f"Data loaded into '{table_name}' table in '{db_name}' SQLite database.")



if __name__ == "__main__":
    csv_file = "emissions_metrics.csv"
    db_name = "emissions_metrics_db.db"
    table_name = "emissions_metrics"
    csv_to_sqlite(csv_file, db_name, table_name)
