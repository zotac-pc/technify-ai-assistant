import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'documents')
DB = os.path.join(os.path.dirname(__file__), '..', 'data', 'vector_store')
def main():
    print('Loading documents...')
    loader = DirectoryLoader(DATA, glob='**/*.md', loader_cls=TextLoader,
         loader_kwargs={'encoding': 'utf-8'})
    docs = loader.load()
    print(f'Loaded {len(docs)} docs.')
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f'Split into {len(chunks)} chunks.')
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    Chroma.from_documents(documents=chunks, embedding=embeddings,
        persist_directory=DB)
    print('Done! Saved to data/vector_store/')
if __name__ == '__main__': main()