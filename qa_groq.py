import os#
import json
from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS  # Changed import
from sentence_transformers import SentenceTransformer
import numpy as np

# Load API key
load_dotenv()
client = Groq()

# Load notes
if os.path.exists("notes.json"):
    with open("notes.json", "r") as f:
        notes = json.load(f)
else:
    print("No notes.json found. Run notes.py first to add notes.")
    exit()

# Extract note texts
note_texts = []
for note in notes:
    if isinstance(note, dict):
        note_texts.append(note.get("text", ""))
    else:
        note_texts.append(str(note))

print(f"Loading AI model for semantic search...")
model = SentenceTransformer('all-MiniLM-L6-v2')
note_embeddings = model.encode(note_texts)
print(f"Ready with {len(note_texts)} notes")

def semantic_search(question, texts, embeddings, model, top_k=2, threshold=0.2):
    """Find notes by meaning, not keywords"""
    q_emb = model.encode([question])[0]
    
    similarities = []
    for text_emb in embeddings:
        sim = np.dot(q_emb, text_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(text_emb))
        similarities.append(sim)
    
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        if similarities[idx] >= threshold:
            results.append({
                "text": texts[idx],
                "similarity": similarities[idx]
            })
    return results

def web_search(query):
    """Search the web and return top result"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                return results[0]['body']
            return "No results found"
    except Exception as e:
        return f"Search error: {str(e)}"

print("\n" + "="*50)
print("Ask questions about your notes. Type 'quit' to exit.")
print("="*50)

while True:
    question = input("\n❓ Your question: ")
    
    if question.lower() == 'quit':
        break
    
    # Find matching notes using semantic search
    matches = semantic_search(question, note_texts, note_embeddings, model, top_k=2, threshold=0.2)
    
    # CASE 1: No relevant notes found → search web
    if not matches:
        print("📚 No relevant notes found. Searching web...")
        web_answer = web_search(question)
        
        if "error" in web_answer.lower() or "no results" in web_answer.lower():
            print(f"🌐 {web_answer}")
        else:
            print(f"🌐 Found web result, summarizing...")
            # Ask Groq to summarize the web result
            prompt = f"Summarize this in 1-2 sentences: {web_answer}"
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            print(f"🤖 Groq: {response.choices[0].message.content}\n")
        continue
    
    # CASE 2: Relevant notes found → answer from notes
    print(f"\n📚 Found {len(matches)} relevant notes (similarity scores):")
    for m in matches:
        print(f"   • [{m['similarity']:.3f}] {m['text'][:80]}")
    
    # Build prompt from notes
    context = "\n".join(f"- {m['text']}" for m in matches)
    prompt = f"""You are a helpful assistant. Answer based ONLY on these notes.

NOTES:
{context}

QUESTION: {question}

RULES:
- Only use information from the notes above
- If notes don't have the answer, say "I don't have that in my notes"
- Keep answer short (1-2 sentences)

ANSWER:"""
    
    # Ask Groq
    print("\n🤔 Thinking...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    answer = response.choices[0].message.content
    print(f"\n💡 Answer: {answer}")
    print("-"*50)