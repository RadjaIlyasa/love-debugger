"""Loading and storing LoveDebugger assets."""

from pathlib import Path
import tkinter as tk

from config import (
    CLICK_SOUND,
    EMINEM_FILES,
    ERROR_SOUND,
    STICKER_FILES,
)

try:
    import pygame
except ImportError:
    pygame = None

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class AssetManager:
    """Keeps all image/audio loading in one place."""

    def __init__(self, root: tk.Tk, assets_dir: Path) -> None:
        self.root = root
        self.assets_dir = assets_dir
        self.sfx_click = None
        self.sfx_error = None
        self.eminem_frames: list[tk.PhotoImage] = []
        self.stickers: dict[str, tk.PhotoImage] = {}
        self.fade_frames: list[tk.PhotoImage] = []

        self._load_audio()
        self._load_eminem_frames()
        self._load_stickers()
        self._build_fade_frames()

    def _load_audio(self) -> None:
        if pygame is None:
            return

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.sfx_click = self._load_sound(CLICK_SOUND, 0.30)
            self.sfx_error = self._load_sound(ERROR_SOUND, 0.55)
        except Exception:
            # Audio is an enhancement, not a hard dependency for the app.
            self.sfx_click = None
            self.sfx_error = None

    def _load_sound(self, filename: str, volume: float):
        path = self.assets_dir / filename
        if not path.exists():
            return None

        sound = pygame.mixer.Sound(str(path))
        sound.set_volume(volume)
        return sound

    def _load_eminem_frames(self) -> None:
        for filename in EMINEM_FILES:
            path = self.assets_dir / filename
            try:
                if path.exists():
                    self.eminem_frames.append(tk.PhotoImage(file=path))
            except tk.TclError:
                continue

    def _load_stickers(self) -> None:
        for key, filename in STICKER_FILES.items():
            path = self.assets_dir / filename
            try:
                if path.exists():
                    self.stickers[key] = tk.PhotoImage(file=path)
            except tk.TclError:
                continue

    def _build_fade_frames(self) -> None:
        if Image is None or ImageTk is None:
            return

        try:
            for i in range(7):
                alpha = int(255 * (i / 6))
                image = Image.new("RGBA", (600, 500), (13, 17, 23, alpha))
                self.fade_frames.append(ImageTk.PhotoImage(image))
        except Exception:
            self.fade_frames = []
