#!/usr/bin/env python3
"""DEPRECATED: legacy API entrypoint.

This file used to host the FastAPI server. The canonical server entrypoint is now
`jc_agent_api.py`.

Security note:
  Do NOT hardcode secrets here. Use `.env` / environment variables.
"""

from __future__ import annotations

import os

from jc_agent_api import app


if __name__ == "__main__":
    try:
        import uvicorn
    except Exception as e:
        raise SystemExit(
            "uvicorn is required to run the API server. "
            "Install dependencies (e.g. pip install -r requirements.txt). "
            f"Original error: {e}"
        )

    host = os.getenv("API_HOST") or "127.0.0.1"
    port = int(os.getenv("API_PORT") or os.getenv("JC_PORT") or "8000")
    uvicorn.run(app, host=host, port=port, log_level="info")
