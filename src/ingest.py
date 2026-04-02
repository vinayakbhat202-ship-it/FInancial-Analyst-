import os
from pathlib import Path
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent.parent / "db"
MODEL_NAME = "all-MiniLM-L6-v2"

client = chromadb.PersistentClient(path=str(DB_PATH))
embedder = SentenceTransformer(MODEL_NAME)

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest_pdf(pdf_path: str, collection_name: str):
    print(f"Reading {pdf_path}...")
    reader = PdfReader(pdf_path)
    
    all_chunks = []
    all_metadata = []
    
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text or len(text.strip()) < 50:
            continue
        
        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadata.append({
                "page": page_num,
                "source": Path(pdf_path).name
            })
    
    print(f"Total chunks created: {len(all_chunks)}")
    print("Embedding chunks... (this takes 1-2 minutes)")
    
    embeddings = embedder.encode(all_chunks, show_progress_bar=True)
    
    collection = client.get_or_create_collection(name=collection_name)
    
    collection.add(
        documents=all_chunks,
        embeddings=embeddings.tolist(),
        metadatas=all_metadata,
        ids=[f"{collection_name}_chunk_{i}" for i in range(len(all_chunks))]
    )
    
    print(f"Done. {len(all_chunks)} chunks stored in collection '{collection_name}'")
    return collection

if __name__ == "__main__":
    pdf_path = str(Path(__file__).parent.parent / "data" / "apple_10k.pdf")
    collection_name = "apple_10k"
    ingest_pdf(pdf_path, collection_name)


