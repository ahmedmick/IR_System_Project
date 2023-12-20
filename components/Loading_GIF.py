import tkinter as tk
from itertools import count, cycle
from PIL import Image, ImageTk

LOADING_SCREEN_IMAGE =  "./assets/loading_screen.gif"

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """

    def load(self):
        im = LOADING_SCREEN_IMAGE
        MAIN_WINDOW_SIZE = "600x650"
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy().resize((int(MAIN_WINDOW_SIZE[:3]), int(MAIN_WINDOW_SIZE[4:])))))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
