# Smart GitHub Project Reviewer

An AI-powered, Retrieval-Augmented Generation (RAG) codebase analyzer that clones, indexes, and reviews GitHub repositories. The application generates structured summaries, architecture flowcharts, code quality reports, security audits, test plan recommendations, and custom resume/interview preparation materials to evaluate internship readiness.

---

## 🚀 Key Features

* **Automated Codebase Indexing:** Clones public Git repositories shallowly (`depth=1`), scans and filters files recursively, and processes code context in memory.
* **Retrieval-Augmented Generation (RAG):** Employs **FAISS (Facebook AI Similarity Search)** vector storage and **Google Gemini Embeddings (`gemini-embedding-001`)** to enable semantic code search and context retrieval.
* **Core Repository Review:** Analyzes repository purpose, detects tech stacks, identifies architectural design styles (MVC, layered, monolith), evaluates code smells, audits security postures, and suggests README layout enhancements.
* **Internship Readiness Evaluation:** Computes an internship-readiness scorecard, generates polished resume project bullets, drafts 30-second elevator pitches, and provides mock technical interview Q&A lists.

---

## 🛠️ Technical Optimizations & Engineering Depth

Under the hood, the application is heavily optimized to run on strict free-tier API quotas (e.g., 5 RPM, 250k TPM, and 20 RPD):

* **Structured Request Consolidation:** Redesigned legacy sequential pipelines by consolidating 10 separate API chains into **exactly 2 structured requests** utilizing LangChain's native Pydantic validation (`with_structured_output`). This yielded an **80% reduction in daily quota consumption**.
* **Tokens Per Minute (TPM) Optimization:** Implemented a compact 800-character Recursive Text Chunker and dynamic retriever limits ($k = 10$). This reduced the input token count sent to the LLM from ~5,000 down to **~1,800 tokens** per analysis run (a **64% reduction in TPM usage**).
* **Automated Disk Cleanup:** Built filesystem routines that dynamically delete cloned repository code on disk immediately after the in-memory vector database is generated. Included custom permission-override handlers to safely delete Windows read-only `.git` pack files.
* **Time-Based Session Pruning:** Runs an event-driven routine on startup to garbage-collect and delete stale session vector databases older than 24 hours.
* **Rate-Limit Resiliency:** Configured exponential backoff retries (`max_retries = 5`) within LangChain to gracefully handle transient 503 capacity issues.

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
