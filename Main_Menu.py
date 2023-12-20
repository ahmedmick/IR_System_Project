import sys

sys.path.append("./components")  # Replace with the actual path
sys.path.append("./models")  # Replace with the actual path
from Window_Center import window_center
from Boolean_Retreival_Model import *
from Inverted_Index_Model import *
from Positional_Index_Model import *
from Vector_Space_Model import *
from Loading_GIF import *
import Models_Data
import Back_Button
from Animations import (
    main_menu_component_motion,
    boolean_component_motion,
    inverse_component_motion,
    positional_component_motion,
    vector_document_component_motion,
)
import Buttons_Color

############################################################################

# Constants
LOADING_SCREEN = ImageLabel(MAIN_WINDOW)
LOADING_SCREEN_TIME = 2600
EXIT_WINDOW_BACKGROUND_COLOR = "darkred"
EXIT_WINDOW_FOREGROUND_COLOR = "white"
MAIN_WINDOW_STATE_VALUE = 0
MODEL_STATE_VALUE = 1
STATE_VALUE = MAIN_WINDOW_STATE_VALUE

############################################################################


# Functions
def destroy_main_window():
    for compontent in Models_Data.Main_Window_Components:
        compontent["name"].place_forget()


def create_loading_screen():
    global LOADING_SCREEN
    LOADING_SCREEN.pack()
    LOADING_SCREEN.load()


def destroy_loading_screen():
    global LOADING_SCREEN
    LOADING_SCREEN.destroy()


def create_boolean_retrieval_model():
    if STATE_VALUE == MODEL_STATE_VALUE:
        destroy_main_window()
        for component in Models_Data.Boolean_Retrieval_Model_Components:
            boolean_component_motion(
                component["name"], component["PosX"], component["PosY"]
            )


def destroy_boolean_retrieval_model():
    for component in Models_Data.Boolean_Retrieval_Model_Components:
        component["name"].place_forget()


def create_inverted_index_model():
    if STATE_VALUE == MODEL_STATE_VALUE:
        destroy_main_window()
        for component in Models_Data.Inverted_Index_Model_Components:
            inverse_component_motion(
                component["name"], component["PosX"], component["PosY"]
            )


def destroy_inverted_index_model():
    for component in Models_Data.Inverted_Index_Model_Components:
        component["name"].place_forget()


def create_positional_index_model():
    if STATE_VALUE == MODEL_STATE_VALUE:
        destroy_main_window()
        for component in Models_Data.Positional_Index_Model_Components:
            positional_component_motion(
                component["name"], component["PosX"], component["PosY"]
            )


def destroy_positional_index_model():
    for component in Models_Data.Positional_Index_Model_Components:
        component["name"].place_forget()


def create_vector_space_model():
    if STATE_VALUE == MODEL_STATE_VALUE:
        destroy_main_window()
        for component in Models_Data.Vector_Space_Model_Components:
            vector_document_component_motion(
                component["name"], component["PosX"], component["PosY"]
            )


def destroy_vector_space_model():
    for component in Models_Data.Vector_Space_Model_Components:
        component["name"].place_forget()


def create_quit():
    MAIN_WINDOW.quit()


