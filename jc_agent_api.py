#!/usr/bin/env python3
"""JC Agent API (FastAPI).

This is the safe, canonical API server entrypoint for the tray/desktop launchers.

Security note:
  Do NOT hardcode secrets in this file. Use `.env` / environment variables.

Run locally:
  python jc_agent_api.py

Or with uvicorn:
  uvicorn jc_agent_api:app --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, TypedDict, List, Optional, Dict

from fastapi import FastAPI, HTTPException, Query, Depends, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from jc.key_routes import router as keys_router
from jc.secrets import get_effective_provider, get_llm_api_key, get_llm_model, load_env
from jc.key_locker import STORAGE_PATH as JC_STORAGE_PATH
from jc.workspace_indexer import index_workspace, folder_size
from jc.logging_config import setup_logging, get_logger
from jc.error_handling import handle_errors, CircuitBreaker
from jc.auth import get_current_user, get_current_user_optional, User
from jc.external_storage import (
    get_storage_manager, 
    discover_drives, 
    get_drive_summary,
    search_files as search_storage_files,
    find_ai_models
)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import shutil


_BASE_DIR = Path(__file__).resolve().parent
_LOG_FILE = _BASE_DIR / "jc_agent.log"

# Setup structured logging
logger = setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=_LOG_FILE,
    json_format=False
)

# Setup rate limiting
limiter = Limiter(key_func=get_remote_address)

_PUBLIC_DIR = _BASE_DIR / "public"
_env_loaded = False

_chat_html_cache: str | None = None
_jc_instance: Any | None = None
_jc_init_lock = threading.Lock()


def _ensure_env_loaded() -> None:
    """Load `.env` once (fast path for frequent /health polling)."""
    global _env_loaded
    if _env_loaded:
        return
    try:
        load_env(_BASE_DIR / ".env")
    except Exception:
        pass
    _env_loaded = True


def _get_chat_html() -> str:
    """Return the web chat UI HTML (cached)."""
    global _chat_html_cache
    if _chat_html_cache is not None:
        return _chat_html_cache

    # Preferred: serve the bundled template.
    template_path = _BASE_DIR / "templates" / "chat.html"
    if template_path.exists():
        _chat_html_cache = template_path.read_text(encoding="utf-8", errors="ignore")
        return _chat_html_cache

    # Fallback: minimal inline page.
    _chat_html_cache = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>JC Agent</title>
    <style>
      body { font-family: system-ui, Segoe UI, Arial, sans-serif; margin: 2rem; line-height: 1.4; }
      code { background: #f4f4f4; padding: 0.15rem 0.3rem; border-radius: 4px; }
      a { color: #0a58ca; text-decoration: none; }
      a:hover { text-decoration: underline; }
      .card { max-width: 52rem; padding: 1.25rem 1.5rem; border: 1px solid #ddd; border-radius: 12px; }
    </style>
  </head>
  <body>
    <div class=\"card\">
      <h1>JC Agent</h1>
      <p>Server is running. For interactive API docs, go to <a href=\"/docs\">/docs</a>.</p>
      <p>CLI: run <code>python -m jc</code> from the repo root.</p>
      <p>Status: <a href=\"/health\">/health</a></p>
    </div>
  </body>
</html>"""
    return _chat_html_cache


def _get_jc() -> Any:
    """Lazily construct the JC runtime (without voice) once."""
    global _jc_instance
    if _jc_instance is not None:
        return _jc_instance

    with _jc_init_lock:
        if _jc_instance is None:
            # Import lazily to keep FastAPI startup snappy and avoid heavy deps.
            from jc import JC

            _jc_instance = JC(enable_voice=False)
    return _jc_instance


class HealthResponse(TypedDict):
    status: str
    provider: str
    model: str
    has_llm_key: bool


class ChatRequest(BaseModel):
  message: str


class ChatResponse(TypedDict):
  response: str


