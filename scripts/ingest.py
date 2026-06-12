import os
import chromadb
from sentence_transformers import SentenceTransformer

# =========================================================
# 1. MODEL
# =========================================================
print("🚀 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================================
# 2. PATHS (FIXED ABSOLUTE PATHS)
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "documents")
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

print("📁 DATA PATH:", DATA_PATH)
print("📁 CHROMA PATH:", CHROMA_PATH)

# =========================================================
# 3. CHROMA DB INIT
# =========================================================
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="university_docs")

print("✅ ChromaDB ready")

# =========================================================
# 4. CHECK FILES
# =========================================================
if not os.path.exists(DATA_PATH):
    print("❌ Documents folder not found")
    exit()

files = [f for f in os.listdir(DATA_PATH) if f.endswith(".md")]

if not files:
    print("❌ No markdown files found")
    exit()

print("\n📂 Files found:", files)

# =========================================================
# 5. BETTER CHUNKING (sentence-safe)
# =========================================================
def chunk_text(text, chunk_size=800, overlap=150):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# =========================================================
# 6. INGESTION
# =========================================================
total_chunks = 0

for file in files:
    file_path = os.path.join(DATA_PATH, file)

    print("\n" + "=" * 60)
    print("📄 Processing:", file)
    print("=" * 60)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        print("⚠️ Empty file skipped")
        continue

    chunks = chunk_text(text)

    print("🧩 Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks):

        # EMBEDDING
        vector = model.encode(chunk).tolist()

        doc_id = f"{file}_{i}"

        # STORE IN CHROMA
        collection.add(
            ids=[doc_id],
            embeddings=[vector],
            documents=[chunk],
            metadatas=[{
                "file": file,
                "chunk_index": i
            }]
        )

        total_chunks += 1

        if i < 2:
            print("\n--- PREVIEW ---")
            print(chunk[:250])
            print("Vector size:", len(vector))

# =========================================================
# 7. FINAL STATUS
# =========================================================
print("\n✅ INGESTION COMPLETE")
print("Total chunks stored:", total_chunks)
print("ChromaDB path:", CHROMA_PATH)