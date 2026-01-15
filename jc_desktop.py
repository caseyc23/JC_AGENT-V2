#!/usr/bin/env python3
"""JC Desktop - Taskbar/tray GUI for your AI business partner.

Notes:
- This module intentionally does NOT auto-install GUI dependencies.
- PyQt6 is imported lazily so importing this file won't break headless environments.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from typing import Any, IO

import requests


def _show_error(message: str, title: str = "JC Desktop") -> None:
    print(message, file=sys.stderr)
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)  # MB_ICONERROR
        except Exception:
            pass


def _require_pyqt6():
    try:
        from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
        from PyQt6.QtGui import QAction
        from PyQt6.QtCore import QTimer

        return QApplication, QSystemTrayIcon, QMenu, QAction, QTimer
    except Exception as e:
        _show_error(
            "PyQt6 is not installed.\n\n"
            "Install optional UI dependencies with:\n"
            "  pip install -r requirements-ui.txt\n\n"
            "Or install just PyQt6:\n"
            "  pip install PyQt6\n",
            title="JC Desktop - Missing Dependencies",
        )
        raise RuntimeError("PyQt6 is required to run the desktop tray UI") from e


def _resolve_api_url(base_dir: Path) -> str:
    cfg_path = base_dir / "config.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            api_cfg = (cfg.get("api") or {}) if isinstance(cfg, dict) else {}
            host = api_cfg.get("host") or "localhost"
            port = api_cfg.get("port") or 8000
            return f"http://{host}:{int(port)}"
        except Exception:
            pass

    host = os.getenv("API_HOST") or "127.0.0.1"
    port = os.getenv("API_PORT") or os.getenv("JC_PORT") or "8000"
    try:
        port_int = int(port)
    except Exception:
        port_int = 8000
    return f"http://{host}:{port_int}"


class JCDesktop:
    def __init__(self):
        QApplication, QSystemTrayIcon, QMenu, QAction, QTimer = _require_pyqt6()
        self._QApplication = QApplication
        self._QSystemTrayIcon = QSystemTrayIcon
        self._QMenu = QMenu
        self._QAction = QAction
        self._QTimer = QTimer

        self.base_dir = Path(__file__).parent
        self.api_url = _resolve_api_url(self.base_dir)

        self._server_log: IO[bytes] | None = None
        self.server_process: subprocess.Popen[Any] | None = None

        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Start API server in background
        self.start_server()

        # Create system tray icon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.app.style().standardIcon(self.app.style().StandardPixmap.SP_ComputerIcon))
        self.tray.setVisible(True)
        self.tray.setToolTip("JC-Agent - Your Business Partner")

        # Create menu
        menu = QMenu()

        open_dashboard = QAction("Open JC Dashboard", self.app)
        open_dashboard.triggered.connect(self.open_dashboard)
        menu.addAction(open_dashboard)

        status_action = QAction("Check Status", self.app)
        status_action.triggered.connect(self.check_status)
        menu.addAction(status_action)

        menu.addSeparator()

        quit_action = QAction("Quit JC", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_click)

        # Check server status periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5000)  # Check every 5 seconds

        self.tray.showMessage(
            "JC-Agent Started",
            "Your AI business partner is ready!",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )

    def _check_api_status(self) -> bool:
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def start_server(self) -> None:
        """Start the FastAPI server (if not already running)."""
        if self._check_api_status():
            return

        try:
            server_script = self.base_dir / ("jc_agent_api.py" if (self.base_dir / "jc_agent_api.py").exists() else "agent_api.py")
            if not server_script.exists():
                _show_error(f"Server script not found: {server_script}")
                return

            log_path = self.base_dir / "jc_desktop_server.log"
            self._server_log = open(log_path, "ab")

            creationflags = 0
            if sys.platform == "win32":
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

            self.server_process = subprocess.Popen(
                [sys.executable, str(server_script)],
                stdout=self._server_log,
                stderr=self._server_log,
                cwd=self.base_dir,
                creationflags=creationflags,
            )

            time.sleep(2)
        except Exception as e:
            _show_error(f"Error starting server: {e}")

    def open_dashboard(self) -> None:
        """Open JC dashboard in browser."""
        webbrowser.open(f"{self.api_url}/docs")

    def check_status(self) -> None:
        """Check if JC is running."""
        QSystemTrayIcon = self._QSystemTrayIcon

        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            if response.status_code == 200:
                data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                self.tray.showMessage(
                    "JC Status: Online",
                    f"Provider: {data.get('provider')}\nModel: {data.get('model')}",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000,
                )
            else:
                self.tray.showMessage(
                    "JC Status: Error",
                    "Server responded with error",
                    QSystemTrayIcon.MessageIcon.Warning,
                    3000,
                )
        except Exception:
            self.tray.showMessage(
                "JC Status: Offline",
                "Server not responding",
                QSystemTrayIcon.MessageIcon.Critical,
                3000,
            )

    def update_status(self) -> None:
        """Update tray tooltip based on server status."""
        if self._check_api_status():
            self.tray.setToolTip("JC-Agent - Online")
        else:
            self.tray.setToolTip("JC-Agent - Starting...")

    def on_tray_click(self, reason: Any) -> None:
        """Handle tray icon clicks."""
        QSystemTrayIcon = self._QSystemTrayIcon
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.open_dashboard()

    def quit_app(self) -> None:
        """Quit the application."""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except Exception:
                try:
                    self.server_process.kill()
                except Exception:
                    pass

        if self._server_log:
            try:
                self._server_log.close()
            except Exception:
                pass

        self.app.quit()

    def run(self) -> int:
        """Run the application."""
        return int(self.app.exec())


def main() -> int:
    jc = JCDesktop()
    return jc.run()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError:
        raise SystemExit(1)
