import redis
import numpy as np
from sentence_transformers import SentenceTransformer


# Connect to Redis
def connect_redis(host='localhost', port=6379, db=0):
    return redis.StrictRedis(host=host, port=port, db=db)


# Initialize the Redis connection
redis_client = connect_redis()

print("connected")

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Create a function to convert text to vectors
def text_to_vector(text):
    # Generate embeddings (vectors) for the input text
    return model.encode(text)

# Function to push vectors to Redis
def push_vector_to_redis(redis_client, vector, key):
    # Convert each float to a string before storing
    redis_client.hset(key, mapping={str(i): str(val) for i, val in enumerate(vector)})


# Example text to be vectorized and stored
text = "Redis is a powerful in-memory data structure store"
vector = text_to_vector(text)

# Store the vector in Redis with a unique key (e.g., "text:1")
push_vector_to_redis(redis_client, vector, "text:1")

print(f"Vector for text '{text}' pushed to Redis with key 'text:1'")


# Function to retrieve vectors from Redis
def get_vector_from_redis(redis_client, key):
    # Retrieve the hash map from Redis and convert it back to a list of floats
    vector = redis_client.hgetall(key)
    # Sort and convert the values back to float
    sorted_vector = [float(vector[str(i).encode('utf-8')]) for i in range(len(vector))]
    return np.array(sorted_vector)


# Retrieve the vector stored under the key "text:1"
retrieved_vector = get_vector_from_redis(redis_client, "text:1")
print(f"Retrieved vector: {retrieved_vector}")
