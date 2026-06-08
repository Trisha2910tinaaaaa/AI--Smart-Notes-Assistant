import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
from ddgs import DDGS

load_dotenv()
client = Groq()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI-Smart Notes Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card style for answers */
    .answer-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Source card */
    .source-card {
        background: #ffffff;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #10b981;
        font-size: 0.9rem;
    }
    
    /* Custom title */
    .custom-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1e2f 0%, #2d2d44 100%);
    }
    
    /* Input box */
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.2);
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
if os.path.exists("notes.json"):
    with open("notes.json", "r") as f:
        notes = json.load(f)
else:
    notes = []

note_texts = []
for note in notes:
    if isinstance(note, dict):
        note_texts.append(note.get("text", ""))
    else:
        note_texts.append(str(note))

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

if note_texts:
    note_embeddings = model.encode(note_texts)
else:
    note_embeddings = []

# ---------- SEARCH ----------
def search_notes(query, top_k=3):
    if not note_texts:
        return []
    
    q_emb = model.encode([query])[0]
    similarities = []
    
    for emb in note_embeddings:
        sim = np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb))
        similarities.append(sim)
    
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        if similarities[idx] > 0.15:
            results.append({
                "text": note_texts[idx],
                "score": round(similarities[idx], 3)
            })
    return results

def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                return results[0]['body']
            return None
    except:
        return None

# ---------- UI ----------
# Hero section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<p class="custom-title" style="text-align: center;">🧠 AI-Smart Notes Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Your AI-powered memory companion</p>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard")
    st.markdown("---")
    
    # Stats in styled boxes
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#667eea;">{len(note_texts)}</h3>
            <p style="margin:0; font-size:0.8rem;">Total Notes</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        topics = len(set([n.get("category", "general") for n in notes if isinstance(n, dict)]))
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#667eea;">{topics}</h3>
            <p style="margin:0; font-size:0.8rem;">Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick add section
    st.markdown("### ✍️ Quick Capture")
    new_note = st.text_area("", placeholder="What's on your mind?", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Tag", ["personal", "work", "idea", "task"])
    with col2:
        if st.button("💾 Save", use_container_width=True):
            if new_note:
                new_entry = {
                    "text": new_note,
                    "category": category,
                    "timestamp": datetime.now().isoformat()
                }
                notes.append(new_entry)
                with open("notes.json", "w") as f:
                    json.dump(notes, f)
                st.success("✓ Saved!")
                st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.75rem; color: #888;">
        Built with Streamlit + Groq<br>
        Your data stays local
    </div>
    """, unsafe_allow_html=True)

# Main content area
st.markdown("### 💭 Ask me anything")

question = st.text_input("", placeholder="e.g., What do I need to do today?", label_visibility="collapsed")

if question:
    with st.spinner("Searching my memory..."):
        matches = search_notes(question)
        
        if matches:
            # Answer from notes
            context = "\n".join([f"- {m['text']}" for m in matches])
            prompt = f"""Answer this question using ONLY the notes below. Be conversational and helpful.

Notes:
{context}

Question: {question}

Answer:"""
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            answer = response.choices[0].message.content
            
            # Display answer in styled card
            st.markdown(f"""
            <div class="answer-card">
                <strong>🤖 Answer</strong><br>
                {answer}
            </div>
            """, unsafe_allow_html=True)
            
            # Show sources
            with st.expander("📚 Sources from my notes", expanded=False):
                for m in matches:
                    st.markdown(f"""
                    <div class="source-card">
                        <span style="color:#10b981;">●</span> {m['text']}<br>
                        <span style="font-size:0.7rem; color:#888;">relevance: {m['score']}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            # Search web
            st.info("🌐 Not in my notes. Searching the web...")
            web_result = search_web(question)
            
            if web_result:
                prompt = f"Summarize this in 2 concise sentences: {web_result}"
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                st.markdown(f"""
                <div class="answer-card">
                    <strong>🌐 Web Answer</strong><br>
                    {response.choices[0].message.content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Couldn't find an answer. Try rephrasing your question.")

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; font-size: 0.75rem; color: #888;">Your Second Brain • Notes stay on your machine</p>', unsafe_allow_html=True)