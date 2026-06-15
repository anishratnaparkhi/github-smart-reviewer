# Smart GitHub Project Reviewer

An AI-powered, Retrieval-Augmented Generation (RAG) codebase analyzer that clones, indexes, and reviews GitHub repositories. The application generates structured summaries, code quality reports, security audits, test plan recommendations, and custom interview preparation materials to evaluate internship readiness.

---

## 🚀 Key Features

* **Automated Codebase Indexing:** Clones public Git repositories shallowly (`depth=1`), scans and filters files recursively, and processes code context in memory.
* **Retrieval-Augmented Generation (RAG):** Employs **FAISS (Facebook AI Similarity Search)** vector storage and **Google Gemini Embeddings (`gemini-embedding-001`)** to enable semantic code search and context retrieval.
* **Core Repository Review:** Analyzes repository purpose, detects tech stacks, evaluates code smells, audits security postures, and suggests README layout enhancements.
* **Internship Readiness Evaluation:** Computes an internship-readiness scorecard, generates polished resume project bullets, drafts 30-second elevator pitches, and provides mock technical interview Q&A lists.

---

## 📂 Project Architecture

```
github-smart-reviewer/
├── app/
│   ├── chains/         # Prompts, LLM wrapper, and consolidated LangChain scripts
│   ├── indexing/       # Text chunking, document parsing, and FAISS indexing
│   ├── loaders/        # Local file scanner and Git clone loader
│   ├── schemas/        # Pydantic models for structured output serialization
│   ├── services/       # Core review orchestration and export pipelines
│   └── utils/          # File filters, cleanup helpers, and validators
├── frontend/
│   └── streamlit_app.py# Streamlit user interface
├── tests/              # Automated unit tests
├── requirements.txt    # Application dependencies
└── .gitignore          # File exclusions (excludes .env, .venv, vectorstores, temp_repos)
```

---

## ⚙️ Setup & Installation

### Prerequisites
* Python 3.9 or higher
* Git installed locally
* Google Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/))

### 1. Clone the repository
```bash
git clone https://github.com/anishratnaparkhi/github-smart-reviewer.git
cd github-smart-reviewer
```

### 2. Set up a virtual environment
```bash
# Windows Command Prompt
python -m venv .venv
.venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory and configure the following variables:
```env
GOOGLE_API_KEY = "your-actual-gemini-api-key"
LLM_PROVIDER = "google"
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-001"
```

---

## 🏃 How to Run the App

1. Activate your virtual environment (if not already done).
2. Launch the Streamlit application:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
3. Open the browser link provided by Streamlit (usually `http://localhost:8501`).
4. Paste a public GitHub repository URL and click **Analyze Repository**.
