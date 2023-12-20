import tkinter as tk
import sys
from PIL import ImageTk, Image

sys.path.append("./assets")  # Replace with the actual path

MAIN_WINDOW = tk.Tk()
MAIN_WINDOW_SIZE = "600x650"
MAIN_WINDOW_TITLE = "Search Engine Models"
MAIN_WINDOW_BACKGROUND_COLOR = "#111"
MAIN_WINDOW_FOREGROUND_COLOR = "white"
BACKGROUND_IMAGE = ImageTk.PhotoImage(Image.open("./assets/background_image.jpg"))
CANVAS = tk.Canvas(MAIN_WINDOW, width=600, height=650)
