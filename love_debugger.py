import tkinter as tk
import random
import os
import sys
import ctypes

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

TARGET_NAME = "Ilyasa"


class LoveDebugger:
    def __init__(self, root):
        self.root = root

        self.root.title("LoveDebugger")
        self.root.geometry("600x500")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 600) // 2
        y = (sh - 500) // 2
        self.root.geometry(f"600x500+{x}+{y}")

        self._closing = False
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.progress = 0

        self.diagnostics = [
            "Checking CPU.......... OK",
            "Checking RAM.......... OK",
            "Checking Database.......... OK",
            "Checking Network.......... OK",
            "Checking emotional state. ERROR",
        ]

        self.diagnostic_index = 0

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

        self.glitch_active = True

        self._shake_offset = (0, 0)

        self.canvas = tk.Canvas(
            root,
            width=600,
            height=500,
            bg="#0d1117",
            highlightthickness=0
        )

        self.canvas.pack()

        assets_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets"
        )

        try:
            self.eminem_frames = [
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_40.png")),
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_65.png")),
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_90.png")),
                tk.PhotoImage(file=os.path.join(assets_dir, "eminem_115.png")),
            ]
        except Exception:
            self.eminem_frames = []

        try:
            self.img_crying_barbie = tk.PhotoImage(
                file=os.path.join(assets_dir, "crying_barbie.png")
            )
        except Exception:
            self.img_crying_barbie = None

        try:
            self.img_donkey_face = tk.PhotoImage(
                file=os.path.join(assets_dir, "donkey_face.png")
            )
        except Exception:
            self.img_donkey_face = None

        self.random_glitch()

        self.show_boot_screen()

    def _on_close(self):
        """Stop all animation loops and destroy the window cleanly."""
        self._closing = True
        self.glitch_active = False
        if hasattr(self, "blinking"):
            self.blinking = False
        if hasattr(self, "hearts_active"):
            self.hearts_active = False
        self.root.destroy()

    def clear_screen(self):
        self.canvas.delete("all")
        self._shake_offset = (0, 0)
        self.draw_scanlines()

    def draw_scanlines(self):
        for y in range(0, 500, 4):
            self.canvas.create_line(
                0, y, 600, y,
                fill="#141a24",
                tags="scanline"
            )
        self.canvas.tag_lower("scanline")

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

    def typewriter(self, x, y, full_text, fill, font, callback=None, delay=22):
        if self._closing:
            return
        item = self.canvas.create_text(x, y, text="", fill=fill, font=font)
        self._type_step(item, full_text, 1, delay, callback)

    def _type_step(self, item, full_text, index, delay, callback):
        if self._closing:
            return

        self.canvas.itemconfig(item, text=full_text[:index])

        if index < len(full_text):
            self.root.after(
                delay,
                lambda: self._type_step(item, full_text, index + 1, delay, callback)
            )
        elif callback:
            callback()

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
            self.root.after(500, self.run_diagnostics)

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
        else:
            color = "#ffffff"

        def next_diagnostic():
            self.diagnostic_index += 1
            if self.diagnostic_index < len(self.diagnostics):
                self.root.after(150, self.run_diagnostics)
            else:
                self.root.after(1000, self.show_anomaly)

        self.typewriter(
            300,
            180 + (self.diagnostic_index * 35),
            "> " + diagnostic,
            color,
            ("Consolas", 12),
            callback=next_diagnostic
        )

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

        self.shake_screen(frames_left=10, magnitude=6)

        self.root.after(500, self.blink_anomaly)
        self.root.after(2000, self.run_investigation)

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
                self.root.after(1000, self.show_result)

        self.typewriter(
            300,
            250 + (self.investigation_index * 25),
            investigation,
            "#ffffff",
            ("Consolas", 12),
            callback=next_investigation
        )

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

            self.root.after(2000, self.show_confession)

    def show_confession(self):
        if self._closing:
            return

        self.clear_screen()

        self.no_meme_item = None

        if hasattr(self, "yes_button"):
            self.yes_button.destroy()
        if hasattr(self, "no_button"):
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

        if self.no_attempts == 1:
            message = "Nice try."
        elif self.no_attempts == 2:
            message = "Still trying!"
        elif self.no_attempts == 3:
            message = "Bro... seriously?"
        elif self.no_attempts == 4:
            message = "Bro... you really said NO?"
        elif self.no_attempts == 5:
            message = "I'm not giving up."
        elif self.no_attempts == 6:
            message = "You're running out of options."
        elif self.no_attempts == 7:
            message = "Just click YES already!"
        else:
            message = "There is only one answer."

        yes_x, yes_y = 180, 380
        yes_w, yes_h = 100, 40

        for _ in range(20):
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

        current_width = self.yes_button.cget("width")
        if current_width < 18:
            self.yes_button.config(width=current_width + 1)

        if self.no_attempts >= 4:
            if self.no_attempts == 4:
                self.show_no_meme(self.img_crying_barbie)
            else:
                self.show_no_meme(self.img_donkey_face)

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

        if x > 570:
            x = message_coords[0] - 28

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
            self.show_confession
        )

    def answer_yes(self):
        if self._closing:
            return

        self.yes_button.destroy()

        if hasattr(self, "no_button"):
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


if __name__ == "__main__":
    root = tk.Tk()

    app = LoveDebugger(root)

    root.mainloop()
