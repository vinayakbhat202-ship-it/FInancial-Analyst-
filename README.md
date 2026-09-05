Financial-Analyst — Financial Document Intelligence

A RAG-based AI assistant that answers questions about financial documents with cited sources.

What it does
Upload any 10-K filing or financial PDF
Ask questions in plain English
Get precise answers with page citations
Powered by GPT-OSS 120B via Groq
Tech Stack
LLM: GPT-OSS 120B via Groq API
Embeddings: Sentence Transformers
Vector Store: ChromaDB
PDF Parsing: PyPDF
Frontend: Streamlit
Architecture: RAG (Retrieval Augmented Generation)
How RAG works here
PDF is parsed and split into overlapping chunks
Each chunk is embedded into a vector using sentence-transformers
User question is embedded the same way
Cosine similarity finds the top-5 most relevant chunks
Those chunks + question are sent to GPT-OSS 120B
LLM generates answer using only retrieved context — no hallucination
Live Demo

Try it here

## Live Demo
[Try it here](https://rtlufbajszzfux6b2ne8yn.streamlit.app/)
