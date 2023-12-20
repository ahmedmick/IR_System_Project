from tkinter import Button
import Models_Data
import Buttons_Color
from GUI_Components import change_selected_button_color


class Event:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def notify(self):
        for handler in self.handlers:
            handler()


event = Event()


def return_to_main_menu():
    # Boolean_Retrieval_Model
    Models_Data.Boolean_Retrieval_Model_FILES_NAME = ["#"]
    Models_Data.Boolean_Retrieval_Model_FILES_DATA = []
    Models_Data.Boolean_Retrieval_Model_WORDS = []
    Models_Data.Boolean_Retrieval_Model_NUMBER_OF_FILES = 1
    Models_Data.Boolean_Retrieval_Model_MATRIX = []

    # Inverted Index Model
    Models_Data.Inverted_Index_Model_FILES_NAME = []
    Models_Data.Inverted_Index_Model_FILES_DATA = []
    Models_Data.Inverted_Index_Model_WORDS = []
    Models_Data.Inverted_Index_Model_NUMBER_OF_FILES = 0
    Models_Data.Inverted_Index_Model_MATRIX = []

    # Positional Index Model
    Models_Data.Positional_Index_Model_FILES_NAME = []
    Models_Data.Positional_Index_Model_FILES_DATA = []
    Models_Data.Positional_Index_Model_WORDS = []
    Models_Data.Positional_Index_Model_NUMBER_OF_FILES = 0
    Models_Data.Positional_Index_Model_MATRIX = []

    # Vector Space Model
    Models_Data.Vector_Space_Model_FILES_NAME = []
    Models_Data.Vector_Space_Model_FILES_DATA = []
    Models_Data.Vector_Space_Model_WORDS = []
    Models_Data.Vector_Space_Model_NUMBER_OF_FILES = 0
    Models_Data.Vector_Space_Model_MATRIX = []
    Models_Data.Vector_Space_Model_Query_FILES_NAME = []
    Models_Data.Vector_Space_Model_Query_FILES_DATA = []
    Models_Data.Vector_Space_Model_Query_WORDS = []
    Models_Data.Vector_Space_Model_Query_NUMBER_OF_FILES = 0
    Models_Data.Vector_Space_Model_Query_MATRIX = []

    for component in Models_Data.Boolean_Retrieval_Model_Components:
        component["name"].place_forget()
    for component in Models_Data.Inverted_Index_Model_Components:
        component["name"].place_forget()
    for component in Models_Data.Positional_Index_Model_Components:
        component["name"].place_forget()
    for component in Models_Data.Vector_Space_Model_Components:
        if isinstance(component["name"], Button):
            change_selected_button_color(
                component["name"],
                Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
                Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
            )
        component["name"].place_forget()
    event.notify()