app = FastAPI(title="JC Agent API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if _PUBLIC_DIR.exists():
    app.mount("/public", StaticFiles(directory=str(_PUBLIC_DIR)), name="public")
app.include_router(keys_router)


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return HTTPException(
        status_code=500,
        detail="An internal server error occurred. Please check the logs."
    )


@app.get("/keys.html", include_in_schema=False)
def key_manager_ui():
    if not _PUBLIC_DIR.exists():
        raise HTTPException(status_code=404, detail="Key Locker UI not found")
    ui_file = _PUBLIC_DIR / "keys.html"
    if not ui_file.exists():
        raise HTTPException(status_code=404, detail="Key Locker UI not available")
    return HTMLResponse(ui_file.read_text(encoding="utf-8"), media_type="text/html")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/chat")


@app.get("/chat", include_in_schema=False)
def chat():
    return HTMLResponse(_get_chat_html())


@app.post("/api/chat")
@limiter.limit("10/minute")
@handle_errors(fallback_value={"response": "Sorry, I encountered an error. Please try again."})
async def api_chat(
    request: Request, 
    payload: ChatRequest, 
    user: User = Depends(get_current_user)
) -> ChatResponse:
    """Chat endpoint used by the bundled web UI (`templates/chat.html`)."""
    _ensure_env_loaded()
    
    logger.info(f"Chat request from user: {user.username}")
    message = (payload.message or "").strip()
    if not message:
        return {"response": "Say something and I'll respond."}

    jc = _get_jc()
    response = await jc.process_message(message)
    return {"response": response}


class AskRequest(BaseModel):
    workspaceId: str
    README: Optional[str] = None
    top_files: Optional[List[str]] = None
    top_languages: Optional[List[Dict[str, Any]]] = None
    recent_commits: Optional[List[str]] = None


class EventRequest(BaseModel):
    workspaceId: str
    type: str
    payload: Optional[Dict[str, Any]] = None


class PinRequest(BaseModel):
    workspaceId: str
    path: str
    tags: Optional[List[str]] = None
    note: Optional[str] = None


class DeleteRequest(BaseModel):
    workspaceId: str


@app.post("/ask-questions")
@limiter.limit("20/minute")
async def ask_questions(
    request: Request,
    payload: AskRequest,
    user: User = Depends(get_current_user)
):
    """Generate prioritized clarifying questions for a workspace.

    The endpoint accepts a compact workspace metadata payload and returns a
    numbered list of short clarifying questions. If no LLM key is available the
    implementation falls back to a deterministic mock so it can be used offline.
    """
    from jc.ask_questions import generate_clarifying_questions
    
    logger.info(f"Ask questions request from user: {user.username}")
    meta = payload.dict()
    questions = generate_clarifying_questions(meta)
    return {"workspaceId": payload.workspaceId, "questions": questions}


@app.post("/events")
@limiter.limit("50/minute")
async def events(
    request: Request,
    req: EventRequest,
    user: User = Depends(get_current_user)
):
    """Accept workspace events (watcher, index-requests, etc.) and persist them.

    If an index-request event is received the server will run a workspace index
    and write `metadata.json` into the workspace storage folder.
    """
    ws_id = req.workspaceId
    ws_dir = JC_STORAGE_PATH / ws_id
    ws_dir.mkdir(parents=True, exist_ok=True)

    # Append event to events.log
    events_log = ws_dir / "events.log"
    entry = {"at": __import__("datetime").datetime.utcnow().isoformat() + "Z", "type": req.type, "payload": req.payload}
    with open(events_log, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")

    result: Dict[str, object] = {"ok": True}

    if req.type == "index-request":
        # If the client included a path we index that, otherwise index the workspace root
        target_path = req.payload.get("path") if isinstance(req.payload, dict) and req.payload.get("path") else ws_dir
        metadata = index_workspace(target_path)
        meta_file = ws_dir / "metadata.json"
        meta_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        result["metadata"] = metadata

    return result


@app.get("/status")
def status():
    """Return status for known workspaces under the JC storage path."""
    workspaces = []
    for child in JC_STORAGE_PATH.iterdir():
        if not child.is_dir():
            continue
        try:
            size = folder_size(child)
        except Exception:
            size = 0
        workspaces.append({"id": child.name, "path": str(child), "size": size})
    return {"workspaces": workspaces}


@app.post("/delete-workspace")
def delete_workspace(req: DeleteRequest):
    ws_dir = JC_STORAGE_PATH / req.workspaceId
    if not ws_dir.exists():
        raise HTTPException(status_code=404, detail="Workspace not found")
    try:
        shutil.rmtree(ws_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


@app.post("/pin-file")
def pin_file(req: PinRequest):
    ws_dir = JC_STORAGE_PATH / req.workspaceId
    if not ws_dir.exists():
        raise HTTPException(status_code=404, detail="Workspace not found")

    meta_file = ws_dir / "metadata.json"
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
    else:
        meta = {}

    pins = meta.get("pinned", [])
    # Ensure unique pin by path
    existing = next((p for p in pins if p.get("path") == req.path), None)
    pin_entry = {"path": req.path, "tags": req.tags or [], "note": req.note, "pinned_at": __import__("datetime").datetime.utcnow().isoformat() + "Z"}
    if existing:
        existing.update(pin_entry)
    else:
        pins.append(pin_entry)

    meta["pinned"] = pins
    meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"ok": True, "pinned": pin_entry}


async def _stream_llm_response(message: str) -> AsyncGenerator[str, None]:
    """Generate SSE stream from LLM response."""
    _ensure_env_loaded()
    
    try:
        from jc.llm_provider import LLMProvider
        
        llm = LLMProvider()
        messages = [{"role": "user", "content": message}]
        
        # For now, simulate streaming by yielding the full response
        # A true streaming implementation would use the LLM's stream=True
        # and yield chunks as they arrive
        response = llm.call(messages, stream=False)
        
        # Split response into words for simulated streaming effect
        words = response.split()
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            await asyncio.sleep(0.02)  # Small delay for streaming effect
        
        yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@app.get("/api/chat/stream")
async def api_chat_stream(message: str = Query(..., description="Message to send")):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).
    
    Returns chunks of the response as they're generated.
    Use with EventSource in the browser:
    
        const es = new EventSource('/api/chat/stream?message=' + encodeURIComponent(msg));
        es.onmessage = (e) => { const data = JSON.parse(e.data); ... };
    """
    return StreamingResponse(
        _stream_llm_response(message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/health")
def health() -> HealthResponse:
    """Basic health check endpoint - no authentication required."""
    _ensure_env_loaded()

    provider = get_effective_provider()
    model = get_llm_model(provider)

    return {
        "status": "ok",
        "provider": provider,
        "model": model,
        "has_llm_key": bool(get_llm_api_key(provider)),
    }


@app.get("/health/detailed")
async def health_detailed(user: User = Depends(get_current_user)):
    """Detailed health check with system status - requires authentication."""
    import sqlite3
    import psutil
    from jc.key_locker import KeyLocker
    
    _ensure_env_loaded()
    
    health_status = {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # Check LLM provider
    try:
        provider = get_effective_provider()
        model = get_llm_model(provider)
        has_key = bool(get_llm_api_key(provider))
        health_status["checks"]["llm"] = {
            "status": "ok" if has_key else "warning",
            "provider": provider,
            "model": model,
            "has_key": has_key
        }
    except Exception as e:
        health_status["checks"]["llm"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check database
    try:
        from jc import JC
        db_path = Path.home() / ".jc-agent" / "brain.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("SELECT 1").fetchone()
        conn.close()
        health_status["checks"]["database"] = {
            "status": "ok",
            "path": str(db_path)
        }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check KeyLocker
    try:
        locker = KeyLocker()
        keys = locker.list_keys()
        health_status["checks"]["keylocker"] = {
            "status": "ok",
            "keys_count": len(keys)
        }
    except Exception as e:
        health_status["checks"]["keylocker"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check system resources
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        health_status["checks"]["system"] = {
            "status": "ok",
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "cpu_count": psutil.cpu_count()
        }
        
        if memory.percent > 90 or disk.percent > 90:
            health_status["checks"]["system"]["status"] = "warning"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["checks"]["system"] = {
            "status": "error",
            "error": str(e)
        }
    
    return health_status


# ===== External Storage Research Endpoints =====

@app.get("/storage/discover")
async def discover_storage(user: User = Depends(get_current_user)):
    """Discover all available external storage devices.
    
    Returns list of detected drives with metadata.
    """
    logger.info(f"Storage discovery requested by user: {user.username}")
    
    try:
        devices = discover_drives()
        return {
            "devices": [d.to_dict() for d in devices],
            "count": len(devices)
        }
    except Exception as e:
        logger.error(f"Storage discovery error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/storage/summary")
async def storage_summary(user: User = Depends(get_current_user)):
    """Get a human-readable summary of all external storage.
    
    Returns formatted summary with drive info, special locations, and index stats.
    """
    logger.info(f"Storage summary requested by user: {user.username}")
    
    try:
        summary = get_drive_summary()
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Storage summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/storage/index")
async def index_storage(
    request: Request,
    drive: str = Query(..., description="Drive letter or mount point (e.g., 'G:', '/mnt/usb')"),
    max_files: int = Query(10000, description="Maximum files to index"),
    user: User = Depends(get_current_user)
):
    """Index files on an external drive for research.
    
    This scans the drive and indexes important files (AI models, docs, code, data).
    Large drives may take several minutes to index.
    """
    logger.info(f"Storage indexing requested by user {user.username}: drive={drive}, max_files={max_files}")
    
    try:
        storage_mgr = get_storage_manager()
        indexed_count = storage_mgr.index_drive(drive, max_files)
        
        return {
            "drive": drive,
            "indexed_count": indexed_count,
            "message": f"Successfully indexed {indexed_count} files from {drive}"
        }
    except Exception as e:
        logger.error(f"Storage indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/storage/search")
async def search_storage(
    query: str = Query(..., description="Search query"),
    file_types: Optional[str] = Query(None, description="Comma-separated file extensions (e.g., '.py,.md')"),
    drives: Optional[str] = Query(None, description="Comma-separated drive letters"),
    limit: int = Query(50, description="Maximum results"),
    user: User = Depends(get_current_user)
):
    """Search indexed files on external storage.
    
    Search by filename, path, keywords, or description.
    """
    logger.info(f"Storage search requested by user {user.username}: query={query}")
    
    try:
        # Parse filters
        file_type_list = file_types.split(',') if file_types else None
        drive_list = drives.split(',') if drives else None
        
        # Search
        results = search_storage_files(
            query=query,
            file_types=file_type_list,
            drives=drive_list,
            limit=limit
        )
        
        return {
            "query": query,
            "count": len(results),
            "results": [r.to_dict() for r in results]
        }
    except Exception as e:
        logger.error(f"Storage search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/storage/ai-models")
async def list_ai_models(user: User = Depends(get_current_user)):
    """Find all AI models on external storage.
    
    Returns list of .gguf, .safetensors, .pt, .pth, .onnx files.
    """
    logger.info(f"AI models list requested by user: {user.username}")
    
    try:
        models = find_ai_models()
        
        # Group by drive for better presentation
        by_drive = {}
        for model in models:
            drive = model.drive
            if drive not in by_drive:
                by_drive[drive] = []
            by_drive[drive].append(model.to_dict())
        
        return {
            "count": len(models),
            "by_drive": by_drive,
            "models": [m.to_dict() for m in models]
        }
    except Exception as e:
        logger.error(f"AI models list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Keep defaults aligned with existing launcher/scripts.
    _ensure_env_loaded()

    port = int(os.getenv("API_PORT") or os.getenv("JC_PORT") or "8000")
    host = os.getenv("API_HOST") or "127.0.0.1"

    import uvicorn

    uvicorn.run(app, host=host, port=port, log_level="info")
