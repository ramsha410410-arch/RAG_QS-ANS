"""
FastAPI Server — RAG Document Q&A
Endpoints: /upload, /query, /reset, /stats, /health
"""

import os
import uuid
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from rag_pipeline import RAGPipeline, LOADER_MAP

# ─────────────────────────────────────────────
app = FastAPI(
    title="RAG Document Q&A API",
    description="LangChain + FAISS + GPT-4o powered document Q&A",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance (per-server; swap for Redis/session if multi-user)
pipeline: Optional[RAGPipeline] = None
UPLOAD_DIR = Path(tempfile.mkdtemp(prefix="rag_uploads_"))

SUPPORTED_EXTENSIONS = list(LOADER_MAP.keys())


# ─────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────
class InitRequest(BaseModel):
    groq_api_key: str


class QueryRequest(BaseModel):
    question: str


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/supported-types")
def supported_types():
    return {"extensions": SUPPORTED_EXTENSIONS}


@app.post("/init")
def init_pipeline(req: InitRequest):
    """Initialize or reinitialize the pipeline with an API key."""
    global pipeline
    pipeline = RAGPipeline(groq_api_key=req.groq_api_key)
    return {"status": "initialized"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and index a document."""
    if pipeline is None:
        raise HTTPException(status_code=400, detail="Pipeline not initialized. POST /init first.")

    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Supported: {SUPPORTED_EXTENSIONS}",
        )

    # Save to temp file
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / unique_name

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        result = pipeline.ingest_file(str(save_path), file.filename)
    except Exception as e:
        save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content=result)


@app.post("/query")
def query(req: QueryRequest):
    """Ask a question against indexed documents."""
    if pipeline is None:
        raise HTTPException(status_code=400, detail="Pipeline not initialized.")
    if not req.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    try:
        result = pipeline.query(req.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    return JSONResponse(content=result)


@app.post("/reset")
def reset():
    """Clear all indexed documents and conversation history."""
    if pipeline is None:
        raise HTTPException(status_code=400, detail="Pipeline not initialized.")
    pipeline.reset()
    # Clean upload dir
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    UPLOAD_DIR.mkdir(exist_ok=True)
    return {"status": "reset"}


@app.get("/stats")
def stats():
    """Return pipeline statistics."""
    if pipeline is None:
        return {"initialized": False}
    return {**pipeline.stats, "initialized": True}


# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
