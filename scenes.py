"""LoveDebugger scene flow."""

from config import (
    BORDER,
    DIAGNOSTICS,
    ERROR,
    FONT,
    INVESTIGATION_STEPS,
    NO,
    NO_HOVER,
    NO_REACTIONS,
    PRIMARY,
    SECONDARY,
    SUCCESS,
    SUCCESS_HOVER,
    TARGET_NAME,
    WHITE,
)


class Scenes:
    """Controls the application's screens and scene-specific interactions."""

    def __init__(self, app) -> None:
        self.app = app

    @property
    def root(self):
        return self.app.root

    @property
    def canvas(self):
        return self.app.canvas

    @property
    def effects(self):
        return self.app.effects

    def update_progress(self) -> None:
        if self.app.closing:
            return

        self.app.progress += 2
        width = 300 * (self.app.progress / 100)
        self.canvas.coords(
            self.app.progress_bar,
            150,
            300,
            150 + width,
            320,
        )

        if self.app.progress < 100:
            self.root.after(50, self.update_progress)
        else:
            self.root.after(500, lambda: self.effects.fade_to(self.run_diagnostics))

    def run_diagnostics(self) -> None:
        if self.app.closing:
            return

        if self.app.diagnostic_index == 0:
            self.effects.clear_screen()
            self.canvas.create_text(
                300,
                100,
                text="SYSTEM DIAGNOSTIC",
                fill=PRIMARY,
                font=(FONT, 20, "bold"),
            )

        diagnostic = DIAGNOSTICS[self.app.diagnostic_index]
        color = ERROR if "ERROR" in diagnostic else WHITE

        if "ERROR" in diagnostic:
            self.effects.play_error_sfx()

        def next_diagnostic():
            self.app.diagnostic_index += 1
            if self.app.diagnostic_index < len(DIAGNOSTICS):
                self.root.after(150, self.run_diagnostics)
            else:
                self.root.after(1000, lambda: self.effects.fade_to(self.show_anomaly))

        self.effects.typewriter(
            300,
            180 + (self.app.diagnostic_index * 35),
            "> " + diagnostic,
            color,
            (FONT, 12),
            callback=next_diagnostic,
        )

    def show_anomaly(self) -> None:
        if self.app.closing:
            return

        self.effects.clear_screen()

        self.app.anomaly_text = self.canvas.create_text(
            300,
            150,
            text="⚠ ANOMALY DETECTED",
            fill=ERROR,
            font=(FONT, 20, "bold"),
        )

        self.canvas.create_line(180, 180, 420, 180, fill=BORDER)
        self.canvas.create_text(
            300,
            220,
            text="Possible cause:",
            fill=SECONDARY,
            font=(FONT, 12),
        )
        self.canvas.create_text(
            300,
            260,
            text="Someone has occupied your thoughts.",
            fill=WHITE,
            font=(FONT, 13),
        )

        self.app.blinking = True
        self.effects.play_error_sfx()
        self.effects.shake_screen(frames_left=10, magnitude=6)
        self.root.after(500, self.blink_anomaly)
        self.root.after(2000, lambda: self.effects.fade_to(self.run_investigation))

    def blink_anomaly(self, state=True) -> None:
        if self.app.closing or not self.app.blinking:
            return

        color = ERROR if state else "#0d1117"
        self.canvas.itemconfig(self.app.anomaly_text, fill=color)
        self.root.after(300, lambda: self.blink_anomaly(not state))

    def run_investigation(self) -> None:
        if self.app.closing:
            return

        self.app.blinking = False

        if self.app.investigation_index == 0:
            self.effects.clear_screen()
            self.canvas.create_text(
                300,
                100,
                text="INVESTIGATION",
                fill=PRIMARY,
                font=(FONT, 20, "bold"),
            )
            self.canvas.create_text(
                300,
                150,
                text="Scanning target...",
                fill=SECONDARY,
                font=(FONT, 12),
            )
            self.canvas.create_rectangle(
                150,
                180,
                450,
                200,
                fill="",
                outline=BORDER,
            )
            self.app.investigation_bar = self.canvas.create_rectangle(
                150,
                180,
                150,
                200,
                fill=PRIMARY,
                outline="",
            )

        self.app.investigation_progress += 20
        width = 300 * (self.app.investigation_progress / 100)
        self.canvas.coords(
            self.app.investigation_bar,
            150,
            180,
            150 + width,
            200,
        )

        investigation = INVESTIGATION_STEPS[self.app.investigation_index]

        def next_investigation():
            self.app.investigation_index += 1
            if self.app.investigation_index < len(INVESTIGATION_STEPS):
                self.root.after(150, self.run_investigation)
            else:
                self.root.after(1000, lambda: self.effects.fade_to(self.show_result))

        self.effects.typewriter(
            300,
            250 + (self.app.investigation_index * 25),
            investigation,
            WHITE,
            (FONT, 12),
            callback=next_investigation,
        )

    def show_result(self) -> None:
        if self.app.closing:
            return

        self.effects.clear_screen()
        self.canvas.create_text(
            300,
            150,
            text="TARGET IDENTIFIED",
            fill=PRIMARY,
            font=(FONT, 20, "bold"),
        )
        self.canvas.create_text(
            300,
            200,
            text=f"Subject: {TARGET_NAME}",
            fill=WHITE,
            font=(FONT, 13),
        )
        self.app.confidence_text = self.canvas.create_text(
            300,
            230,
            text="Confidence: 0.0%",
            fill=WHITE,
            font=(FONT, 13),
        )
        self.animate_confidence(0.0)

    def animate_confidence(self, current) -> None:
        if self.app.closing:
            return

        target = 98.7
        current = min(current + 3.5, target)
        self.canvas.itemconfig(
            self.app.confidence_text,
            text=f"Confidence: {current:.1f}%",
        )

        if current < target:
            self.root.after(25, lambda: self.animate_confidence(current))
            return

        self.canvas.create_text(
            300,
            280,
            text="Conclusion:",
            fill=SECONDARY,
            font=(FONT, 13),
        )
        self.canvas.create_text(
            300,
            310,
            text="You are in love.",
            fill=ERROR,
            font=(FONT, 16, "bold"),
        )
        self.root.after(2000, lambda: self.effects.fade_to(self.show_confession))

    def show_confession(self) -> None:
        if self.app.closing:
            return

        self.effects.clear_screen()
        self.app.no_meme_item = None
        self.app.no_attempts = 0

        self._destroy_button("yes_button")
        self._destroy_button("no_button")

        self.canvas.create_text(
            300,
            90,
            text="FINAL QUESTION",
            fill=PRIMARY,
            font=(FONT, 20, "bold"),
        )
        self.canvas.create_text(
            300,
            140,
            text="After analyzing all available data...",
            fill=SECONDARY,
            font=(FONT, 12),
        )
        self.canvas.create_text(
            300,
            170,
            text="I have reached one conclusion.",
            fill=WHITE,
            font=(FONT, 13),
        )
        self.canvas.create_text(
            300,
            215,
            text="Will you be mine?",
            fill=ERROR,
            font=(FONT, 20, "bold"),
        )

        self.effects.animate_eminem_pop(0)

        self.app.no_message = self.canvas.create_text(
            300,
            450,
            text="",
            fill=ERROR,
            font=(FONT, 12),
        )

        self.app.yes_button = self._create_yes_button()
        self.app.no_button = self._create_no_button()
        self.app.no_button.bind("<Enter>", self.move_no_button)

    def _create_yes_button(self):
        import tkinter as tk

        button = tk.Button(
            self.root,
            text="YES",
            font=(FONT, 12, "bold"),
            bg=SUCCESS,
            fg="white",
            activebackground=SUCCESS_HOVER,
            activeforeground="white",
            relief="flat",
            width=10,
            command=self.answer_yes,
        )
        button.place(x=180, y=380)
        return button

    def _create_no_button(self):
        import tkinter as tk

        button = tk.Button(
            self.root,
            text="NO",
            font=(FONT, 12, "bold"),
            bg=NO,
            fg="white",
            activebackground=NO_HOVER,
            activeforeground="white",
            relief="flat",
            width=10,
            takefocus=False,
            command=self.answer_no,
        )
        button.place(x=320, y=380)
        return button

    def move_no_button(self, _event=None) -> None:
        if self.app.closing:
            return

        self.app.no_attempts += 1
        message, sticker = self._get_no_reaction(self.app.no_attempts)

        yes_x, yes_y = 180, 380
        yes_w = max(100, self.app.yes_button.winfo_width())
        yes_h = max(40, self.app.yes_button.winfo_height())

        for _ in range(25):
            new_x = self.app.random.randint(0, 500)
            new_y = self.app.random.randint(0, 440)
            if not (
                yes_x - 100 < new_x < yes_x + yes_w
                and yes_y - 40 < new_y < yes_y + yes_h
            ):
                break

        self.app.no_button.place(x=new_x, y=new_y)
        self.canvas.itemconfig(self.app.no_message, text=message)

        current_width = int(self.app.yes_button.cget("width"))
        if current_width < 18:
            self.app.yes_button.config(width=current_width + 1)

        if sticker:
            self.show_no_meme(sticker)

    @staticmethod
    def _get_no_reaction(attempts: int):
        for threshold, message, sticker in NO_REACTIONS:
            if attempts == threshold:
                return message, sticker
        return "There is only one answer.", "skull"

    def show_no_meme(self, sticker_key: str) -> None:
        image = self.app.assets.stickers.get(sticker_key)
        if image is None:
            image = self.app.assets.stickers.get("broken_heart")
        if self.app.closing or image is None:
            return

        message_coords = self.canvas.bbox(self.app.no_message)
        if not message_coords:
            return

        x = message_coords[2] + 40
        y = (message_coords[1] + message_coords[3]) // 2 + 5

        if x > 560:
            x = max(50, message_coords[0] - 40)

        if self.app.no_meme_item is None:
            self.app.no_meme_item = self.canvas.create_image(x, y, image=image)
        else:
            self.canvas.coords(self.app.no_meme_item, x, y)
            self.canvas.itemconfig(self.app.no_meme_item, image=image)

    def answer_no(self) -> None:
        if self.app.closing:
            return

        self.effects.play_error_sfx()
        self._destroy_button("no_button")
        self.canvas.create_text(
            300,
            420,
            text="ERROR: Response rejected.",
            fill=ERROR,
            font=(FONT, 11),
        )
        self.root.after(1000, lambda: self.effects.fade_to(self.show_confession))

    def answer_yes(self) -> None:
        if self.app.closing:
            return

        self._destroy_button("yes_button")
        self._destroy_button("no_button")
        self.app.glitch_active = False
        self.effects.clear_screen()

        self.canvas.create_text(
            300,
            180,
            text="✓ CONNECTION ESTABLISHED",
            fill=PRIMARY,
            font=(FONT, 20, "bold"),
        )
        self.canvas.create_text(
            300,
            240,
            text="LoveDebugger has detected",
            fill=WHITE,
            font=(FONT, 13),
        )
        self.canvas.create_text(
            300,
            270,
            text="a successful response.",
            fill=WHITE,
            font=(FONT, 13),
        )
        self.canvas.create_text(
            300,
            340,
            text="♥",
            fill=ERROR,
            font=(FONT, 40, "bold"),
        )

        self.app.hearts_active = True
        self.effects.spawn_hearts()

    def _destroy_button(self, attr_name: str) -> None:
        button = getattr(self.app, attr_name, None)
        if button is not None and button.winfo_exists():
            button.destroy()
            setattr(self.app, attr_name, None)
