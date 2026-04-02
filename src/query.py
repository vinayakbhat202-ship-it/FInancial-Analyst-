from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent.parent / "db"
MODEL_NAME = "all-MiniLM-L6-v2"

client = chromadb.PersistentClient(path=str(DB_PATH))
embedder = SentenceTransformer(MODEL_NAME)

def query_collection(question: str, collection_name: str, n_results: int = 5):
    collection = client.get_collection(name=collection_name)
    
    query_embedding = embedder.encode([question]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    
    formatted = []
    for chunk, meta, dist in zip(chunks, metadatas, distances):
        formatted.append({
            "text": chunk,
            "page": meta["page"],
            "source": meta["source"],
            "score": round(1 - dist, 4)
        })
    
    return formatted

if __name__ == "__main__":
    question = "What were Apple's total revenues?"
    collection_name = "apple_10k"
    
    results = query_collection(question, collection_name)
    
    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} (Page {r['page']}, Score: {r['score']}) ---")
        print(r["text"][:300])

