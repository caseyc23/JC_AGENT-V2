import importlib
import sys
from types import ModuleType
from types import SimpleNamespace


def _make_fake_tk_modules():
    tk = ModuleType("tkinter")

    class StringVar:
        def __init__(self, value=""):
            self._v = value

        def get(self):
            return self._v

        def set(self, v):
            self._v = v

    class BooleanVar:
        def __init__(self, value=False):
            self._v = bool(value)

        def get(self):
            return self._v

        def set(self, v):
            self._v = bool(v)

    class Widget:
        def __init__(self, *a, **k):
            pass

        def grid(self, *a, **k):
            pass

        def pack(self, *a, **k):
            pass

        def config(self, *a, **k):
            pass

    class Entry(Widget):
        def __init__(self, parent=None, textvariable=None, **kw):
            self.textvariable = textvariable

        def get(self):
            return self.textvariable.get() if self.textvariable else ""

        def config(self, *a, **k):
            pass

    class Label(Widget):
        pass

    class Frame(Widget):
        pass

    class Button(Widget):
        pass

    class Checkbutton(Widget):
        pass

    class Tk(Widget):
        def __init__(self):
            self._w = 600
            self._h = 700
            self._sw = 1024
            self._sh = 768

        def title(self, *a):
            pass

        def geometry(self, *a):
            pass

        def resizable(self, *a):
            pass

        def configure(self, *a, **k):
            pass

        def update(self):
            pass

        def update_idletasks(self):
            pass

        def winfo_width(self):
            return self._w

        def winfo_height(self):
            return self._h

        def winfo_screenwidth(self):
            return self._sw

        def winfo_screenheight(self):
            return self._sh

        def mainloop(self):
            pass

    tk.StringVar = StringVar
    tk.BooleanVar = BooleanVar
    tk.Entry = Entry
    tk.Label = Label
    tk.Frame = Frame
    tk.Button = Button
    tk.Checkbutton = Checkbutton
    tk.Tk = Tk
    tk.BOTH = "both"
    tk.LEFT = "left"
    tk.FLAT = "flat"
    tk.RIGHT = "right"
    tk.TOP = "top"
    tk.W = "w"
    tk.X = "x"

    # ttk
    ttk = ModuleType("tkinter.ttk")

    class Combobox(Widget):
        def __init__(self, parent=None, textvariable=None, values=None, state=None, width=None, **kw):
            self.textvariable = textvariable

        def grid(self, *a, **k):
            pass

    ttk.Combobox = Combobox

    # messagebox
    messagebox = ModuleType("tkinter.messagebox")

    def _noop(*a, **k):
        return None

    messagebox.showinfo = _noop
    messagebox.showerror = _noop
    messagebox.showwarning = _noop

    return tk, ttk, messagebox


def test_test_connection_success(monkeypatch):
    tk, ttk, messagebox = _make_fake_tk_modules()
    sys.modules["tkinter"] = tk
    sys.modules["tkinter.ttk"] = ttk
    sys.modules["tkinter.messagebox"] = messagebox

    if "jc.settings_gui" in sys.modules:
        del sys.modules["jc.settings_gui"]

    settings_gui = importlib.import_module("jc.settings_gui")

    app = settings_gui.JCSettingsGUI()
    app.provider_var.set("openrouter")
    app.openrouter_key_var.set("ok-key")

    # Mock requests.get to simulate a 200 response
    def fake_get(url, headers=None, timeout=None):
        return SimpleNamespace(status_code=200)

    monkeypatch.setattr(settings_gui, "requests", SimpleNamespace(get=fake_get, exceptions=settings_gui.requests.exceptions))

    # Should not raise
    app._test_connection()


def test_test_connection_timeout(monkeypatch):
    tk, ttk, messagebox = _make_fake_tk_modules()
    sys.modules["tkinter"] = tk
    sys.modules["tkinter.ttk"] = ttk
    sys.modules["tkinter.messagebox"] = messagebox

    if "jc.settings_gui" in sys.modules:
        del sys.modules["jc.settings_gui"]

    settings_gui = importlib.import_module("jc.settings_gui")

    app = settings_gui.JCSettingsGUI()
    app.provider_var.set("openrouter")
    app.openrouter_key_var.set("ok-key")

    class FakeExceptions:
        class Timeout(Exception):
            pass

        class RequestException(Exception):
            pass

    def fake_get(url, headers=None, timeout=None):
        raise FakeExceptions.Timeout()

    monkeypatch.setattr(settings_gui, "requests", SimpleNamespace(get=fake_get, exceptions=FakeExceptions))

    # Should handle timeout without raising
    app._test_connection()
