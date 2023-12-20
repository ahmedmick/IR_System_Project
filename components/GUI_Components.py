from tkinter import font, Label, Button, Text, Entry, END
from Main_Window_Screen import *


def create_label(content):
    label_font = font.Font(size=content["label_size"])
    label = Label(MAIN_WINDOW, text=content["label_text"], font=label_font)
    label["background"] = content["label_background_color"]
    label["foreground"] = content["label_foreground_color"]
    return label


def create_button(content):
    global MAIN_WINDOW
    button_font = font.Font(size=content["button_size"])
    button = Button(
        MAIN_WINDOW,
        text=content["button_text"],
        command=content["function_name"],
        font=button_font,
    )
    button["background"] = content["button_background_color"]
    button["foreground"] = content["button_foreground_color"]
    return button


def create_textbox(content):
    global MAIN_WINDOW
    textbox_font = font.Font(size=content["textbox_size"])
    textbox = Text(
        MAIN_WINDOW, height=content["height"], width=content["width"], font=textbox_font
    )
    textbox["background"] = content["textbox_background_color"]
    textbox["foreground"] = content["textbox_foreground_color"]
    return textbox


def change_selected_button_color(component, background_color, foreground_color):
    component.config(bg=background_color, fg=foreground_color)
    component.update()


def load_background_image(window):
    # Create a Canvas widget to cover the entire window
    CANVAS.pack()
    CANVAS.create_image(0, 0, anchor=tk.NW, image=BACKGROUND_IMAGE)
    CANVAS.update()


# Classes
class Table:
    def __init__(self, root, MATRIX):
        global TABLE_WINDOW_X_AXIS, TABLE_WINDOW_Y_AXIS
        total_rows = len(MATRIX)
        total_columns = len(MATRIX[0])

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                color = ""
                if i == 0 and j == 0:
                    color = "blue"
                elif i == 0:
                    color = "darkgreen"
                elif j == 0:
                    color = "black"
                else:
                    color = "red"
                self.e = Entry(
                    root,
                    width=12,
                    fg=color,
                    justify="center",
                    font=("Arial", 12, "bold"),
                )

                self.e.grid(row=i, column=j)
                self.e.insert(END, MATRIX[i][j])
