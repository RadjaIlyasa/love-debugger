"""Project configuration and user-facing strings."""

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
WINDOW_TITLE = "LoveDebugger"
WINDOW_BG = "#0d1117"

TARGET_NAME = "YOU"

PRIMARY = "#58a6ff"
SECONDARY = "#8b949e"
WHITE = "#ffffff"
ERROR = "#ff5555"
SUCCESS = "#238636"
SUCCESS_HOVER = "#2ea043"
NO = "#da3633"
NO_HOVER = "#f85149"
BORDER = "#30363d"
SCANLINE = "#141a24"

FONT = "Consolas"

DIAGNOSTICS = [
    "Checking CPU.......... OK",
    "Checking RAM.......... OK",
    "Checking Database.......... OK",
    "Checking Network.......... OK",
    "Checking emotional state. ERROR",
]

INVESTIGATION_STEPS = [
    "> Starting investigation...",
    "> Scanning recent interactions...",
    "> Analyzing behavioral patterns...",
    "> Cross-referencing emotional data...",
    "> Identifying source...",
]

NO_REACTIONS = [
    (1, "Nice try.", "side_eye"),
    (2, "Still trying!", "raised_eyebrow"),
    (3, "Bro... seriously?", "clown"),
    (4, "Bro... you really said NO?", "crying_barbie"),
    (5, "I'm not giving up.", "pleading_face"),
    (6, "You're running out of options.", "crying_cat"),
    (7, "Just click YES already!", "donkey_face"),
    (8, "Why do you hurt me like this?", "loudly_crying"),
]

STICKER_FILES = {
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

EMINEM_FILES = [
    "eminem_40.png",
    "eminem_65.png",
    "eminem_90.png",
    "eminem_115.png",
]

CLICK_SOUND = "click.wav"
ERROR_SOUND = "error.wav"
