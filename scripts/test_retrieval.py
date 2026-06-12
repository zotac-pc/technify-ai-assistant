import chromadb
from sentence_transformers import SentenceTransformer

print("🔍 Retrieval Test Started")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("university_docs")

# Query
query = "attendance policy"
print("\nQUERY:", query)

# Convert query into vector
query_vector = model.encode(query).tolist()

# Search in ChromaDB
results = collection.query(
    query_embeddings=[query_vector],
    n_results=3
)

# Print results
print("\nTOP MATCHES:\n")

for i, doc in enumerate(results["documents"][0]):
    print(f"Result {i+1}")
    print(doc)
    print("-" * 50)