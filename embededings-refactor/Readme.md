# RAG (Retrieval-Augmented Generation) System

This project implements a Retrieval-Augmented Generation (RAG) system using Python, Redis, and the Ollama API. The system processes documents, generates embeddings, performs similarity searches, and answers questions based on the retrieved context.

Inspiration and credits:
https://www.youtube.com/watch?v=aGwb1KLmtog&t=513s&ab_channel=MattWilliams

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Code Structure](#code-structure)
7. [Recommendations](#recommendations)

## Features

- Document processing and chunking
- Embedding generation using multiple models
- Vector storage and similarity search using Redis
- Question answering using a language model
- Configurable via YAML file

## Requirements

- Python 3.7+
- Redis
- Ollama API
- BeautifulSoup4
- NLTK
- Pydantic
- PyYAML

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/rag-system.git
   cd rag-system
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Install and start Redis on your local machine.

4. Set up Ollama and ensure it's accessible via API.

## Configuration

Configure the system by editing the `config/config.yaml` file:

```yaml
embed_models:
  - "model1"
  - "model2"
main_model: "main-model"
source_doc_url: "https://example.com/document"
chunk_size: 500
questions:
  - "What is the main topic of the document?"
  - "Summarize the key points."
```

- `embed_models`: List of embedding models to use
- `main_model`: Main language model for question answering
- `source_doc_url`: URL of the document to process
- `chunk_size`: Maximum size of text chunks
- `questions`: List of questions to ask about the document

## Usage

Run the main script:

```
python main.py
```

The system will:
1. Load the configuration
2. Fetch and process the document
3. Generate embeddings and store them in Redis
4. Perform similarity searches for each question
5. Generate answers using the main language model
6. Log the results

Check the `logs/app.log` file for detailed output.

## Code Structure

- `config.py`: Configuration management using Pydantic
- `document_processor.py`: Document fetching and processing
- `model_manager.py`: Handling of models, embeddings, and Redis operations
- `main.py`: Main execution script

## Recommendations

1. **Security**: Implement proper authentication and encryption for Redis in production environments.

2. **Scalability**: Consider using Redis Cluster for larger datasets and higher throughput.

3. **Error Handling**: Implement more robust error handling and retries, especially for network operations.

4. **Monitoring**: Set up proper monitoring and alerting for the application and Redis instance.

5. **Caching**: Implement caching mechanisms to avoid redundant embedding calculations.

6. **Performance Tuning**: Profile the application and optimize bottlenecks, especially for large documents or high query volumes.

7. **Testing**: Implement unit tests and integration tests to ensure system reliability.

8. **Documentation**: Keep the documentation up-to-date, especially if you extend the system's functionality.

9. **Containerization**: Consider using Docker to containerize the application for easier deployment and scaling.

10. **Asynchronous Processing**: Implement asynchronous processing for document fetching and embedding generation to improve performance.

11. **Rate Limiting**: Implement rate limiting for API calls to Ollama to prevent overloading.

12. **Logging**: Implement structured logging and consider using a centralized logging system for better observability in production.

Remember to regularly update dependencies and review the latest best practices in RAG systems and vector databases to keep your system up-to-date and efficient.