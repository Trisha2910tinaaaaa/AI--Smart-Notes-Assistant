# 🧠 AI Smart Notes Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29%2B-red)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203-orange)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Your Second Brain** – A personal RAG (Retrieval-Augmented Generation) system that searches your notes, answers questions, and emails daily summaries. Built from scratch without LangChain.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Smart Note Taking** | Categorized notes with timestamps, saved locally in JSON |
| 🔍 **Semantic Search** | Find notes by meaning, not keywords (sentence-transformers embeddings) |
| 💬 **AI Q&A** | Ask questions, get answers from your notes using Groq's Llama 3 |
| 🌐 **Web Fallback** | Searches DuckDuckGo when your notes don't have the answer |
| 📧 **Daily Email Summary** | Automated email with AI-generated insights, delivered every morning at 9 AM |
| 🎨 **Web Interface** | Clean Streamlit UI with gradient design and responsive layout |
| ⚡ **Fast & Local** | Your data never leaves your machine (except optional web search) |

---

## 🖼️ Demo

![Web Interface Screenshot](screenshot.png)

---


---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.10+ |
| **UI Framework** | Streamlit |
| **LLM API** | Groq (Llama 3.3 70B) |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) |
| **Vector Search** | Custom cosine similarity (NumPy) |
| **Web Search** | DuckDuckGo (ddgs) |
| **Email Automation** | SMTP + Gmail App Password |
| **Scheduling** | Cron (macOS/Linux) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API key ([free at console.groq.com](https://console.groq.com))
- Gmail account (for email automation)

### Installation

```bash
# Clone the repository
git clone https://github.com/Trisha2910tinaaaaa/AI--Smart-Notes-Assistant.git
cd AI--Smart-Notes-Assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keysGROQ_API_KEY="your-groq-api-key"
EMAIL_ADDRESS="your-email@gmail.com"
GMAIL_APP_PASSWORD="your-16-char-app-password"

RUN THe APP
# Terminal Q&A version
python qa_groq.py

# Open crontab
crontab -e

# Add this line (runs at 9 AM daily)
0 9 * * * cd /path/to/project && source venv/bin/activate && python email_summary_with_ai.py >> email_log.txt 2>&1

# Web UI version
streamlit run app.py

# Add notes manually
python notes.py
 ```

## 🎯 Use Cases

| Scenario | How It Helps |
|----------|---------------|
| Daily Journaling | Add notes, get AI insights every morning |
| Research | Ask questions, get answers from your saved knowledge |
| Task Management | "What do I need to do today?" → answers from your notes |
| Learning | Save concepts, search semantically later |
| Quick Capture | Sidebar in web UI for instant note saving |

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Embedding Model | all-MiniLM-L6-v2 (384 dims) |
| Search Latency | <100ms for 100 notes |
| LLM Response | ~2-5 seconds (Groq) |
| Email Delivery | <10 seconds |

---

## 🔮 Future Roadmap

- [ ] Multi-modal search (images + text)
- [ ] Vector database (ChromaDB) for scale
- [ ] Export notes to PDF/Markdown
- [ ] Mobile responsive UI
- [ ] Docker deployment
- [ ] Hugging Face Spaces deployment

---

## 📧 Contact

**Author:** Trisha Soni  
**GitHub:** [@Trisha2910tinaaaaa](https://github.com/Trisha2910tinaaaaa)  
**Email:** trishasonii.29@gmail.com

---

## 📄 License

MIT License – free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for fast Llama 3 inference
- [Sentence-Transformers](https://www.sbert.net/) for embeddings
- [Streamlit](https://streamlit.io/) for the web framework
- [DuckDuckGo](https://duckduckgo.com/) for free web search API

---

⭐ **Star this repo if you found it useful!**
