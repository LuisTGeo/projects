import sys, chromadb, ollama

chromaclient = chromadb.HttpClient(host="localhost", port=8000)
collection = chromaclient.get_or_create_collection(name="buildragwithpython")


def main(query):
    # query = " ".join(sys.argv[1:])
    #
    print("query ---- ", query)
    queryembed = ollama.embed(model="nomic-embed-text", input=query)['embeddings']

    relateddocs = '\n\n'.join(collection.query(query_embeddings=queryembed, n_results=10)['documents'][0])

    prompt = f"{query} - Answer that question using the following text as a resource: {relateddocs}"

    noragoutput = ollama.generate(model="llama3.2", prompt=query, stream=False)

    print(f"Answered without RAG: {noragoutput['response']}")

    print("---")
    ragoutput = ollama.generate(model="llama3.2", prompt=prompt, stream=False)

    print(f"Answered with RAG: {ragoutput['response']}")


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    query = query if query else "How ollama works"
    main(query)
