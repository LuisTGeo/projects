from langchain.document_loaders import DirectoryLoader, CSVLoader, UnstructuredWordDocumentLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from sentence_transformers import SentenceTransformer, util
#from htmlTemplate import css, bot_template, user_template
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_huggingface import HuggingFaceEmbeddings

file_directory="data_directory"
embedding_model='sentence-transformers/all-MiniLM-L6-v2'
llm_model ="llama3.2"


def prepare_and_split_docs(directory):
    # Load the documents
    loaders = [
        DirectoryLoader(directory, glob="**/*.pdf",show_progress=True, loader_cls=PyPDFLoader),
        DirectoryLoader(directory, glob="**/*.docx",show_progress=True),
        DirectoryLoader(directory, glob="**/*.csv",loader_cls=CSVLoader)
    ]


    documents=[]
    for loader in loaders:
        data =loader.load()
        documents.extend(data)

    # Initialize a text splitter
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,  # Use the smaller chunk size here to avoid repeating splitting logic
        chunk_overlap=256,
        disallowed_special=(),
        separators=["\n\n", "\n", " "]
    )

    # Split the documents and keep metadata
    split_docs = splitter.split_documents(documents)

    print(f"Documents are split into {len(split_docs)} passages")
    return split_docs