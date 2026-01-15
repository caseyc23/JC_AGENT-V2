# JC-Agent - AI Coding Agent Instructions

JC-Agent is an enterprise-grade autonomous AI agent framework with FastAPI backend, multi-provider LLM support, and comprehensive system integration. Named in memory of a friend, JC combines professional-grade engineering with a personal touch.

## Architecture Overview

### Core Structure

```
jc/                     # Core package (production code)
├── __init__.py        # JC runtime, JCState, main orchestration
├── api.py             # FastAPI routes (imported by jc_agent_api.py)
├── llm_provider.py    # Multi-provider LLM abstraction layer
├── secrets.py         # Safe credential loading (.env, environment)
├── brain.py           # Memory, learning, user profile (SQLite)
├── personality.py     # JC_IDENTITY, voice commands, memorial
├── voice.py           # Speech recognition/synthesis integration
├── research.py        # Web scraping, search aggregation
├── third_party.py     # Integration with external repos/tools
└── ...                # Other modules (guardrails, hallucination detection, etc.)

jc_agent_api.py        # Production FastAPI server entrypoint
agent_api.py           # DEPRECATED - redirects to jc_agent_api.py
jc.py                  # CLI shim: delegates to `python -m jc`
jc_*.py                # Legacy standalone modules (gradually refactored into jc/)
```

### Key Architectural Decisions

1. **Package Migration**: Code is being migrated from `jc_*.py` standalone files into the `jc/` package for better modularity and reusability. When modifying functionality, prefer editing `jc/*.py` over legacy files.

2. **Lazy Imports**: Heavy dependencies (voice, web clients) are imported lazily in `jc/__init__.py` to keep startup fast and avoid requiring optional dependencies.

3. **Local-First Design**: All processing runs locally on user's machine (target: Asus Zenbook Duo). External APIs are opt-in with user-provided keys.

4. **Deliberate Workflow**: JC asks clarifying questions before acting. The `/ask-questions` mode generates prioritized lists of requirements/constraints/dependencies.

## Developer Workflows

### Installation & Setup

```bash
# Quick setup (Windows)
install_windows.bat          # Installs deps, creates desktop shortcut, adds to startup

# Manual setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python jc_settings_gui.py    # Configure API keys (GUI with masking)
```

### Running the Server

```bash
python jc_agent_api.py                    # Development server (localhost:8000)
uvicorn jc_agent_api:app --reload        # Auto-reload on changes
python -m jc                              # CLI interface
```

### Running Tests

```bash
pytest                                    # All tests
pytest tests/test_jc_settings_gui.py      # Specific module
pytest -v -s                              # Verbose with stdout
```

### Configuration Files

- `.env`: API keys (never commit! Use `.env.example` as template)
- `config.json`: Fine-tuned LLM parameters, system settings
- `jc_data/`: SQLite database for memory/learning
- `pyrightconfig.json`: Type checking configuration (Pyright, Python 3.12)

## Critical Patterns & Conventions

### Secrets Management

**NEVER hardcode API keys**. Always use environment variables:

```python
from jc.secrets import load_env, get_llm_api_key

load_env()  # Loads .env file if present
api_key = get_llm_api_key()  # Prefers OPENAI_API_KEY, falls back to OPENROUTER_API_KEY
```

Preference order: `OPENAI_API_KEY` → `OPENROUTER_API_KEY`. See [jc/secrets.py](jc/secrets.py) for full logic.

### LLM Provider Abstraction

Use the unified provider interface in [jc/llm_provider.py](jc/llm_provider.py). Supports OpenRouter, Ollama, OpenAI, Hugging Face:

```python
from jc.llm_provider import get_llm_provider

provider = get_llm_provider()
response = await provider.chat_completion(messages, model="openai/gpt-4o-mini")
```

### Memory & Learning

JC uses SQLite (`jc_data/brain.db`) for persistent memory. See [jc/brain.py](jc/brain.py):

