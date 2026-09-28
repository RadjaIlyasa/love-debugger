# 💙 LoveDebugger

> A terminal-inspired interactive confession experience built with Python and Tkinter.

LoveDebugger is a small desktop app that pretends to diagnose the user's emotional state like a computer system. The program starts with a fake boot sequence, runs a diagnostic scan, detects an "emotional anomaly", investigates the cause, identifies the target, and finally asks the most important question.

It is intentionally designed as a playful interactive experience rather than a conventional utility app.

## ✨ Features

- Terminal-inspired dark UI
- Boot sequence with progress bar
- Typewriter text animation
- Fake system diagnostics
- Glitch effects and screen shake
- Anomaly detection scene
- Investigation progress sequence
- Animated confidence score
- Interactive YES / NO confession screen
- Escaping NO button
- Progressive meme/sticker reactions
- Sound effects through pygame
- Fade transitions between scenes
- Floating heart animation on successful response
- Windows high-DPI handling

## 🎬 Flow

```text
BOOT
  ↓
SYSTEM DIAGNOSTIC
  ↓
ANOMALY DETECTED
  ↓
INVESTIGATION
  ↓
TARGET IDENTIFIED
  ↓
FINAL QUESTION
  ↓
YES / NO
  ↓
ENDING
```

## 🛠️ Built With

- Python
- Tkinter
- Pillow
- Pygame

## 📁 Project Structure

```text
LoveDebugger/
├── assets/
│   ├── click.wav
│   ├── error.wav
│   ├── eminem_40.png
│   ├── eminem_65.png
│   ├── eminem_90.png
│   ├── eminem_115.png
│   └── ... stickers ...
│
├── app.py
├── assets.py
├── config.py
├── effects.py
├── scenes.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Why the code is split this way?

The original prototype grew into a large single Python file. This version separates responsibilities so the project is easier to understand and maintain:

- `main.py` — application entry point
- `app.py` — shared application state and window setup
- `config.py` — colors, messages, asset names, and other configuration
- `assets.py` — image and audio loading
- `effects.py` — reusable animations and visual effects
- `scenes.py` — screen flow and user interactions

The goal is to keep the personality of the original project while making the codebase easier to modify.

## 🚀 Installation

Clone the repository and enter the project directory:

```bash
git clone <your-repository-url>
cd LoveDebugger
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python main.py
```

## 🎨 Customization

The name displayed on the result screen can be changed in `config.py`:

```python
TARGET_NAME = "YOU"
```

You can also change colors, diagnostic messages, investigation messages, and NO-button reactions from the same file without touching the scene logic.

## 🔊 Assets

The app can still run without some optional assets, but audio and visual reactions will be reduced. Put the expected files inside the `assets/` directory.

Expected asset names include:

```text
click.wav
error.wav
eminem_40.png
eminem_65.png
eminem_90.png
eminem_115.png
side_eye.png
raised_eyebrow.png
clown.png
crying_barbie.png
pleading_face.png
crying_cat.png
donkey_face.png
loudly_crying.png
skull.png
broken_heart.png
```

## 🧠 What I Learned

This project was built as a way to practice more than just Python syntax. It combines object-oriented programming, event-driven GUI development, animation timing, asset handling, user interaction, and small UX details into one project.

The main lesson is simple: a small application can become much more memorable when the interface itself becomes part of the experience.

## 🔮 Possible Future Improvements

- Add a real scene/state manager
- Add a settings screen for target name and sound
- Package the app as a Windows executable
- Add more reaction branches
- Add a first-run asset checker
- Add automated tests for non-GUI logic

## 📜 License

This project is for personal/portfolio use. Review the licenses of any third-party images, memes, stickers, sounds, or fonts included in the `assets/` directory before redistributing them.
