# Technify Academic AI Assistant (TAIA) 🎓🤖

> AI-powered academic assistant integrated with Technify University ERP

## 🏗️ Project Overview

TAIA is an intelligent chatbot microservice that integrates with the Technify University ERP system. It provides natural language support to students, faculty, and administrators for academic queries.

**Key Features:**
- 💬 Natural language Q&A for academic information
- 🔒 Role-based access control (Student, Faculty, Admin, Finance, Exam Officer)
- 📚 Knowledge base with RAG for university policies
- 📊 Study recommendations and planning
- 🔗 Secure ERP API integration (no direct database access)

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Core language |
| FastAPI | Web framework |
| LangChain | LLM orchestration |
| ChromaDB | Vector database for RAG |
| OpenAI GPT / Llama | LLM backbone |
| JWT | Authentication |

## 📁 Project Structure

```
technify-ai-assistant/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── auth/                # JWT & RBAC
│   ├── api/                 # API routes & middleware
│   ├── services/            # Business logic
│   ├── chains/              # LangChain chains
│   ├── prompts/             # Prompt templates
│   └── models/              # Data models
├── data/
│   ├── synthetic/           # Test data
│   ├── documents/           # Policy PDFs
│   └── vector_store/        # ChromaDB storage
├── mock_erp/                # Mock ERP for testing
├── scripts/                 # Utility scripts
├── tests/                   # Test files
└── docs/                    # Documentation
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repo-url>
cd technify-ai-assistant
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
copy .env.example .env
# Edit .env with your API keys
```

### 3. Generate Test Data
```bash
python scripts/generate_data.py
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```

### 5. Open API Docs
Visit: http://localhost:8000/docs

## 👥 Team

| Role | Responsibility |
|------|---------------|
| Team Lead | Architecture, LangChain pipeline, code review |
| Backend Dev 1 | FastAPI, JWT auth, API gateway |
| Backend Dev 2 | ERP connectors, audit logging |
| AI/NLP Dev | LangChain chains, prompts, conversation |
| RAG Dev | ChromaDB, document ingestion, knowledge base |
| Data/Test | Synthetic data, testing, documentation |

## 📋 Modules

1. **User Auth Verification** — JWT validation & role checking
2. **Academic Info Retrieval** — ERP API connectors
3. **Knowledge Base (RAG)** — University policy Q&A
4. **Study Recommendations** — Study plans & course suggestions
5. **Conversation Management** — Context-aware multi-turn chat

## 📄 License

Internal project — Technify Software House © 2026
