import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calpkg.ponggame import ponggame

def main():
    print("Starting Game...")
    root = tk.Tk()
    game = ponggame(root)
    root.mainloop()

if __name__ == "__main__":
    main()