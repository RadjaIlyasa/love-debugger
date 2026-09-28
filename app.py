"""Main LoveDebugger application."""

import ctypes
import random
import sys
import tkinter as tk
from pathlib import Path

from assets import AssetManager
from config import WINDOW_BG, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from effects import Effects
from scenes import Scenes


class LoveDebugger:
    """Application shell that owns shared state and delegates behavior."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=WINDOW_BG)
        self.root.resizable(False, False)

        self._center_window()

        self.closing = False
        self.glitch_active = True
        self.blinking = False
        self.hearts_active = False
        self.shake_offset = (0, 0)
        self.random = random

        self.progress = 0
        self.diagnostic_index = 0
        self.investigation_index = 0
        self.investigation_progress = 0
        self.no_attempts = 0

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=WINDOW_BG,
            highlightthickness=0,
        )
        self.canvas.pack()

        assets_dir = Path(__file__).resolve().parent / "assets"
        self.assets = AssetManager(root, assets_dir)
        self.effects = Effects(self)
        self.scenes = Scenes(self)

        self._setup_dpi_awareness()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.effects.random_glitch()
        self.show_boot_screen()

    def _setup_dpi_awareness(self) -> None:
        if sys.platform != "win32":
            return

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    def _center_window(self) -> None:
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def close(self) -> None:
        """Stop scheduled animation states and close the application."""
        self.closing = True
        self.glitch_active = False
        self.blinking = False
        self.hearts_active = False
        self.root.destroy()

    def show_boot_screen(self) -> None:
        self.effects.draw_scanlines()

        self.canvas.create_text(
            300,
            150,
            text="LOVE DEBUGGER",
            fill="#58a6ff",
            font=("Consolas", 28, "bold"),
        )
        self.canvas.create_text(
            300,
            195,
            text="v1.0",
            fill="#8b949e",
            font=("Consolas", 12),
        )
        self.canvas.create_rectangle(
            150,
            300,
            450,
            320,
            fill="",
            outline="#30363d",
        )
        self.progress_bar = self.canvas.create_rectangle(
            150,
            300,
            150,
            320,
            fill="#58a6ff",
            outline="",
        )
        self.effects.typewriter(
            300,
            260,
            "Initializing system...",
            "#ffffff",
            ("Consolas", 14),
            callback=lambda: self.root.after(500, self.scenes.update_progress),
        )