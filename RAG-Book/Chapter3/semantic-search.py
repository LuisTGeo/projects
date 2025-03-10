from sentence_transformers import SentenceTransformer
import scipy.spatial

import pandas as pd

examples = [  #A
    "The cat is playing in the garden",
    "A dog and a cat are good pets",
    "Cats love to chase mice",
    "Machine learning is based on algorithms",
    "Deep learning uses neural networks",
    "Recurrent networks have connections"]

model = SentenceTransformer('all-MiniLM-L6-v2')
print(model)

embeddings = model.encode(examples)
embeddings.shape


def semantic_search(query, embeddings, examples):
    query_embedding = model.encode(query)  # A

    scores = [scipy.spatial.distance.cosine(query_embedding, doc) for doc in embeddings]  # B

    for i, doc in enumerate(examples):  # C
        print(f"Example {i}: {examples[i]}")
        print(f"Score: {1 - scores[i]:.4f}")

    print("Most similar example:", examples[scores.index(min(scores))])


semantic_search("Machine learning", embeddings, examples)