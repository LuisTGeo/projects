import nltk  # A

nltk.download('punkt')
from nltk.tokenize import word_tokenize
import math

examples = [
    "The cat is playing in the garden",  # B
    "A dog and a cat are good pets",
    "Cats love to chase mice",
    "Machine learning is based on algorithms",
    "Deep learning uses neural networks",
    "Recurrent networks have connections"
]

tokenized_docs = [word_tokenize(d) for d in examples]  # C

index = {}  # D

for i, doc in enumerate(tokenized_docs):
    for word in doc:
        if word not in index:
            index[word] = []
        index[word].append(i)

print(f'Inverted Index:\n {index}')


def tfidf(word, id):  # A

    tf = tokenized_docs[id].count(word)  # B
    df = len(index[word]) if word in index else 0  # C
    idf = math.log(len(examples) / (df + 1))  # D

    return tf * idf



