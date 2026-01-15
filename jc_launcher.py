#!/usr/bin/env python3
"""JC Agent Launcher - System Tray Application.

This module is importable (unlike .pyw) so other code can do `import jc_launcher`.
The Windows-friendly entrypoint remains `jc_launcher.pyw`.

The tray UI depends on optional packages:
  - pystray
  - pillow

If they are missing, we exit with a clear message instead of crashing on import.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, IO, cast

import requests


def _show_error(message: str, title: str = "JC Launcher") -> None:
    """Best-effort user-visible error message."""
    # Console output is always available.
    print(message, file=sys.stderr)

    # On Windows, also try a native message box.
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)  # MB_ICONERROR
        except Exception:
            pass


def _require_tray_deps() -> tuple[Any, Any, Any]:
    try:
        import pystray  # type: ignore
        from PIL import Image, ImageDraw  # type: ignore

        return cast(Any, pystray), cast(Any, Image), cast(Any, ImageDraw)
    except Exception as e:
        _show_error(
            "Tray dependencies are not installed.\n\n"
            "Install them with:\n"
            "  pip install pystray pillow\n\n"
            "Then re-run the launcher.",
            title="JC Launcher - Missing Dependencies",
        )
        raise SystemExit(1) from e


class JCLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "config.json"
        self.api_process: subprocess.Popen[Any] | None = None
        self.api_url = self._resolve_api_url()
        self.icon: Any | None = None
        self._api_log: IO[bytes] | None = None

    def _resolve_api_url(self) -> str:
        """Resolve API URL from config/env, with sane defaults."""
        if self.config_file.exists():
            try:
                cfg: dict[str, Any] = json.loads(self.config_file.read_text(encoding="utf-8"))
                api_cfg = cast(dict[str, Any], cfg.get("api") or {})
                host = str(api_cfg.get("host") or "localhost")
                port = int(api_cfg.get("port") or 8000)
                return f"http://{host}:{int(port)}"
            except Exception:
                pass

        host = os.getenv("API_HOST") or "localhost"
        port = os.getenv("API_PORT") or os.getenv("JC_PORT") or "8000"
        try:
            port_int = int(port)
        except Exception:
            port_int = 8000
        return f"http://{host}:{port_int}"

    def create_icon_image(self, color: str = "green") -> Any:
        """Create a simple icon for the system tray."""
        _pystray, Image, ImageDraw = _require_tray_deps()

        width = 64
        height = 64
        image = Image.new("RGB", (width, height), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)

        colors = {"green": (0, 255, 0), "yellow": (255, 255, 0), "red": (255, 0, 0)}
        text_color = colors.get(color, (0, 255, 0))

        draw.ellipse([10, 10, 54, 54], fill=text_color)
        draw.rectangle([20, 25, 44, 45], fill=(30, 30, 30))

        return image

    def check_api_status(self) -> bool:
        """Check if the API is running."""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def start_api_server(self) -> bool:
        """Start the FastAPI backend server."""
        if self.check_api_status():
            return True

        try:
            api_script = self.base_dir / "jc_agent_api.py"
            if not api_script.exists():
                # Backwards compatibility fallback (older repo layouts)
                api_script = self.base_dir / "agent_api.py"

            if not api_script.exists():
                _show_error(f"API script not found: {api_script}")
                return False

            # Avoid deadlocks from PIPE buffers (FastAPI/uvicorn can be chatty).
            log_path = self.base_dir / "jc_agent_api_subprocess.log"
            self._api_log = open(log_path, "ab")

            creationflags = 0
            if sys.platform == "win32":
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

            self.api_process = subprocess.Popen(
                [sys.executable, str(api_script)],
                cwd=str(self.base_dir),
                stdout=self._api_log,
                stderr=self._api_log,
                creationflags=creationflags,
            )

            # Wait briefly for startup.
            time.sleep(3)
            return self.check_api_status()
        except Exception as e:
            _show_error(f"Failed to start API: {e}")
            return False

    def stop_api_server(self) -> None:
        """Stop the API server."""
        if self.api_process:
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
            except Exception:
                try:
                    self.api_process.kill()
                except Exception:
                    pass
            self.api_process = None

        if self._api_log:
            try:
                self._api_log.close()
            except Exception:
                pass
            self._api_log = None

    def open_chat_interface(self, icon: Any, item: Any) -> None:
        """Open the chat interface in browser."""
        if not self.check_api_status():
            if not self.start_api_server():
                self.show_notification("Error", "Failed to start JC Agent")
                return

        webbrowser.open(f"{self.api_url}/chat")

    def run_command(self, icon: Any, item: Any) -> None:
        """Open CLI interface."""
        if sys.platform == "win32":
            subprocess.Popen(["cmd", "/k", sys.executable, "-m", "jc"], cwd=str(self.base_dir))
            return

        # Best-effort: try a terminal emulator, otherwise just run the CLI.
        try:
            subprocess.Popen(["gnome-terminal", "--", sys.executable, "-m", "jc"], cwd=str(self.base_dir))
        except Exception:
            subprocess.Popen([sys.executable, "-m", "jc"], cwd=str(self.base_dir))

    def open_settings(self, icon: Any, item: Any) -> None:
        """Open settings GUI."""
        settings_script = self.base_dir / "jc_settings_gui.py"
        if not settings_script.exists():
            self.show_notification("Settings Error", "Settings GUI script not found")
            return

        try:
            subprocess.Popen([sys.executable, str(settings_script)], cwd=str(self.base_dir))
        except Exception as e:
            self.show_notification("Settings Error", f"Failed to open settings: {e}")

    def check_status(self, icon: Any, item: Any) -> None:
        """Check and display agent status."""
        if self.check_api_status():
            self.show_notification("JC Agent", "✓ Online and ready")
        else:
            self.show_notification("JC Agent", "✗ Offline - Click to start")

    def show_notification(self, title: str, message: str) -> None:
        """Show system notification."""
        if self.icon:
            self.icon.notify(message, title)

    def quit_app(self, icon: Any, item: Any) -> None:
        """Quit the application."""
        self.stop_api_server()
        icon.stop()

    def run(self) -> None:
        """Run the system tray application."""
        pystray, _Image, _ImageDraw = _require_tray_deps()

        # Auto-start API on launch
        threading.Thread(target=self.start_api_server, daemon=True).start()

        menu = pystray.Menu(
            pystray.MenuItem("Open JC Chat", self.open_chat_interface, default=True),
            pystray.MenuItem("Run Command", self.run_command),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Check Status", self.check_status),
            pystray.MenuItem("Settings", self.open_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app),
        )

        icon = pystray.Icon(
            "jc_agent",
            self.create_icon_image(),
            "JC Agent - Your AI Business Partner",
            menu,
        )

        self.icon = icon
        icon.run()


def main() -> int:
    JCLauncher().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
