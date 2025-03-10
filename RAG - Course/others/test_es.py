from elasticsearch import Elasticsearch

# Connect to the Elasticsearch instance (e.g., running locally on port 9200)
# Elasticsearch credentials
username = "elastic"
password = "X75eZVaxvPg=5eXc7Q*s"

# Connect to Elasticsearch using HTTPS and basic authentication
es = Elasticsearch(
    "https://localhost:9200",  # Use your Elasticsearch URL
    http_auth=(username, password),  # Basic Authentication
    verify_certs=False,  # Disable SSL verification for self-signed certificates (adjust for production)
    ssl_show_warn=False
)
# "https://localhost:9200"
# Step 1: Create a small index
index_name = 'dummy_data_index'
index_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "age": {"type": "integer"},
            "email": {"type": "keyword"}
        }
    }
}

# Check if the index already exists, if not, create it
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists.")

# Step 2: Populate the index with some dummy data
dummy_data = [
    {"name": "Luis Torres", "age": 34, "email": "luis.torres@example.com"},
    {"name": "Jane Doe", "age": 28, "email": "jane.doe@example.com"}
]

# Insert the documents one by one
for i, doc in enumerate(dummy_data, start=1):
    es.index(index=index_name, id=i, body=doc)
    print(f"Inserted document {i}: {doc}")

# Step 3: Verify the inserted data by searching the index
response = es.search(index=index_name, body={"query": {"match_all": {}}})
print("Data from the index:")
for hit in response['hits']['hits']:
    print(hit['_source'])
