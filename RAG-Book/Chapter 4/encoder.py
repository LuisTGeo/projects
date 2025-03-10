from sentence_transformers import SentenceTransformer
import torch
import pandas as pd

# This model ouput is 384 dimensional ( array length)
model = SentenceTransformer("all-MiniLM-L6-v2")

if torch.cuda.is_available():
    model = model.to('cuda')
    print("CUDA is available. The model has been moved to GPU.")
else:
    print("CUDA is not available. The model will run on CPU.")

df = pd.read_csv("hotel_datasets_train.csv")
df_paris = df.loc[df.locality == 'Paris']
print(df_paris.head())

reviews = df_paris['review_text'].tolist()

review_embeddings = model.encode(reviews, show_progress_bar=True)

print(f"Embeddings shape: {review_embeddings.shape}")