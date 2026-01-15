import os
from pathlib import Path

from jc_self_awareness import JCSelfAwareness
from jc.settings_gui import is_valid_port, write_env_atomic, read_env_file


def test_self_awareness_runs_basic_diagnostic(tmp_path, monkeypatch):
    # Ensure no special keys set
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    sa = JCSelfAwareness()
    res = sa.run_full_diagnostic()
    assert isinstance(res, dict)
    # should contain expected keys
    assert "capabilities" in res


def test_settings_gui_env_write_and_read(tmp_path):
    env_file = tmp_path / ".env"
    content = "OPENAI_API_KEY=abc123\nJC_PORT=9000\n"
    write_env_atomic(env_file, content)
    got = read_env_file(env_file)
    assert got == content
    assert is_valid_port("8000")
    assert not is_valid_port("notaport")
