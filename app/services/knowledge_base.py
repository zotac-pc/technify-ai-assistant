import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'vector_store')

def query_knowledge_base(query: str) -> str:
    if not os.path.exists(DB): return 'Knowledge base not initialized.'
    emb = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    db = Chroma(persist_directory=DB, embedding_function=emb)
    docs = db.similarity_search(query, k=3)
    return '\n\n'.join([d.page_content for d in docs])
