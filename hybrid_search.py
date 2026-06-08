import json#
import os
from sentence_transformers import SentenceTransformer
import numpy as np

# Load notes
if os.path.exists("notes.json"):
    with open("notes.json", "r") as f:
        notes = json.load(f)
else:
    print("No notes found")
    exit()

# Extract text in a single format
note_texts = []
for note in notes:
    if isinstance(note, dict):#checking if notes are present in dict form
        note_texts.append(note.get("text", ""))#returns only the value pair
    else:
        note_texts.append(str(note))#returns strings of notes

# Load model
print("Loading model...")
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(note_texts)
print("Ready!")

def hybrid_search(query, texts, embeddings, model, alpha=0.5):
    """
    alpha = 0.0 → pure keyword search
    alpha = 1.0 → pure semantic search
    alpha = 0.5 → equal mix
    """
    query_lower = query.lower()
    
    # Keyword scores (exact word matches)
    keyword_scores = []
    for text in texts:
        if query_lower in text.lower():
            keyword_scores.append(1.0)  # Exact match
        else:
            # Count partial word matches
            words = query_lower.split()
            matches = sum(1 for w in words if w in text.lower())
            keyword_scores.append(matches / max(len(words), 1))
    
    # Semantic scores
    q_emb = model.encode([query])[0]
    semantic_scores = []
    for text_emb in embeddings:
        sim = np.dot(q_emb, text_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(text_emb))
        semantic_scores.append(sim)
    
    # Combine scores
    combined = []
    for i in range(len(texts)):
        score = alpha * semantic_scores[i] + (1 - alpha) * keyword_scores[i]
        combined.append((i, score, texts[i]))
    
    combined.sort(key=lambda x: x[1], reverse=True)
    return combined[:3]

# Test it
test_queries = ["family", "work", "dairy", "python"]

for query in test_queries:
    print(f"\n{'='*50}")
    print(f"Query: '{query}'")
    print(f"{'-'*30}")
    
    results = hybrid_search(query, note_texts, embeddings, model, alpha=0.6)
    for idx, score, text in results:
        print(f"   [{score:.3f}] {text}")