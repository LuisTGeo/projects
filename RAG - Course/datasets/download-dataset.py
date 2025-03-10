from datasets import load_dataset
import pandas as pd

# Load the dataset
# dataset = load_dataset("traversaal-ai-hackathon/hotel_datasets")
dataset = load_dataset("traversaal-ai-hackathon/hotel_datasets")

# Check the type and length of the training dataset
print(type(dataset))
print(len(dataset["train"]))

# Convert the training dataset to a pandas DataFrame
train_df = pd.DataFrame(dataset["train"])

# Save the DataFrame to a CSV file
train_df.to_csv("hotel_datasets_train.csv", index=False)

print("Dataset saved to hotel_datasets_train.csv")