def create_main_window():

    def on_boolean_retrieval_model_button_enter(e):
        create_boolean_retrieval_model_button.config(
            background=BUTTON_FOREGROUND_COLOR, foreground=BUTTON_BACKGROUND_COLOR
        )

    def on_boolean_retrieval_model_button_leave(e):
        create_boolean_retrieval_model_button.config(
            background=BUTTON_BACKGROUND_COLOR, foreground=BUTTON_FOREGROUND_COLOR
        )

    def on_inverted_index_model_button_enter(e):
        create_inverted_index_model_button.config(
            background=INVERTED_BUTTON_FOREGROUND_COLOR,
            foreground=INVERTED_BUTTON_BACKGROUND_COLOR,
        )

    def on_inverted_index_model_button_leave(e):
        create_inverted_index_model_button.config(
            background=INVERTED_BUTTON_BACKGROUND_COLOR,
            foreground=INVERTED_BUTTON_FOREGROUND_COLOR,
        )

    def on_positional_index_model_button_enter(e):
        create_positional_index_model_button.config(
            background=POSITIONAL_BUTTON_FOREGROUND_COLOR,
            foreground=POSITIONAL_BUTTON_BACKGROUND_COLOR,
        )

    def on_positional_index_model_button_leave(e):
        create_positional_index_model_button.config(
            background=POSITIONAL_BUTTON_BACKGROUND_COLOR,
            foreground=POSITIONAL_BUTTON_FOREGROUND_COLOR,
        )

    def on_vector_space_model_button_enter(e):
        create_vector_space_model_button.config(
            background=Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
            foreground=Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        )

    def on_vector_space_model_button_leave(e):
        create_vector_space_model_button.config(
            background=Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
            foreground=Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
        )

    def on_quit_button_enter(e):
        create_quit_button.config(
            background=EXIT_WINDOW_FOREGROUND_COLOR,
            foreground=EXIT_WINDOW_BACKGROUND_COLOR,
        )

    def on_quit_button_leave(e):
        create_quit_button.config(
            background=EXIT_WINDOW_BACKGROUND_COLOR,
            foreground=EXIT_WINDOW_FOREGROUND_COLOR,
        )

    # Main Window Title
    main_window_title_config = {
        "label_size": "28",
        "label_text": "Search Engine Models",
        "label_background_color": TITLE_BACKGROUND_COLOR,
        "label_foreground_color": TITLE_FOREGROUND_COLOR,
    }
    main_window_title = create_label(main_window_title_config)

    # Create Boolean Retrieval Model Button
    create_boolean_retrieval_model_button_config = {
        "button_size": "20",
        "button_text": "Boolean Retrieval Model",
        "function_name": create_boolean_retrieval_model,
        "button_background_color": BUTTON_BACKGROUND_COLOR,
        "button_foreground_color": BUTTON_FOREGROUND_COLOR,
    }
    create_boolean_retrieval_model_button = create_button(
        create_boolean_retrieval_model_button_config
    )
    create_boolean_retrieval_model_button.bind(
        "<Enter>", on_boolean_retrieval_model_button_enter
    )
    create_boolean_retrieval_model_button.bind(
        "<Leave>", on_boolean_retrieval_model_button_leave
    )

    # Create Inverted Index Model Button
    create_inverted_index_model_button_config = {
        "button_size": "20",
        "button_text": "Inverted Index Model",
        "function_name": create_inverted_index_model,
        "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
        "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
    }
    create_inverted_index_model_button = create_button(
        create_inverted_index_model_button_config
    )
    create_inverted_index_model_button.bind(
        "<Enter>", on_inverted_index_model_button_enter
    )
    create_inverted_index_model_button.bind(
        "<Leave>", on_inverted_index_model_button_leave
    )

    # Create Positional Index Model Button
    create_positional_index_model_button_config = {
        "button_size": "20",
        "button_text": "Positional Index Model",
        "function_name": create_positional_index_model,
        "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
        "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
    }
    create_positional_index_model_button = create_button(
        create_positional_index_model_button_config
    )
    create_positional_index_model_button.bind(
        "<Enter>", on_positional_index_model_button_enter
    )
    create_positional_index_model_button.bind(
        "<Leave>", on_positional_index_model_button_leave
    )

    # Create Vector Space Model Button
    create_vector_space_model_button_config = {
        "button_size": "20",
        "button_text": "Vector Space Model",
        "function_name": create_vector_space_model,
        "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    }
    create_vector_space_model_button = create_button(
        create_vector_space_model_button_config
    )
    create_vector_space_model_button.bind("<Enter>", on_vector_space_model_button_enter)
    create_vector_space_model_button.bind("<Leave>", on_vector_space_model_button_leave)

    # Create Quit Button
    create_quit_button_config = {
        "button_size": "24",
        "button_text": "  Quit  ",
        "function_name": create_quit,
        "button_background_color": EXIT_WINDOW_BACKGROUND_COLOR,
        "button_foreground_color": EXIT_WINDOW_FOREGROUND_COLOR,
    }
    create_quit_button = create_button(create_quit_button_config)
    create_quit_button.bind("<Enter>", on_quit_button_enter)
    create_quit_button.bind("<Leave>", on_quit_button_leave)

    Models_Data.Main_Window_Components = [
        {"name": main_window_title, "PosX": 120, "PosY": 60},
        {"name": create_boolean_retrieval_model_button, "PosX": 140, "PosY": 160},
        {"name": create_inverted_index_model_button, "PosX": 164, "PosY": 230},
        {"name": create_positional_index_model_button, "PosX": 154, "PosY": 300},
        {"name": create_vector_space_model_button, "PosX": 164, "PosY": 370},
        {"name": create_quit_button, "PosX": 234, "PosY": 500},
    ]

    for component in Models_Data.Main_Window_Components:
        global STATE_VALUE
        STATE_VALUE = MAIN_WINDOW_STATE_VALUE
        main_menu_component_motion(
            component["name"], component["PosX"], component["PosY"]
        )
        STATE_VALUE = MODEL_STATE_VALUE


# this line to execute create_main_window when Back_Button is clicked
Back_Button.event.add_handler(create_main_window)


def task():
    destroy_loading_screen()
    MAIN_WINDOW.geometry(MAIN_WINDOW_SIZE)
    create_main_window()


# Main Window
def start_window():
    global MAIN_WINDOW
    MAIN_WINDOW.geometry(MAIN_WINDOW_SIZE)
    MAIN_WINDOW.title(MAIN_WINDOW_TITLE)
    MAIN_WINDOW["background"] = MAIN_WINDOW_BACKGROUND_COLOR
    window_center(MAIN_WINDOW)
    MAIN_WINDOW.resizable(width=False, height=False)
    create_loading_screen()
    MAIN_WINDOW.after(LOADING_SCREEN_TIME, task)
    load_background_image(MAIN_WINDOW)
    MAIN_WINDOW.mainloop()


############################################################################
