import os
import stat
import sys
from pathlib import Path

import pytest

from jc_settings_gui import write_env_atomic, is_valid_port, read_env_file


def test_write_env_atomic_and_permissions(tmp_path):
    env_path = tmp_path / ".env"
    content = "JC_PROVIDER=openrouter\nJC_PORT=8000\n"
    write_env_atomic(env_path, content)
    assert env_path.exists()
    read = env_path.read_text()
    assert content == read
    if sys.platform != "win32":
        st = os.stat(env_path)
        assert (st.st_mode & 0o777) == 0o600


def test_is_valid_port():
    assert is_valid_port("8000")
    assert not is_valid_port("0")
    assert not is_valid_port("70000")
    assert not is_valid_port("notaport")


def test_read_env_file_returns_none_for_missing(tmp_path):
    env_path = tmp_path / ".env"
    assert read_env_file(env_path) is None
