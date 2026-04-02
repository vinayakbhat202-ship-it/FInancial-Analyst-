from dotenv import load_dotenv
load_dotenv()
import os
from query import query_collection
from groq import Groq

def answer_question(question: str, collection_name: str) -> dict:
    chunks = query_collection(question, collection_name, n_results=5)
    
    context = ""
    for i, chunk in enumerate(chunks, 1):
        context += f"[Page {chunk['page']}]\n{chunk['text']}\n\n"
    
    prompt = f"""You are a financial analyst assistant. Answer the question using ONLY the context below.
Always cite which page your answer comes from.

Context:
{context}

Question: {question}

Answer:"""
    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {
        "answer": message.choices[0].message.content,
        "sources": chunks
    }

if __name__ == "__main__":
    result = answer_question("What were Apple's total revenues?", "apple_10k")
    print(result["answer"])
    print("\nSources used:")
    for s in result["sources"]:
        print(f"  - Page {s['page']} (score: {s['score']})")