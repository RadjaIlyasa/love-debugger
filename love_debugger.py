import tkinter as tk
import random
import os


class LoveDebugger:
    def __init__(self, root):
        self.root = root

        self.root.title("LoveDebugger")
        self.root.geometry("600x500")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

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
        # MEME ASSETS
        # =========================

        # path assets/ relatif terhadap lokasi file .py ini, jadi
        # tetap ketemu gambarnya walau dijalanin dari folder lain
        assets_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets"
        )

        # frame-frame Eminem buat efek "pop" (kecil -> besar) pas
        # scene "Will you be mine?"
        self.eminem_frames = [
            tk.PhotoImage(file=os.path.join(assets_dir, "eminem_40.png")),
            tk.PhotoImage(file=os.path.join(assets_dir, "eminem_65.png")),
            tk.PhotoImage(file=os.path.join(assets_dir, "eminem_90.png")),
            tk.PhotoImage(file=os.path.join(assets_dir, "eminem_115.png")),
        ]

        # sticker reaksi buat spam tombol NO
        self.img_crying_barbie = tk.PhotoImage(
            file=os.path.join(assets_dir, "crying_barbie.png")
        )
        self.img_donkey_face = tk.PhotoImage(
            file=os.path.join(assets_dir, "donkey_face.png")
        )

        # mulai loop glitch flash (jalan terus sepanjang app hidup)
        self.random_glitch()

        self.show_boot_screen()

    # =========================
    # CLEAR SCREEN
    # =========================

    def clear_screen(self):
        self.canvas.delete("all")
        # scanline digambar ulang tiap kali layar di-clear,
        # supaya "tekstur" CRT-nya nempel di semua scene
        self.draw_scanlines()

    # =========================
    # SCANLINE (background texture)
    # =========================

    def draw_scanlines(self):
        # garis horizontal tipis tiap 4px, warna dikit lebih terang
        # dari background -> efek layar CRT tua, subtle biar teks
        # tetap kebaca jelas
        for y in range(0, 500, 4):
            self.canvas.create_line(
                0, y, 600, y,
                fill="#141a24",
                tags="scanline"
            )
        # kirim scanline ke paling belakang, supaya teks/elemen
        # lain yang digambar setelahnya selalu di atas
        self.canvas.tag_lower("scanline")

    # =========================
    # GLITCH FLASH (random, jalan independen dari scene)
    # =========================

    def random_glitch(self):
        # berhenti total kalau udah masuk scene final (hati)
        if not self.glitch_active:
            return

        # garis terang random yang muncul sekilas lalu hilang,
        # kesannya kayak "signal noise" / error sesaat
        y = random.randint(0, 500)
        glitch_color = random.choice(["#58a6ff", "#ff5555", "#ffffff"])

        glitch_line = self.canvas.create_line(
            0, y, 600, y,
            fill=glitch_color,
            width=random.choice([1, 2, 3]),
            tags="glitch"
        )

        # hapus lagi setelah sangat sebentar (kedip cepat)
        self.root.after(
            random.randint(40, 100),
            lambda: self.canvas.delete(glitch_line)
        )

        # jadwalin glitch berikutnya, interval random biar
        # gak terasa mekanis/predictable
        self.root.after(
            random.randint(800, 2500),
            self.random_glitch
        )

    # =========================
    # TYPEWRITER EFFECT
    # =========================

    def typewriter(self, x, y, full_text, fill, font, callback=None, delay=22):
        # bikin text item kosong dulu, nanti diisi karakter
        # demi karakter -> efek "ngetik" ala terminal
        item = self.canvas.create_text(x, y, text="", fill=fill, font=font)
        self._type_step(item, full_text, 1, delay, callback)

    def _type_step(self, item, full_text, index, delay, callback):
        self.canvas.itemconfig(item, text=full_text[:index])

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
        # posisikan ulang seluruh isi canvas secara random tiap
        # frame, lalu balikin ke posisi semula di frame terakhir
        if not hasattr(self, "_shake_offset"):
            self._shake_offset = (0, 0)

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

    # =========================
    # DIAGNOSTIC
    # =========================

    def run_diagnostics(self):
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

    # =========================
    # ANOMALY
    # =========================

    def show_anomaly(self):
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

        # flag supaya blink berhenti begitu pindah scene,
        # bukan cuma mengandalkan timing pas
        self.blinking = True

        # layar berguncang sesaat pas anomaly baru kedetect,
        # kesan "sistem kaget"
        self.shake_screen(frames_left=10, magnitude=6)

        self.root.after(500, self.blink_anomaly)
        self.root.after(2000, self.run_investigation)

    # =========================
    # ANOMALY BLINK
    # =========================

    def blink_anomaly(self, state=True):
        # kalau scene udah pindah, jangan lanjut toggle warna
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
        # hentikan blink begitu masuk scene investigation
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

            self.investigation_bar = self.canvas.create_rectangle(
                150,
                180,
                150,
                200,
                fill="#58a6ff",
                outline=""
            )

        # Update investigation progress

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

        # Show investigation message

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

    # =========================
    # RESULT
    # =========================

    def show_result(self):
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
            text="Subject: UNKNOWN",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        # teks confidence dimulai dari 0%, nanti dihitung naik
        # pelan-pelan sampai ke angka final
        self.confidence_text = self.canvas.create_text(
            300,
            230,
            text="Confidence: 0.0%",
            fill="#ffffff",
            font=("Consolas", 13)
        )

        self.animate_confidence(0.0)

    def animate_confidence(self, current):
        target = 98.7
        current = min(current + 3.5, target)

        self.canvas.itemconfig(
            self.confidence_text,
            text=f"Confidence: {current:.1f}%"
        )

        if current < target:
            self.root.after(25, lambda: self.animate_confidence(current))
        else:
            # baru tampilin kesimpulan setelah hitungan selesai
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

    # =========================
    # CONFESSION
    # =========================

    def show_confession(self):
        self.clear_screen()

        # reset sticker reaksi NO tiap scene ini di-render ulang
        self.no_meme_item = None

        # --- FIX: bersihin widget lama sebelum bikin yang baru,
        # supaya gak numpuk (widget leak) tiap kali user klik NO
        # dan show_confession() dipanggil ulang.
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

        # gambar Eminem muncul dengan efek "pop" (kecil -> besar)
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
        self.no_attempts += 1

        if self.no_attempts == 1:
            message = "Nice try."
        elif self.no_attempts == 2:
            message = "Still trying!"
        elif self.no_attempts == 3:
            message = "Bro... seriously?"
        elif self.no_attempts == 4:
            message = "🙃"
            self.show_no_meme(self.img_crying_barbie)
        else:
            message = "Umm... maybe you should click YES?"
            self.show_no_meme(self.img_donkey_face)

        # --- FIX: batasi area random supaya tombol (lebar ~90px,
        # tinggi ~30px) selalu utuh di dalam window 600x500,
        # gak nongol/kepotong di tepi kanan atau bawah.
        new_x = random.randint(0, 500)
        new_y = random.randint(0, 440)

        self.no_button.place(
            x=new_x,
            y=new_y
        )

        self.canvas.itemconfig(
            self.no_message,
            text=message
        )

    def show_no_meme(self, image):
        # posisi pojok kanan atas, jauh dari tombol NO yang lagi
        # kabur-kaburan random, biar gak ketutupan
        if self.no_meme_item is None:
            self.no_meme_item = self.canvas.create_image(
                530, 90,
                image=image
            )
        else:
            self.canvas.itemconfig(
                self.no_meme_item,
                image=image
            )

    def answer_no(self):
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

    # =========================
    # YES
    # =========================

    def answer_yes(self):
        self.yes_button.destroy()

        # kalau user langsung klik YES tanpa pernah hover NO,
        # no_button masih ada di layar -> aman di-destroy di sini
        if hasattr(self, "no_button"):
            self.no_button.destroy()

        # matiin glitch flash, biar scene final tenang & fokus
        # ke hati yang bertebaran (gak keganggu efek noise lagi)
        self.glitch_active = False

        self.canvas.delete("all")

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

        # mulai efek hati bertebaran, jalan terus selama scene ini
        self.hearts_active = True
        self.spawn_hearts()

    # =========================
    # FLOATING HEARTS EFFECT
    # =========================

    def spawn_hearts(self):
        if not self.hearts_active:
            return

        # bikin 1-2 hati baru tiap kali dipanggil, muncul dari
        # posisi bawah canvas dengan ukuran & warna random
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

            # tiap hati punya kecepatan naik & goyangan horizontal
            # sendiri-sendiri, biar gerakannya gak keliatan seragam
            speed = random.uniform(1.0, 2.5)
            drift = random.uniform(-0.6, 0.6)
            self.animate_heart(heart, speed, drift)

        # jadwalin batch hati berikutnya
        self.root.after(300, self.spawn_hearts)

    def animate_heart(self, heart, speed, drift):
        self.canvas.move(heart, drift, -speed)
        coords = self.canvas.coords(heart)

        # kalau hati sudah lewat dari batas atas canvas, hapus
        # supaya gak numpuk item canvas tak terbatas (memory leak)
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

        self.progress_bar = self.canvas.create_rectangle(
            150,
            300,
            150,
            320,
            fill="#58a6ff",
            outline=""
        )

        # "Initializing system..." diketik pelan-pelan, progress bar
        # baru mulai jalan setelah teksnya selesai diketik
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
