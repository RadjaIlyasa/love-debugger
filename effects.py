"""Reusable visual effects and animation helpers."""

import random

from config import ERROR, SCANLINE, WHITE, PRIMARY


class Effects:
    """Animations that operate on the application's Tkinter canvas."""

    def __init__(self, app) -> None:
        self.app = app

    @property
    def root(self):
        return self.app.root

    @property
    def canvas(self):
        return self.app.canvas

    def play_typing_sfx(self) -> None:
        sound = self.app.assets.sfx_click
        if sound is not None and not self.app.closing:
            try:
                sound.play()
            except Exception:
                pass

    def play_error_sfx(self) -> None:
        sound = self.app.assets.sfx_error
        if sound is not None and not self.app.closing:
            try:
                sound.play()
            except Exception:
                pass

    def draw_scanlines(self) -> None:
        for y in range(0, 500, 4):
            self.canvas.create_line(
                0,
                y,
                600,
                y,
                fill=SCANLINE,
                tags="scanline",
            )
        self.canvas.tag_lower("scanline")

    def clear_screen(self) -> None:
        self.canvas.delete("all")
        self.app.shake_offset = (0, 0)
        self.draw_scanlines()

    def random_glitch(self) -> None:
        if self.app.closing or not self.app.glitch_active:
            return

        y = random.randint(0, 500)
        glitch_color = random.choice([PRIMARY, ERROR, WHITE])
        glitch_line = self.canvas.create_line(
            0,
            y,
            600,
            y,
            fill=glitch_color,
            width=random.choice([1, 2, 3]),
            tags="glitch",
        )

        self.root.after(
            random.randint(40, 100),
            lambda: self.canvas.delete(glitch_line) if not self.app.closing else None,
        )
        self.root.after(random.randint(800, 2500), self.random_glitch)

    def typewriter(self, x, y, text, fill, font, callback=None, delay=22) -> None:
        if self.app.closing:
            return

        item = self.canvas.create_text(x, y, text="", fill=fill, font=font)
        self._type_step(item, text, 1, delay, callback)

    def _type_step(self, item, text, index, delay, callback) -> None:
        if self.app.closing:
            return

        self.canvas.itemconfig(item, text=text[:index])

        if index % 2 == 1:
            self.play_typing_sfx()

        if index < len(text):
            self.root.after(
                delay,
                lambda: self._type_step(item, text, index + 1, delay, callback),
            )
        elif callback:
            callback()

    def fade_to(self, callback, step_ms=20) -> None:
        if self.app.closing or not self.app.assets.fade_frames:
            callback()
            return

        overlay = self.canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.app.assets.fade_frames[0],
        )

        def step_out(index):
            if self.app.closing:
                return
            if index < len(self.app.assets.fade_frames):
                self.canvas.itemconfig(
                    overlay,
                    image=self.app.assets.fade_frames[index],
                )
                self.canvas.tag_raise(overlay)
                self.root.after(step_ms, lambda: step_out(index + 1))
            else:
                callback()
                in_overlay = self.canvas.create_image(
                    0,
                    0,
                    anchor="nw",
                    image=self.app.assets.fade_frames[-1],
                )
                step_in(in_overlay, len(self.app.assets.fade_frames) - 1)

        def step_in(in_overlay, index):
            if self.app.closing:
                return
            if index >= 0:
                self.canvas.itemconfig(
                    in_overlay,
                    image=self.app.assets.fade_frames[index],
                )
                self.canvas.tag_raise(in_overlay)
                self.root.after(step_ms, lambda: step_in(in_overlay, index - 1))
            else:
                self.canvas.delete(in_overlay)

        step_out(0)

    def shake_screen(self, frames_left, magnitude=6) -> None:
        if self.app.closing:
            return

        if frames_left <= 0:
            offset_x, offset_y = self.app.shake_offset
            self.canvas.move("all", -offset_x, -offset_y)
            self.app.shake_offset = (0, 0)
            return

        new_x = random.randint(-magnitude, magnitude)
        new_y = random.randint(-magnitude, magnitude)
        old_x, old_y = self.app.shake_offset

        self.canvas.move("all", new_x - old_x, new_y - old_y)
        self.app.shake_offset = (new_x, new_y)
        self.root.after(
            40,
            lambda: self.shake_screen(frames_left - 1, magnitude),
        )

    def animate_eminem_pop(self, index=0) -> None:
        frames = self.app.assets.eminem_frames
        if self.app.closing or not frames:
            return

        if index == 0:
            self.app.eminem_img_item = self.canvas.create_image(
                300,
                305,
                image=frames[0],
            )
        else:
            self.canvas.itemconfig(self.app.eminem_img_item, image=frames[index])

        if index < len(frames) - 1:
            self.root.after(70, lambda: self.animate_eminem_pop(index + 1))

    def spawn_hearts(self) -> None:
        if self.app.closing or not self.app.hearts_active:
            return

        for _ in range(random.randint(1, 2)):
            x = random.randint(30, 570)
            size = random.randint(14, 30)
            color = random.choice(["#ff5555", "#ff8080", "#ffb3b3"])
            heart = self.canvas.create_text(
                x,
                510,
                text="♥",
                fill=color,
                font=("Consolas", size, "bold"),
            )

            speed = random.uniform(1.0, 2.5)
            drift = random.uniform(-0.6, 0.6)
            self.animate_heart(heart, speed, drift)

        self.root.after(300, self.spawn_hearts)

    def animate_heart(self, heart, speed, drift) -> None:
        if self.app.closing:
            return

        self.canvas.move(heart, drift, -speed)
        coords = self.canvas.coords(heart)

        if coords and coords[1] > -30:
            self.root.after(
                30,
                lambda: self.animate_heart(heart, speed, drift),
            )
        else:
            self.canvas.delete(heart)
