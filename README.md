# RAG Document Q&A

> **100% Free** · LangChain + FAISS + Groq (Llama 3) + HuggingFace Embeddings  
> Ask questions about any document — PDF, DOCX, TXT, CSV, PPTX, XLSX, HTML, MD

---

## Table of Contents

1. [What is RAG?](#what-is-rag)
2. [System Architecture](#system-architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation Guide (Windows)](#installation-guide-windows)
6. [Getting a Free Groq API Key](#getting-a-free-groq-api-key)
7. [Running the App](#running-the-app)
8. [Using the Web UI](#using-the-web-ui)
9. [How the Pipeline Works](#how-the-pipeline-works)
10. [Chunking Strategy](#chunking-strategy)
11. [Embedding & Retrieval](#embedding--retrieval)
12. [API Reference](#api-reference)
13. [Supported File Types](#supported-file-types)
14. [Troubleshooting](#troubleshooting)
15. [Extending the Project](#extending-the-project)

---

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that lets an AI answer questions about your own documents — documents it has never been trained on.

Without RAG, if you ask an LLM "What does page 42 of my PDF say?", it has no idea. With RAG:

```
1. Your document is split into small chunks
2. Each chunk is converted into a vector (embedding)
3. When you ask a question, the most relevant chunks are retrieved
4. Those chunks are passed to the LLM as context
5. The LLM answers based on your actual document content
```

This means the AI is not guessing — it is reading your document and answering from it.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      WEB BROWSER                        │
│               frontend/index.html (UI)                  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP REST (localhost:8000)
┌────────────────────────▼────────────────────────────────┐
│                   FASTAPI SERVER                         │
│                    server.py                            │
│   /init  /upload  /query  /reset  /stats  /health       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   RAG PIPELINE                           │
│                  rag_pipeline.py                        │
│                                                         │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐  │
│  │  Document   │   │   Adaptive   │   │ HuggingFace │  │
│  │  Loaders   │──▶│   Chunker    │──▶│  Embeddings │  │
│  │(PDF,DOCX..)│   │(per filetype)│   │(MiniLM-L6)  │  │
│  └─────────────┘   └──────────────┘   └──────┬──────┘  │
│                                               │         │
│  ┌─────────────┐   ┌──────────────┐   ┌──────▼──────┐  │
│  │  Groq LLM  │◀──│ Conversational│◀──│    FAISS    │  │
│  │  Llama 3   │   │    Chain     │   │ VectorStore │  │
│  │  (FREE)    │   │  + Memory    │   │(MMR Retriev)│  │
│  └─────────────┘   └──────────────┘   └─────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Web UI | HTML + CSS + Vanilla JS | Free |
| API Server | FastAPI + Uvicorn | Free |
| RAG Framework | LangChain | Free |
| Vector Store | FAISS (Facebook AI) | Free |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Free (runs locally) |
| LLM | Groq — Llama 3 8B | Free |
| PDF Loader | PyPDF | Free |
| DOCX Loader | Docx2txt | Free |
| Other Loaders | Unstructured | Free |

**Total cost: $0.00**

---

## Project Structure

```
RAG Document Q&A/
│
├── backend/
│   ├── rag_pipeline.py       ← Core RAG logic (loaders, chunking, FAISS, LLM)
│   ├── server.py             ← FastAPI REST API server
│   ├── requirements.txt      ← Python dependencies
│   └── .env.example          ← Environment variable template
│
└── frontend/
    └── index.html            ← Complete web UI (single file)
```

---

## Installation Guide (Windows)

### Prerequisites

Make sure you have Python 3.9 or higher installed. Check with:

```powershell
python --version
```

If you don't have Python, download it from https://python.org

---

### Step 1 — Open PowerShell in the backend folder

Navigate into your project:

```powershell
cd "C:\Users\DELL\Downloads\RAG Document QSANS\backend"
```

---

### Step 2 — Create a virtual environment (recommended)

A virtual environment keeps your project dependencies isolated:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

You will see `(.venv)` appear at the start of your prompt. This means it is active.

---

### Step 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

Also install these manually to make sure everything is present:

```powershell
pip install langchain langchain-community langchain-groq sentence-transformers faiss-cpu pypdf docx2txt python-multipart
```

> **Note:** The first time you run the app, it will automatically download the HuggingFace embedding model (~90MB). This only happens once and is saved to your machine.

---

## Getting a Free Groq API Key

Groq gives you free access to Llama 3 with no credit card required.

1. Go to **https://console.groq.com**
2. Click **Sign Up** and create a free account
3. After logging in, click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Give it a name (e.g. "RAG Project") and copy the key

Your key will look like this:
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Keep this key private. Do not share it or commit it to GitHub.

---

## Running the App

You need **two terminal windows** open at the same time.

### Terminal 1 — Start the backend server

```powershell
cd "C:\Users\DELL\Downloads\RAG Document QSANS\backend"
.venv\Scripts\activate
python server.py
```

You should see:

```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Leave this terminal running. Do not close it.

---

### Terminal 2 — Start the frontend server

```powershell
cd "C:\Users\DELL\Downloads\RAG Document QSANS\frontend"
python -m http.server 3000
```

---

### Open the app in your browser

Type this manually in your browser address bar:

```
http://localhost:3000
```

Or simply double-click `frontend/index.html` in File Explorer.

---

## Using the Web UI

### Step 1 — Enter your Groq API Key

Paste your `gsk_...` key into the **Groq API Key** field in the top-left sidebar.

### Step 2 — Initialize the Pipeline

Click the **Initialize Pipeline** button. Wait for the green dot to appear and the status to say `pipeline ready`.

### Step 3 — Upload Documents

Click the upload area or drag and drop your files. Each file will show a status badge:

- `⟳` — currently indexing
- `✓` — successfully indexed
- `✗` — error (unsupported format or corrupted file)

### Step 4 — Ask Questions

Type your question in the chat box at the bottom and press **Enter**. The AI will answer based on your uploaded documents and show which file and page the answer came from.

---

## How the Pipeline Works

### Stage 1 — Document Loading

When you upload a file, the correct loader is selected based on the file extension:

```
.pdf   → PyPDFLoader           extracts text page by page
.docx  → Docx2txtLoader        extracts Word document text
.txt   → TextLoader            plain text
.csv   → CSVLoader             comma-separated data
.pptx  → UnstructuredPPTX      extracts slide text
.xlsx  → UnstructuredExcel     extracts spreadsheet content
.html  → UnstructuredHTML      extracts webpage content
.md    → UnstructuredMarkdown  extracts markdown text
```

### Stage 2 — Chunking

The loaded text is split into smaller overlapping chunks. Smaller chunks are easier to search and match against your question. Each chunk carries metadata (source filename, page number) so the answer can be traced back to the original document.

### Stage 3 — Embedding

Each chunk is converted into a 384-dimensional numerical vector using the HuggingFace `all-MiniLM-L6-v2` model running locally on your CPU. Similar meaning = similar vector direction.

### Stage 4 — FAISS Indexing

All vectors are stored in a FAISS index — a highly optimised similarity search engine built by Facebook AI Research. FAISS can search millions of vectors in milliseconds.

### Stage 5 — Query and Retrieval

When you ask a question:

```
1. Your question is embedded into a vector
2. FAISS finds the 20 most similar chunk vectors
3. MMR re-ranks them → picks 5 most relevant AND diverse chunks
4. Those 5 chunks are sent to the LLM as context
```

### Stage 6 — Generation

Llama 3 (via Groq) reads your question + the retrieved context + conversation history and generates a precise answer grounded in your documents.

---

## Chunking Strategy

Chunking is one of the most important optimisations in a RAG pipeline. The right chunk size depends on the document type.

| File Type | Chunk Size | Overlap | Why |
|-----------|-----------|---------|-----|
| PDF / DOCX / TXT / MD / HTML | 1200 chars | 200 chars | Prose needs larger context to preserve meaning |
| PPTX / PPT | 800 chars | 100 chars | Slides are already short and semi-structured |
| CSV / XLSX / XLS | 512 chars | 64 chars | Structured data — small chunks reduce noise |

**Separator hierarchy** — chunks always break at the most natural boundary first:

```
paragraph (\n\n) → line (\n) → sentence (.) → ! → ? → space → character
```

**Overlap** — each chunk shares some characters with the previous one. This prevents answers from being missed because they happened to fall right on a chunk boundary.

---

## Embedding & Retrieval

### Embedding Model: `all-MiniLM-L6-v2`

- Runs 100% locally on your CPU — no API calls, no cost
- Produces 384-dimensional vectors
- Trained specifically for semantic similarity (not just keyword matching)
- Fast: embeds hundreds of chunks per second on CPU

### Retrieval Strategy: MMR

**Maximal Marginal Relevance** balances two goals simultaneously:

- **Relevance** — retrieved chunks should closely match your question
- **Diversity** — retrieved chunks should not all say the same thing

Without MMR, FAISS might return 5 chunks that are nearly identical paragraphs. MMR ensures the 5 chunks together cover more ground and give the LLM richer context.

### Conversation Memory

The pipeline remembers the last 5 turns using `ConversationBufferWindowMemory`, enabling natural follow-up questions:

```
You:  What is the main topic of this document?
AI:   The document is about neural networks in computer vision...

You:  Can you give more detail on that?    ← AI understands "that" refers to neural networks
AI:   Specifically, the document covers CNN architectures...
```

---

## API Reference

All endpoints are available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### POST /init — Initialize pipeline

```json
Request:  { "groq_api_key": "gsk_..." }
Response: { "status": "initialized" }
```

### POST /upload — Upload and index a document

```
Request:  multipart/form-data  { file: <your file> }
Response: { "status": "indexed", "filename": "report.pdf", "chunks": 47, "pages": 12 }
```

### POST /query — Ask a question

```json
Request:  { "question": "What are the main findings?" }
Response: {
  "answer": "The main findings are...",
  "sources": [
    { "source": "report.pdf", "snippet": "The study found...", "page": 3 }
  ]
}
```

### POST /reset — Clear everything

```json
Response: { "status": "reset" }
```

### GET /stats — Pipeline statistics

```json
Response: {
  "initialized": true,
  "indexed_files": ["report.pdf", "data.csv"],
  "total_chunks": 134,
  "ready": true
}
```

### GET /health — Health check

```json
Response: { "status": "ok" }
```

---

## Supported File Types

| Extension | Format | Loader Used |
|-----------|--------|-------------|
| `.pdf` | PDF Document | PyPDFLoader |
| `.txt` | Plain Text | TextLoader |
| `.docx` `.doc` | Word Document | Docx2txtLoader |
| `.csv` | CSV Spreadsheet | CSVLoader |
| `.xlsx` `.xls` | Excel Spreadsheet | UnstructuredExcelLoader |
| `.pptx` `.ppt` | PowerPoint | UnstructuredPowerPointLoader |
| `.html` `.htm` | Web Page | UnstructuredHTMLLoader |
| `.md` | Markdown | UnstructuredMarkdownLoader |

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'langchain'`

Your virtual environment is not activated. Run:

```powershell
.venv\Scripts\activate
```

---

### `ModuleNotFoundError: No module named 'rag_pipeline'`

You are not inside the `backend` folder, or the file is named incorrectly. Run:

```powershell
cd "C:\Users\DELL\Downloads\RAG Document QSANS\backend"
ls
```

The file must be named exactly `rag_pipeline.py`. If it shows `Rag_pipeline.py`, rename it:

```powershell
Rename-Item "Rag_pipeline.py" "rag_pipeline.py"
```

---

### `ERR_ADDRESS_INVALID` in browser

Do not click auto-generated links. Type manually in the address bar:

```
http://localhost:3000
```

---

### Blank page in browser

Press F12 → Console tab and check for red errors. Most likely the backend is not running. Confirm Terminal 1 shows the Uvicorn message, if not restart it:

```powershell
python server.py
```

---

### Groq API error

Make sure your key starts with `gsk_` and has no extra spaces. Generate a fresh key at https://console.groq.com/keys

---

### First upload is very slow

The HuggingFace model (~90MB) is downloading for the first time. This is normal. Subsequent runs are instant.

---

## Extending the Project

### Persist FAISS index across restarts

```python
# Save after indexing
self.vectorstore.save_local("faiss_index")

# Load on startup
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
```

### Switch to a more powerful Groq model

In `rag_pipeline.py`:

```python
model="llama3-8b-8192"    # default — fast
model="llama3-70b-8192"   # more powerful, still free
model="mixtral-8x7b-32768" # large context window
```

Check all available models at https://console.groq.com/docs/models

### Add hybrid search (BM25 + FAISS)

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever

bm25 = BM25Retriever.from_documents(chunks)
faiss_ret = vectorstore.as_retriever()
ensemble = EnsembleRetriever(retrievers=[bm25, faiss_ret], weights=[0.4, 0.6])
```

### Enable streaming responses

```python
# rag_pipeline.py
self.llm = ChatGroq(model="llama3-8b-8192", streaming=True)

# server.py — use StreamingResponse from FastAPI
```

### Support multiple users

```python
pipelines: dict[str, RAGPipeline] = {}

@app.post("/init")
def init(req: InitRequest, session_id: str = Header(...)):
<img width="1361" height="619" alt="image" src="https://github.com/user-attachments/assets/770ccb8a-364e-47d6-bd03-403ceba980b5" />

    pipelines[session_id] = RAGPipeline(groq_api_key=req.groq_api_key)
```
