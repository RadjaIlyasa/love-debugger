"""LoveDebugger entry point."""

import tkinter as tk

from app import LoveDebugger


if __name__ == "__main__":
    root = tk.Tk()
    LoveDebugger(root)
    root.mainloop()
