import numpy as np
import scipy.spatial
from sentence_transformers import SentenceTransformer
import torch
import pandas as pd

def cosine_search(query_embedding, review_embeddings, k):
    query_embedding = query_embedding.reshape(-1)  # A “#A Reshape the query embedding to have a shape of (768,)
    dot_products = np.dot(review_embeddings, query_embedding)  #B Compute the dot product between the query embedding and all review embeddings

    query_norm = np.linalg.norm(query_embedding)  #C Normalize the query and documents (review_embeddings)
    review_norms = np.linalg.norm(review_embeddings, axis=1)

    cosine_similarities = dot_products / (query_norm * review_norms)  #D Compute the cosine similarity scores

    top_indices = np.argsort(-cosine_similarities)[:k]  #E Get the indices of the top-k highest cosine similarity scores
    top_cosine_similarities = cosine_similarities[top_indices]  #F Get the cosine similarity scores of the top-k similar reviews”

    return top_indices, top_cosine_similarities

model = SentenceTransformer("all-MiniLM-L6-v2")

if torch.cuda.is_available():
    model = model.to('cuda')
    print("CUDA is available. The model has been moved to GPU.")
else:
    print("CUDA is not available. The model will run on CPU.")

df = pd.read_csv("hotel_datasets_train.csv")
df_paris = df.loc[df.locality == 'Paris']

reviews = df_paris['review_text'].tolist()

review_embeddings = model.encode(reviews, show_progress_bar=True)