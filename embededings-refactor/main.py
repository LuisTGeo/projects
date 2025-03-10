# main.py
import asyncio
import logging

import yaml

from config import Config
from document_processor import DocumentProcessor
from model_manager import ModelManager
import redis

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



def load_config(path: str = "config/config.yaml") -> dict:
    """Load YAML configuration."""
    with open(path, "r") as f:
        return yaml.safe_load(f)

async def main():
    # Load configuration
    # config = Config.from_yaml()
    config = load_config()
    # Initialize Redis client
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # Initialize document processor and process document # it is just one url document
    doc_processor = DocumentProcessor(config["source_doc_url"], config["chunk_size"])
    source_doc_chunks = doc_processor.process_document()

    # Initialize model manager and pull required models
    model_manager = ModelManager(config["embed_models"], config["main_model"], redis_client)
    model_manager.pull_models()

    # Process each embedding model
    for embed_model in config["embed_models"]:
        model_manager.add_items(source_doc_chunks, embed_model)
        model_manager.create_redis_index(embed_model)

        # Process each question
        for question in config["questions"]:
            question_embedding = model_manager.get_embedding([question], embed_model)
            results = model_manager.similarity_search(question_embedding, embed_model, k=10,
                                                      return_fields=("score", "text"))
            context = "\n\n---\n".join(result.text for result in results.docs)
            answer = model_manager.ask_question(question, context)

            # Log results
            logging.info(f"Embed Model: {embed_model}")
            print(f"Embed Model: {embed_model}")
            #
            logging.info(f"Question: {question}")
            print(f"Question: {question}")
            #
            logging.info(f"Answer: {answer}")
            print(f"Answer: {answer}")
            #
            logging.info(f"Scores: {', '.join([f'{float(result.score):.2f}' for result in results.docs])}")
            print(f"Scores: {', '.join([f'{float(result.score):.2f}' for result in results.docs])}")
            #
            logging.info("---")
            print("---")
            logging.info("---")


if __name__ == "__main__":
    asyncio.run(main())