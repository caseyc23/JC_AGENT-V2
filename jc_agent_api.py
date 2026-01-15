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
from pathlib import Path
from typing import Any, AsyncGenerator, TypedDict, List, Optional, Dict

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from jc.key_routes import router as keys_router
from jc.secrets import get_effective_provider, get_llm_api_key, get_llm_model, load_env
from jc.key_locker import STORAGE_PATH as JC_STORAGE_PATH
from jc.workspace_indexer import index_workspace, folder_size
import shutil


_BASE_DIR = Path(__file__).resolve().parent
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
if _PUBLIC_DIR.exists():
    app.mount("/public", StaticFiles(directory=str(_PUBLIC_DIR)), name="public")
app.include_router(keys_router)


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
async def api_chat(payload: ChatRequest) -> ChatResponse:
    """Chat endpoint used by the bundled web UI (`templates/chat.html`)."""
    _ensure_env_loaded()

    message = (payload.message or "").strip()
    if not message:
        return {"response": "Say something and I'll respond."}

    try:
        jc = _get_jc()
        response = await jc.process_message(message)
        return {"response": response}
    except Exception:
        # Keep response JSON-shape stable for the frontend.
        return {
            "response": "Sorry — I hit an error processing that. Check `jc_agent.log` for details.",
        }


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
def ask_questions(payload: AskRequest):
    """Generate prioritized clarifying questions for a workspace.

    The endpoint accepts a compact workspace metadata payload and returns a
    numbered list of short clarifying questions. If no LLM key is available the
    implementation falls back to a deterministic mock so it can be used offline.
    """
    from jc.ask_questions import generate_clarifying_questions

    meta = payload.dict()
    questions = generate_clarifying_questions(meta)
    return {"workspaceId": payload.workspaceId, "questions": questions}


@app.post("/events")
def events(req: EventRequest):
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
    _ensure_env_loaded()

    provider = get_effective_provider()
    model = get_llm_model(provider)

    return {
        "status": "ok",
        "provider": provider,
        "model": model,
        "has_llm_key": bool(get_llm_api_key(provider)),
    }


if __name__ == "__main__":
    # Keep defaults aligned with existing launcher/scripts.
    _ensure_env_loaded()

    port = int(os.getenv("API_PORT") or os.getenv("JC_PORT") or "8000")
    host = os.getenv("API_HOST") or "127.0.0.1"

    import uvicorn

    uvicorn.run(app, host=host, port=port, log_level="info")
