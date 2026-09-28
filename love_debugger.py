import tkinter as tk
import random
import os
import sys
import ctypes

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# --- Windows high-DPI awareness for crisp text rendering ---
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

# --- Change this to customize the subject name shown on the
# result screen (e.g. TARGET_NAME = "Sana"). ---
TARGET_NAME = "YOU"


class LoveDebugger:
    def __init__(self, root):
        self.root = root

        self.root.title("LoveDebugger")
        self.root.geometry("600x500")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        # Center window on screen
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 600) // 2
        y = (sh - 500) // 2
        self.root.geometry(f"600x500+{x}+{y}")

        # Clean shutdown flag
        self._closing = False
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # =========================
        # BOOT
        # =========================

        self.progress = 0

        # =========================
        # DIAGNOSTIC
        # =========================

        self.diagnostics = [
            "Checking CPU.......... OK",
            "Checking RAM.......... OK",
            "Checking Database.......... OK",
            "Checking Network.......... OK",
            "Checking emotional state. ERROR",
        ]

        self.diagnostic_index = 0

        # =========================
        # INVESTIGATION
        # =========================

        self.investigation = [
            "> Starting investigation...",
            "> Scanning recent interactions...",
            "> Analyzing behavioral patterns...",
            "> Cross-referencing emotional data...",
            "> Identifying source..."
        ]

        self.investigation_index = 0
        self.investigation_progress = 0
        self.no_attempts = 0

        # flag buat matiin loop glitch flash pas masuk scene final
        self.glitch_active = True

        # Initialize shake offset so clear_screen can always reset it
        self._shake_offset = (0, 0)

        # =========================
        # CANVAS
        # =========================

        self.canvas = tk.Canvas(
            root,
            width=600,
            height=500,
            bg="#0d1117",
            highlightthickness=0
        )

        self.canvas.pack()

        # =========================
        # ASSETS DIRECTORY
        # =========================

        assets_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets"
        )

        # =========================
        # AUDIO (SFX)
        # =========================

        self.sfx_click = None
        self.sfx_error = None
        try:
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            click_path = os.path.join(assets_dir, "click.wav")
            error_path = os.path.join(assets_dir, "error.wav")
            if os.path.exists(click_path):
                self.sfx_click = pygame.mixer.Sound(click_path)
                self.sfx_click.set_volume(0.3)
            if os.path.exists(error_path):
                self.sfx_error = pygame.mixer.Sound(error_path)
                self.sfx_error.set_volume(0.55)
        except Exception:
            pass

        # =========================
        # FADE TRANSITION ASSETS
        # =========================

        self.fade_frames = []
        if HAS_PIL:
            try:
                # 7 alpha steps from 0 to 255 for smooth fade-in/fade-out
                for i in range(7):
                    alpha = int(255 * (i / 6))
                    img = Image.new("RGBA", (600, 500), (13, 17, 23, alpha))
                    self.fade_frames.append(ImageTk.PhotoImage(img))
            except Exception:
                self.fade_frames = []

        # =========================
        # MEME ASSETS & STICKERS
        # =========================

        # frame-frame Eminem buat efek "pop" (kecil -> besar) pas
        # scene "Will you be mine?"
        try:
            self.eminem_frames = [
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_40.png")),
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_65.png")),
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_90.png")),
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_115.png")),
            ]
        except Exception:
            self.eminem_frames = []

        # Dictionary sticker reaksi yang luas untuk eskalasi tombol NO
        sticker_files = {
            "side_eye": "side_eye.png",
            "raised_eyebrow": "raised_eyebrow.png",
            "clown": "clown.png",
            "crying_barbie": "crying_barbie.png",
            "pleading_face": "pleading_face.png",
            "crying_cat": "crying_cat.png",
            "donkey_face": "donkey_face.png",
            "loudly_crying": "loudly_crying.png",
            "skull": "skull.png",
            "broken_heart": "broken_heart.png",
        }

        self.stickers = {}
        for key, fname in sticker_files.items():
            path = os.path.join(assets_dir, fname)
            try:
                if os.path.exists(path):
                    self.stickers[key] = tk.PhotoImage(file=path)
            except Exception:
                pass

        # mulai loop glitch flash (jalan terus sepanjang app hidup)
        self.random_glitch()

        self.show_boot_screen()

    # =========================
    # AUDIO HELPERS
    # =========================

    def play_typing_sfx(self):
        if self.sfx_click and not self._closing:
            try:
                self.sfx_click.play()
            except Exception:
                pass

    def play_error_sfx(self):
        if self.sfx_error and not self._closing:
            try:
                self.sfx_error.play()
            except Exception:
                pass

    # =========================
    # FADE TRANSITION
    # =========================

    def fade_to(self, callback, step_ms=20):
        """Transisi fade-to-black halus antar scene."""
        if self._closing or not self.fade_frames:
            callback()
            return

        overlay = self.canvas.create_image(0, 0, anchor="nw", image=self.fade_frames[0])

        def step_out(idx):
            if self._closing:
                return
            if idx < len(self.fade_frames):
                self.canvas.itemconfig(overlay, image=self.fade_frames[idx])
                self.canvas.tag_raise(overlay)
                self.root.after(step_ms, lambda: step_out(idx + 1))
            else:
                # Layar sudah gelap penuh, load scene baru
                callback()
                # Buat overlay baru di atas konten baru, lalu fade in
                in_overlay = self.canvas.create_image(0, 0, anchor="nw", image=self.fade_frames[-1])
                step_in(in_overlay, len(self.fade_frames) - 1)

        def step_in(in_overlay, idx):
            if self._closing:
                return
            if idx >= 0:
                self.canvas.itemconfig(in_overlay, image=self.fade_frames[idx])
                self.canvas.tag_raise(in_overlay)
                self.root.after(step_ms, lambda: step_in(in_overlay, idx - 1))
            else:
                self.canvas.delete(in_overlay)

        step_out(0)

    # =========================
    # CLEAN SHUTDOWN
    # =========================

    def _on_close(self):
        """Stop all animation loops and destroy the window cleanly."""
        self._closing = True
        self.glitch_active = False
        if hasattr(self, "blinking"):
            self.blinking = False
        if hasattr(self, "hearts_active"):
            self.hearts_active = False
        self.root.destroy()

    # =========================
    # CLEAR SCREEN
    # =========================

    def clear_screen(self):
        self.canvas.delete("all")
        self._shake_offset = (0, 0)
        self.draw_scanlines()

    # =========================
    # SCANLINE (background texture)
    # =========================

    def draw_scanlines(self):
        for y in range(0, 500, 4):
            self.canvas.create_line(
                0, y, 600, y,
                fill="#141a24",
                tags="scanline"
            )
        self.canvas.tag_lower("scanline")

    # =========================
    # GLITCH FLASH (random, jalan independen dari scene)
    # =========================

    def random_glitch(self):
        if self._closing:
            return

        if not self.glitch_active:
            return

        y = random.randint(0, 500)
        glitch_color = random.choice(["#58a6ff", "#ff5555", "#ffffff"])

        glitch_line = self.canvas.create_line(
            0, y, 600, y,
            fill=glitch_color,
            width=random.choice([1, 2, 3]),
            tags="glitch"
        )

        self.root.after(
            random.randint(40, 100),
            lambda: self.canvas.delete(glitch_line) if not self._closing else None
        )

        self.root.after(
            random.randint(800, 2500),
            self.random_glitch
        )

    # =========================
    # TYPEWRITER EFFECT
    # =========================

    def typewriter(self, x, y, full_text, fill, font, callback=None, delay=22):
        if self._closing:
            return
        item = self.canvas.create_text(x, y, text="", fill=fill, font=font)
        self._type_step(item, full_text, 1, delay, callback)

    def _type_step(self, item, full_text, index, delay, callback):
        if self._closing:
            return

        self.canvas.itemconfig(item, text=full_text[:index])

        # Suara ketik setiap 2 karakter untuk ritme mekanikal yang pas
        if index % 2 == 1:
            self.play_typing_sfx()

        if index < len(full_text):
            self.root.after(
                delay,
                lambda: self._type_step(item, full_text, index + 1, delay, callback)
            )
        elif callback:
            callback()

    # =========================
    # SCREEN SHAKE EFFECT
    # =========================

    def shake_screen(self, frames_left, magnitude=6):
        if self._closing:
            return

        if frames_left <= 0:
            ox, oy = self._shake_offset
            self.canvas.move("all", -ox, -oy)
            self._shake_offset = (0, 0)
            return

        new_x = random.randint(-magnitude, magnitude)
        new_y = random.randint(-magnitude, magnitude)
        ox, oy = self._shake_offset

        self.canvas.move("all", new_x - ox, new_y - oy)
        self._shake_offset = (new_x, new_y)

        self.root.after(40, lambda: self.shake_screen(frames_left - 1, magnitude))

    # =========================
    # BOOT PROGRESS
    # =========================

    def update_progress(self):
        if self._closing:
            return

        self.progress += 2

        width = 300 * (self.progress / 100)

        self.canvas.coords(
            self.progress_bar,
            150,
            300,
            150 + width,
            320
        )

        if self.progress < 100:
            self.root.after(50, self.update_progress)
        else:
            self.root.after(500, lambda: self.fade_to(self.run_diagnostics))

    # =========================
    # DIAGNOSTIC
    # =========================

    def run_diagnostics(self):
        if self._closing:
            return

        if self.diagnostic_index == 0:
            self.clear_screen()
            self.canvas.create_text(
                300,
                100,
                text="SYSTEM DIAGNOSTIC",
                fill="#58a6ff",
                font=("Consolas", 20, "bold")
            )

        diagnostic = self.diagnostics[self.diagnostic_index]

        if "ERROR" in diagnostic:
            color = "#ff5555"
            self.play_error_sfx()
        else:
            color = "#ffffff"

        def next_diagnostic():
            self.diagnostic_index += 1
            if self.diagnostic_index < len(self.diagnostics):
                self.root.after(150, self.run_diagnostics)
            else:
                self.root.after(1000, lambda: self.fade_to(self.show_anomaly))

        self.typewriter(
            300,
            180 + (self.diagnostic_index * 35),
            "> " + diagnostic,
            color,
            ("Consolas", 12),
            callback=next_diagnostic
        )

    # =========================
    # ANOMALY
    # =========================

    def show_anomaly(self):
        if self._closing:
            return

        self.clear_screen()

        self.anomaly_text = self.canvas.create_text(
            300,
            150,
            text="⚠ ANOMALY DETECTED",
            fill="#ff5555",
            font=("Consolas", 20, "bold")
        )

        self.canvas.create_line(
            180,
            180,
            420,
            180,
            fill="#30363d"
        )

        self.canvas.create_text(
            300,
            220,
            text="Possible cause:",
            fill="#8b949e",
            font=("Consolas", 12)
        )

        self.canvas.create_text(
            300,
            260,
            text="Someone has occupied your thoughts.",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.blinking = True

        # Layar berguncang & error sound saat anomaly terdeteksi
        self.play_error_sfx()
        self.shake_screen(frames_left=10, magnitude=6)

        self.root.after(500, self.blink_anomaly)
        self.root.after(2000, lambda: self.fade_to(self.run_investigation))

    # =========================
    # ANOMALY BLINK
    # =========================

    def blink_anomaly(self, state=True):
        if self._closing:
            return

        if not self.blinking:
            return

        color = "#ff5555" if state else "#0d1117"

        self.canvas.itemconfig(
            self.anomaly_text,
            fill=color
        )
        self.root.after(
            300,
            lambda: self.blink_anomaly(not state)
        )

    # =========================
    # INVESTIGATION
    # =========================

    def run_investigation(self):
        if self._closing:
            return

        self.blinking = False

        if self.investigation_index == 0:
            self.clear_screen()

            self.canvas.create_text(
                300,
                100,
                text="INVESTIGATION",
                fill="#58a6ff",
                font=("Consolas", 20, "bold")
            )

            self.canvas.create_text(
                300,
                150,
                text="Scanning target...",
                fill="#8b949e",
                font=("Consolas", 12)
            )

            # Progress bar trough
            self.canvas.create_rectangle(
                150, 180, 450, 200,
                fill="",
                outline="#30363d"
            )

            self.investigation_bar = self.canvas.create_rectangle(
                150,
                180,
                150,
                200,
                fill="#58a6ff",
                outline=""
            )

        self.investigation_progress += 20

        width = 300 * (
            self.investigation_progress / 100
        )

        self.canvas.coords(
            self.investigation_bar,
            150,
            180,
            150 + width,
            200
        )

        investigation = self.investigation[
            self.investigation_index
        ]

        def next_investigation():
            self.investigation_index += 1
            if self.investigation_index < len(self.investigation):
                self.root.after(150, self.run_investigation)
            else:
                self.root.after(1000, lambda: self.fade_to(self.show_result))

        self.typewriter(
            300,
            250 + (self.investigation_index * 25),
            investigation,
            "#ffffff",
            ("Consolas", 12),
            callback=next_investigation
        )

    # =========================
    # RESULT
    # =========================

    def show_result(self):
        if self._closing:
            return

        self.clear_screen()

        self.canvas.create_text(
            300,
            150,
            text="TARGET IDENTIFIED",
            fill="#58a6ff",
            font=("Consolas", 20, "bold")
        )

        self.canvas.create_text(
            300,
            200,
            text=f"Subject: {TARGET_NAME}",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.confidence_text = self.canvas.create_text(
            300,
            230,
            text="Confidence: 0.0%",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.animate_confidence(0.0)

    def animate_confidence(self, current):
        if self._closing:
            return

        target = 98.7
        current = min(current + 3.5, target)

        self.canvas.itemconfig(
            self.confidence_text,
            text=f"Confidence: {current:.1f}%"
        )

        if current < target:
            self.root.after(25, lambda: self.animate_confidence(current))
        else:
            self.canvas.create_text(
                300,
                280,
                text="Conclusion:",
                fill="#8b949e",
                font=("Consolas", 13)
            )

            self.canvas.create_text(
                300,
                310,
                text="You are in love.",
                fill="#ff5555",
                font=("Consolas", 16, "bold")
            )

            self.root.after(2000, lambda: self.fade_to(self.show_confession))

    # =========================
    # CONFESSION
    # =========================

    def show_confession(self):
        if self._closing:
            return

        self.clear_screen()

        self.no_meme_item = None

        if hasattr(self, "yes_button") and self.yes_button.winfo_exists():
            self.yes_button.destroy()
        if hasattr(self, "no_button") and self.no_button.winfo_exists():
            self.no_button.destroy()

        self.canvas.create_text(
            300,
            90,
            text="FINAL QUESTION",
            fill="#58a6ff",
            font=("Consolas", 20, "bold")
        )

        self.canvas.create_text(
            300,
            140,
            text="After analyzing all available data...",
            fill="#8b949e",
            font=("Consolas", 12)
        )

        self.canvas.create_text(
            300,
            170,
            text="I have reached one conclusion.",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.canvas.create_text(
            300,
            215,
            text="Will you be mine?",
            fill="#ff5555",
            font=("Consolas", 20, "bold")
        )

        if self.eminem_frames:
            self.animate_eminem_pop(0)

        self.no_message = self.canvas.create_text(
            300,
            450,
            text="",
            fill="#ff5555",
            font=("Consolas", 12)
        )

        # =========================
        # YES BUTTON
        # =========================

        self.yes_button = tk.Button(
            self.root,
            text="YES",
            font=("Consolas", 12, "bold"),
            bg="#238636",
            fg="white",
            activebackground="#2ea043",
            activeforeground="white",
            relief="flat",
            width=10,
            command=self.answer_yes
        )

        self.yes_button.place(
            x=180,
            y=380
        )

        # =========================
        # NO BUTTON
        # =========================

        self.no_button = tk.Button(
            self.root,
            text="NO",
            font=("Consolas", 12, "bold"),
            bg="#da3633",
            fg="white",
            activebackground="#f85149",
            activeforeground="white",
            relief="flat",
            width=10,
            takefocus=False,
            command=self.answer_no
        )

        self.no_button.place(
            x=320,
            y=380
        )

        self.no_button.bind(
            "<Enter>",
            self.move_no_button
        )

    # =========================
    # EMINEM POP ANIMATION
    # =========================

    def animate_eminem_pop(self, index):
        if self._closing or not self.eminem_frames:
            return

        if index == 0:
            self.eminem_img_item = self.canvas.create_image(
                300, 305,
                image=self.eminem_frames[0]
            )
        else:
            self.canvas.itemconfig(
                self.eminem_img_item,
                image=self.eminem_frames[index]
            )

        if index < len(self.eminem_frames) - 1:
            self.root.after(70, lambda: self.animate_eminem_pop(index + 1))

    def move_no_button(self, event):
        if self._closing:
            return

        self.no_attempts += 1

        # Eskalasi pesan & variasi stiker yang jauh lebih kaya
        if self.no_attempts == 1:
            message = "Nice try."
            sticker = self.stickers.get("side_eye")
        elif self.no_attempts == 2:
            message = "Still trying!"
            sticker = self.stickers.get("raised_eyebrow")
        elif self.no_attempts == 3:
            message = "Bro... seriously?"
            sticker = self.stickers.get("clown")
        elif self.no_attempts == 4:
            message = "Bro... you really said NO?"
            sticker = self.stickers.get("crying_barbie")
        elif self.no_attempts == 5:
            message = "I'm not giving up."
            sticker = self.stickers.get("pleading_face")
        elif self.no_attempts == 6:
            message = "You're running out of options."
            sticker = self.stickers.get("crying_cat")
        elif self.no_attempts == 7:
            message = "Just click YES already!"
            sticker = self.stickers.get("donkey_face")
        elif self.no_attempts == 8:
            message = "Why do you hurt me like this?"
            sticker = self.stickers.get("loudly_crying")
        else:
            message = "There is only one answer."
            sticker = self.stickers.get("skull") or self.stickers.get("broken_heart")

        # Zona eksklusi agar tombol NO tidak menutupi tombol YES
        yes_x, yes_y = 180, 380
        yes_w, yes_h = 100, 40

        for _ in range(25):
            new_x = random.randint(0, 500)
            new_y = random.randint(0, 440)
            if not (yes_x - 100 < new_x < yes_x + yes_w
                    and yes_y - 40 < new_y < yes_y + yes_h):
                break

        self.no_button.place(
            x=new_x,
            y=new_y
        )

        self.canvas.itemconfig(
            self.no_message,
            text=message
        )

        # Tombol YES bertambah besar bertahap
        try:
            current_width = self.yes_button.cget("width")
            if current_width < 18:
                self.yes_button.config(width=current_width + 1)
        except Exception:
            pass

        # Tampilkan stiker meme reaksi di samping pesan
        if sticker:
            self.show_no_meme(sticker)

    def show_no_meme(self, image):
        if self._closing or image is None:
            return

        message_coords = self.canvas.bbox(self.no_message)
        if not message_coords:
            return

        sticker_x_offset = 40
        sticker_y_offset = 5

        x = message_coords[2] + sticker_x_offset
        y = (message_coords[1] + message_coords[3]) // 2 + sticker_y_offset

        # Cegah keluar canvas di sisi kanan / kiri
        if x > 560:
            x = max(50, message_coords[0] - 40)

        if self.no_meme_item is None:
            self.no_meme_item = self.canvas.create_image(
                x,
                y,
                image=image
            )
        else:
            self.canvas.coords(
                self.no_meme_item,
                x,
                y
            )
            self.canvas.itemconfig(
                self.no_meme_item,
                image=image
            )

    def answer_no(self):
        if self._closing:
            return

        self.play_error_sfx()
        self.no_button.destroy()

        self.canvas.create_text(
            300,
            420,
            text="ERROR: Response rejected.",
            fill="#ff5555",
            font=("Consolas", 11)
        )

        self.root.after(
            1000,
            lambda: self.fade_to(self.show_confession)
        )

    # =========================
    # YES
    # =========================

    def answer_yes(self):
        if self._closing:
            return

        if hasattr(self, "yes_button") and self.yes_button.winfo_exists():
            self.yes_button.destroy()
        if hasattr(self, "no_button") and self.no_button.winfo_exists():
            self.no_button.destroy()

        self.glitch_active = False

        self.clear_screen()

        self.canvas.create_text(
            300,
            180,
            text="✓ CONNECTION ESTABLISHED",
            fill="#58a6ff",
            font=("Consolas", 20, "bold")
        )

        self.canvas.create_text(
            300,
            240,
            text="LoveDebugger has detected",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.canvas.create_text(
            300,
            270,
            text="a successful response.",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.canvas.create_text(
            300,
            340,
            text="♥",
            fill="#ff5555",
            font=("Consolas", 40, "bold")
        )

        self.hearts_active = True
        self.spawn_hearts()

    # =========================
    # FLOATING HEARTS EFFECT
    # =========================

    def spawn_hearts(self):
        if self._closing:
            return

        if not self.hearts_active:
            return

        for _ in range(random.randint(1, 2)):
            x = random.randint(30, 570)
            size = random.randint(14, 30)
            color = random.choice(["#ff5555", "#ff8080", "#ffb3b3"])

            heart = self.canvas.create_text(
                x, 510,
                text="♥",
                fill=color,
                font=("Consolas", size, "bold")
            )

            speed = random.uniform(1.0, 2.5)
            drift = random.uniform(-0.6, 0.6)
            self.animate_heart(heart, speed, drift)

        self.root.after(300, self.spawn_hearts)

    def animate_heart(self, heart, speed, drift):
        if self._closing:
            return

        self.canvas.move(heart, drift, -speed)
        coords = self.canvas.coords(heart)

        if coords and coords[1] > -30:
            self.root.after(30, lambda: self.animate_heart(heart, speed, drift))
        else:
            self.canvas.delete(heart)

    # =========================
    # BOOT SCREEN
    # =========================

    def show_boot_screen(self):
        self.draw_scanlines()

        self.canvas.create_text(
            300,
            150,
            text="LOVE DEBUGGER",
            fill="#58a6ff",
            font=("Consolas", 28, "bold")
        )

        self.canvas.create_text(
            300,
            195,
            text="v1.0",
            fill="#8b949e",
            font=("Consolas", 12)
        )

        self.canvas.create_rectangle(
            150, 300, 450, 320,
            fill="",
            outline="#30363d"
        )

        self.progress_bar = self.canvas.create_rectangle(
            150,
            300,
            150,
            320,
            fill="#58a6ff",
            outline=""
        )

        self.typewriter(
            300, 260,
            "Initializing system...",
            "#ffffff",
            ("Consolas", 14),
            callback=lambda: self.root.after(500, self.update_progress)
        )


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    root = tk.Tk()

    app = LoveDebugger(root)

    root.mainloop()
