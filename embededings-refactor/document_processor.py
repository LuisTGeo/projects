# document_processor.py
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize

class DocumentProcessor:
    """Handles fetching and processing of documents."""

    def __init__(self, doc_url: str, chunk_size: int):
        self.doc_url = doc_url
        self.chunk_size = chunk_size

    def fetch_document(self) -> str:
        """Fetch the document from the provided URL."""
        response = requests.get(self.doc_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)

    def process_document(self) -> list[str]:
        """Fetch and process document into chunks."""
        html_content = self.fetch_document()
        return self.split_text_into_chunks(html_content)

    # @staticmethod
    def split_text_into_chunks(self, text: str) -> list[str]:
        """Split text into chunks of specified maximum length."""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(word_tokenize(sentence))
            if current_length + sentence_length > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks