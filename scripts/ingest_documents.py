import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "documents")
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "vector_store")

def main():
    print("Loading documents...")
    # FIXED: The university policy files are .md, not .txt!
    loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()

    print(f"Loaded {len(documents)} documents.")

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print(f"Split into {len(chunks)} chunks.")

    print("Initializing Embeddings and ChromaDB...")
    # Using HuggingFace embeddings instead of OpenAI so you don't need a paid API key!
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print("Ingestion complete! Database saved to data/vector_store/")

if __name__ == "__main__":
    main()