- `JCBrain.log_conversation()`: Records interactions
- `JCBrain.get_personality_prompt()`: Adapts personality based on learned patterns
- `UserProfile`: Tracks preferences, communication style

### Type Safety

- Pydantic models for data validation (`JCState`, API request/response models)
- Type hints throughout (Python 3.8+ compatible)
- Pyright configured for basic type checking (see `pyrightconfig.json`)

### Logging

Consistent logging pattern:

```python
import logging
logger = logging.getLogger('JC')
logger.info("Action message", extra={"user_id": user.id})
```

Logs write to `jc_agent.log` + stdout (see `jc/__init__.py`).

## Integration Points

### Third-Party Repos

Managed via [integrations/third_party.json](integrations/third_party.json) and [jc/third_party.py](jc/third_party.py). To add new integrations:

1. Add entry to `integrations/third_party.json` with repo URL, license, description
2. Run `python scripts/update_third_party.py` to clone/update repos
3. Extract documentation with `python scripts/extract_third_party_docs.py`

**License Compliance**: Avoid embedding AGPL code directly. Reference or link to permissively licensed implementations.

### Desktop Application

[jc_desktop.py](jc_desktop.py) provides system tray integration (double-click → dashboard, right-click → menu). Auto-starts via `setup_autostart.bat`.

### Voice Interface

[jc/voice.py](jc/voice.py) wraps SpeechRecognition (input) and pyttsx3/ElevenLabs (output). Disabled by default; enable via `ENABLE_VOICE=true` in `.env`.

## Work-in-Progress Features

### Observability (Phase 1, Q1 2026)

- OpenTelemetry tracing planned (see [ROADMAP.md](ROADMAP.md))
- No production tracing/metrics yet

### "Remember This?" Mode

From requirements worklog:

- Default: JC doesn't persist new material unless explicitly told
- Planned: tagging system (research, build, decision), pinned vs transient storage
- Cleanup: dry-run reports before deletion, soft-delete with undo window

### "Watch Me Work"

Planned safe observability via VS Code extension + CLI file watcher (no OS-level keystroke logging). See requirements doc for details.

## Testing Strategy

See [TEST_GUIDE.md](TEST_GUIDE.md). Key patterns:

- Mocked LLM responses for deterministic tests
- Headless GUI testing (tkinter with `Toplevel`)
- Integration tests validate FastAPI endpoints
- `conftest.py` provides shared fixtures

## Common Pitfalls

1. **Don't bypass the secrets module**: Always use `jc.secrets.get_llm_api_key()` instead of direct `os.getenv()` calls
2. **Don't use deprecated entrypoints**: Use `jc_agent_api.py` not `agent_api.py`
3. **Don't commit .env**: Verify `.gitignore` excludes secrets before commits
4. **Don't assume all dependencies are installed**: Wrap optional imports in try/except (voice, research modules)
5. **Don't hard-delete user data**: Implement soft-delete with undo windows (per requirements)

## Quick Reference

- **API Docs**: Run server, visit http://localhost:8000/docs (FastAPI auto-generated)
- **Main Work Log**: Work logs stored in artifacts repo (`caseyc23_JC-agent-_files`)
- **Type Checking**: `pyright` or `mypy` (configured in `pyrightconfig.json`)
- **Code Style**: Follow existing patterns, prefer explicit over implicit

## When Making Changes

1. **Verify you're in the correct repo**: This is `JC-agent-` (source code). Artifacts live in `caseyc23_JC-agent-_files`.
2. **Check requirements docs first**: Ensure changes align with documented requirements and sequential task order.
3. **Test locally**: Run affected tests before committing (`pytest tests/test_*.py`).
4. **Update docs**: If changing APIs or workflows, update README.md or relevant .md files.
5. **Respect the memorial**: JC is named for someone who mattered. Keep the code professional and the tribute intact.
