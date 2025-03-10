
import pandas as pd

# Load the dataset from the CSV file
df = pd.read_csv("hotel_datasets_train.csv")

# Drop rows with missing values
df = df.dropna()

# Select the first 2 rows
df = df.head(2)

# Print the shape of the DataFrame
print(df.shape)

# Display the first few rows of the DataFrame
print(df.head())

# Add a new column 'id' based on the DataFrame index
df["id"] = df.index + 1

# Display the updated DataFrame
print(df)
