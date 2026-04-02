# Financial-Analyst — Financial Document Intelligence

A RAG-based AI assistant that answers questions about financial documents with cited sources.

## What it does
- Upload any 10-K filing or financial PDF
- Ask questions in plain English
- Get precise answers with page citations
- Powered by LLaMA 3.3 70B via Groq

## Tech Stack
- **LLM:** LLaMA 3.3 70B via Groq API
- **Embeddings:** Sentence Transformers
- **Vector Store:** ChromaDB
- **PDF Parsing:** PyPDF
- **Frontend:** Streamlit
- **Architecture:** RAG (Retrieval Augmented Generation)

## How RAG works here
1. PDF is parsed and split into overlapping chunks
2. Each chunk is embedded into a vector using sentence-transformers
3. User question is embedded the same way
4. Cosine similarity finds the top-5 most relevant chunks
5. Those chunks + question are sent to LLaMA 3.3
6. LLM generates answer using only retrieved context — no hallucination

## Live Demo
[Try it here](https://rtlufbajszzfux6b2ne8yn.streamlit.app/)
