import tempfile
from pathlib import Path

import jc_settings_gui


def test_shim_exports_and_env_write_read():
    # Exported symbols exist and are callable
    assert callable(jc_settings_gui.write_env_atomic)
    assert callable(jc_settings_gui.is_valid_port)
    assert callable(jc_settings_gui.read_env_file)

    # is_valid_port behavior
    assert jc_settings_gui.is_valid_port("8080") is True
    assert jc_settings_gui.is_valid_port("0") is False
    assert jc_settings_gui.is_valid_port("notaport") is False

    # write_env_atomic + read_env_file integration
    with tempfile.TemporaryDirectory() as td:
        env_path = Path(td) / ".env_test"
        content = "JC_PROVIDER=openrouter\nJC_PORT=8000\n"

        # Should not raise
        jc_settings_gui.write_env_atomic(env_path, content)

        # File should exist and content should match
        assert env_path.exists()
        read = jc_settings_gui.read_env_file(env_path)
        assert read == content
