import os
import re
from pathlib import Path
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer, util

DB_PATH = Path(__file__).parent.parent / "db"
MODEL_NAME = "all-MiniLM-L6-v2"

client = chromadb.PersistentClient(path=str(DB_PATH))
embedder = SentenceTransformer(MODEL_NAME)

def chunk_text(text, similarity_threshold=0.55, max_chunk_words=500, min_chunk_words=40):
    """Semantic chunking: split into sentences, embed each one, and only
    start a new chunk when the topic actually shifts — instead of cutting
    every fixed N words regardless of what's being talked about."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 1:
        return [text.strip()] if text.strip() else []

    # Embed every sentence once, in a single batch
    sentence_embeddings = embedder.encode(sentences, convert_to_tensor=True)

    chunks = []
    current_sentences = [sentences[0]]
    current_word_count = len(sentences[0].split())

    for i in range(1, len(sentences)):
        similarity = util.cos_sim(sentence_embeddings[i - 1], sentence_embeddings[i]).item()
        sentence_word_count = len(sentences[i].split())

        topic_changed = similarity < similarity_threshold
        chunk_too_big = current_word_count + sentence_word_count > max_chunk_words

        if chunk_too_big or (topic_changed and current_word_count >= min_chunk_words):
            chunks.append(" ".join(current_sentences))
            current_sentences = [sentences[i]]
            current_word_count = sentence_word_count
        else:
            current_sentences.append(sentences[i])
            current_word_count += sentence_word_count

    if current_sentences:
        chunks.append(" ".join(current_sentences))

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

