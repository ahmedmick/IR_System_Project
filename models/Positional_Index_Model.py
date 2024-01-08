# Imports

import tkinter as tk
from GUI_Components import *
from tkinter import filedialog
from Window_Center import window_center
from Stack_Data_Structure import Stack
from Text_File_Processing import (
    open_text_file,
    convert_list_to_string,
    get_file_name,
    unsorted_distinct_list,
)
from Window_Size_Fit_Contents import set_window_size_to_fit_contents
import Table_Adjustment
import Models_Data
from Back_Button import return_to_main_menu
from Preprocessing import stemming_text, tokenization_and_stemming
from Processing_Two_Lists import process_two_lists

############################################################################

# Constants

POSITIONAL_BUTTON_BACKGROUND_COLOR = "#711921"
POSITIONAL_BUTTON_FOREGROUND_COLOR = "white"
FIRST_STEP_COLUMNS_NAME = ["Term", "Document Number"]
SECOND_STEP_COLUMNS_NAME = ["Term", "Document Number"]
THIRD_STEP_COLUMNS_NAME = ["Term", "Frequency", "Posted List"]
TABLE_WINDOW_TITLE = "Table Window"
TABLE_WINDOW_BACKGROUND_COLOR = "white"
TABLE_WINDOW_FOREGROUND_COLOR = "white"
TITLE_FONT = "24"
TITLE_BACKGROUND_COLOR = "#333"
TITLE_FOREGROUND_COLOR = "white"
LABEL_BACKGROUND_COLOR = "#333"
LABEL_FOREGROUND_COLOR = "white"
OPERATIONS = {"AND": "AND", "OR": "OR", "NOT": "NOT"}
WORD_START_INDEX = 0
WORD_END_INDEX = 0
QUERY_STACK = Stack()
QUERY_TEXT = ""
ERROR_TEXT = "Query Couldn't be Solved:\nInput is not found"

############################################################################

# Functions


# Preprocessing
def add_new_document():
    data_file_path = filedialog.askopenfilenames()
    for file in data_file_path:
        text_file = open_text_file(file)
        text_file[0] = text_file[0].strip()
        text_file[0] = stemming_text(text_file[0])
        text_file_data = convert_list_to_string(text_file).split(" ")
        text_file_data = tokenization_and_stemming(text_file_data)
        Models_Data.Positional_Index_Model_WORDS += text_file_data
        Models_Data.Positional_Index_Model_WORDS = unsorted_distinct_list(
            Models_Data.Positional_Index_Model_WORDS
        )
        current_filename = get_file_name(file)
        if current_filename not in Models_Data.Positional_Index_Model_FILES_NAME:
            Models_Data.Positional_Index_Model_FILES_NAME.append(current_filename)
            Models_Data.Positional_Index_Model_NUMBER_OF_FILES += 1
            Models_Data.Positional_Index_Model_FILES_DATA.append(text_file)
        else:
            for i in range(0, len(Models_Data.Positional_Index_Model_FILES_NAME)):
                if Models_Data.Positional_Index_Model_FILES_NAME[i] == current_filename:
                    Models_Data.Positional_Index_Model_FILES_DATA[i - 1] = text_file

    print(Models_Data.Positional_Index_Model_FILES_DATA)


# Step 1: Create Table of every term and it's associated Document
def show_matrix_table():
    table_view = tk.Tk()
    table_view.title(TABLE_WINDOW_TITLE)
    table_view.resizable(width=False, height=False)
    table_view["background"] = TABLE_WINDOW_BACKGROUND_COLOR
    table = Table(table_view, Models_Data.Positional_Index_Model_MATRIX)

    # Call the function to adjust the window size
    set_window_size_to_fit_contents(table_view)

    table_view.geometry(
        str(Table_Adjustment.TABLE_WINDOW_X_AXIS)
        + "x"
        + str(Table_Adjustment.TABLE_WINDOW_Y_AXIS)
    )
    window_center(table_view)

    # table = ttk.Treeview(table_view, columns=Models_Data.Positional_Index_Model_FILES_NAME, show="headings")
    # for i in Models_Data.Positional_Index_Model_FILES_NAME:
    #     table.heading(i, text=i)
    # table.pack()


def create_data_table():
    matrix = [FIRST_STEP_COLUMNS_NAME]
    itr = 1
    for i in Models_Data.Positional_Index_Model_FILES_DATA:
        row = []
        for word in Models_Data.Positional_Index_Model_WORDS:
            if word in str(i):
                print(i)
                row.append(word)
                row.append(itr)
                matrix.append(row)
                row = []
        itr += 1

    Models_Data.Positional_Index_Model_MATRIX = matrix
    # show matrix using tree view
    show_matrix_table()


# Step 2: Sort Table of every term and it's associated Document
def sort_data_table():
    Models_Data.Positional_Index_Model_MATRIX = sorted(
        Models_Data.Positional_Index_Model_MATRIX
    )
    show_matrix_table()


# Step 3: Create Posted List of the Sorted Table
def create_posted_list():
    posted_list = [THIRD_STEP_COLUMNS_NAME]
    current_position = 1
    while current_position < len(Models_Data.Positional_Index_Model_MATRIX):
        term = Models_Data.Positional_Index_Model_MATRIX[current_position][0]
        documents = str(Models_Data.Positional_Index_Model_MATRIX[current_position][1])
        frequency = 1
        next_position = current_position + 1
        if (
            next_position < len(Models_Data.Positional_Index_Model_MATRIX)
            and term == Models_Data.Positional_Index_Model_MATRIX[next_position][0]
        ):
            current_position += 1
            while (
                current_position < len(Models_Data.Positional_Index_Model_MATRIX)
                and term
                == Models_Data.Positional_Index_Model_MATRIX[current_position][0]
            ):
                documents += "," + str(
                    Models_Data.Positional_Index_Model_MATRIX[current_position][1]
                )
                frequency += 1
                current_position += 1
            current_position -= 1

        row = [term, frequency, documents]
        print(row, current_position)
        posted_list.append(row)
        current_position += 1

    Models_Data.Positional_Index_Model_MATRIX = posted_list


# Step 4: Create Positional Index of Posted List
def find_all_positions(main_string, sub_string):
    positions = [
        i
        for i in range(len(main_string) - len(sub_string) + 1)
        if main_string[i : i + len(sub_string)] == sub_string
    ]
    return positions


def create_positional_index():
    create_posted_list()
    positional_index = Models_Data.Positional_Index_Model_MATRIX
    word_name = 0
    word_frequency = 1
    word_locations = 2
    for index, row in enumerate(positional_index):
        check = True
        multiple_files = False
        if index:
            positional_index_format = "["
            for character in row[word_locations]:
                if character.isnumeric() and not multiple_files:
                    word_locations_in_file = find_all_positions(
                        Models_Data.Positional_Index_Model_FILES_DATA[
                            int(character) - 1
                        ][0],
                        row[word_name],
                    )
                    positional_index[index][word_frequency] = str(
                        len(word_locations_in_file)
                    )
                    positional_index_format += f"{Models_Data.Positional_Index_Model_FILES_NAME[int(character)-1]}:{word_locations_in_file}"
                    multiple_files = True
                elif character.isnumeric() and multiple_files:
                    word_locations_in_file = find_all_positions(
                        Models_Data.Positional_Index_Model_FILES_DATA[
                            int(character) - 1
                        ][0],
                        row[word_name],
                    )
                    positional_index[index][
                        word_frequency
                    ] = f"{int(positional_index[index][word_frequency]) + len(word_locations_in_file)}"
                    positional_index_format += f",{Models_Data.Positional_Index_Model_FILES_NAME[int(character)-1]}:{word_locations_in_file}"
            positional_index_format += "]"
            if check:
                positional_index[index][
                    word_locations
                ] = positional_index_format.replace(" ", "")
                check = False
            else:
                print(f"posted_list = {positional_index[index][word_locations]}")
                positional_index[index][
                    word_locations
                ] += f",{positional_index_format.replace(' ','')}"
    Models_Data.Positional_Index_Model_MATRIX = positional_index
    show_matrix_table()


# Query Answer
def show_query_answer():
    global WORD_START_INDEX, WORD_END_INDEX, QUERY_STACK, QUERY_TEXT
    QUERY_TEXT = create_query_textbox.get("1.0", "end-1c")
    answer_text = stemming_text(QUERY_TEXT)
    words = answer_text.split(" ")
    words = [word.strip() for word in words if len(word.strip()) > 0]
    posted_list = Models_Data.Positional_Index_Model_MATRIX
    print(f"answer_text = {answer_text}")
    word_name = 0
    word_frequency = 1
    word_locations = 2
    words_related_to_query = []
    for i, word in enumerate(words):
        found = False
        for j, row in enumerate(posted_list):
            if word in row[word_name]:
                words[i] = row[word_locations]
                found = True
        if found:
            words_related_to_query.append(words[i])

    print(f"words_related_to_query = {words_related_to_query}")
    # create list to hold the files and positions where the query was found
    all_data = []
    query_answer_list = []

    if len(words_related_to_query) == 0:
        answer_text = ERROR_TEXT
    else:
        # TODO: check if there are any words related to query
        print(f"words = {words_related_to_query}")
        # words_related_to_query is a list of strings where each string
        # contains the files and positions of a word in the query
        # in the documents
        for i, word in enumerate(words_related_to_query):
            files_and_its_positions = []
            file_data = ""
            real_word = word[1:-1]
            for i, charater in enumerate(real_word):
                if i > 0 and charater == "," and real_word[i - 1] == "]":
                    files_and_its_positions.append(file_data)
                    file_data = ""
                    continue
                file_data += charater

            files_and_its_positions.append(file_data)
            # print(f"files_and_its_positions_before = {files_and_its_positions}")
            # file and positions variables are just to improve readability
            file = 0
            positions = 1
            for j, file_data in enumerate(files_and_its_positions):
                files_and_its_positions[j] = file_data.split(":")
                files_and_its_positions[j] = {
                    files_and_its_positions[j][file]: files_and_its_positions[j][
                        positions
                    ][1:-1].split(","),
                }
            all_data.append(files_and_its_positions)

    print(all_data)

    # intersection of all files in all_data list
    file = 0
    positions = 1
    query_files_list = []
    for index, word in enumerate(all_data):
        files_name = []
        for name in all_data[index]:
            files_name.append(str(list(name.keys())[0]))

        if index == 0:
            query_files_list.append(files_name)
        else:
            temp_list = [
                added_word
                for added_word in query_files_list[0]
                if added_word in files_name
            ]
            query_files_list = temp_list

    # query_files_list is a list of comman files where query exists
    print(f"query_files_list = {query_files_list}")

    # intersection of all positions of files in all_data list
    file = 0
    positions = 1
    query_positions_list = []
    for index, word in enumerate(all_data):
        positions_numbers = []
        for name in all_data[index]:
            file_name = str(list(name.keys())[0])
            if file_name in query_files_list:
                positions_numbers.append(name[file_name])

        query_positions_list.append(positions_numbers)

    print(f"query_positions_list = {query_positions_list}")

    # check if query is one word and in documents
    if len(answer_text.strip().split()) == 1:
        create_query_answer_textbox.insert("1.0", str(query_files_list))
        return

    # check if query_positions_list is empty
    for inner_list in query_positions_list:
        if not inner_list:
            create_query_answer_textbox.insert("1.0", ERROR_TEXT)
            return

    # intersection of all files and positions in all_data list
    # TODO:
    for file_number, file_name in enumerate(query_files_list):
        temp_list = []
        for position in query_positions_list:
            temp_list.append(position[file_number])
        query_answer_list.append(temp_list)

    # print(f"query_answer_list = {query_answer_list}")

    # change in indexes of the query_answer_list to list of positions in files
    for position_number, position_value in enumerate(query_answer_list):
        matched_positions = []
        for index, value in enumerate(position_value):
            if index == 0:
                matched_positions.append(value)
                continue
            files_name = Models_Data.Positional_Index_Model_FILES_NAME
            files_data = Models_Data.Positional_Index_Model_FILES_DATA
            processed_two_lists = process_two_lists(
                query_files_list[position_number],
                files_name,
                files_data,
                matched_positions[-1],
                value,
            )

            matched_positions.append(processed_two_lists)
        query_answer_list[position_number] = matched_positions

    print(f"query_answer_list = {query_answer_list}")

    # check if the query exists
    # Transpose the inner lists
    transposed_lists = [
        list(map(list, zip(*inner_list))) for inner_list in query_answer_list
    ]

    # Reshape the list and convert tuples to lists
    reshaped_list = [list(map(list, sublist)) for sublist in transposed_lists]

    print(f"reshaped list = {reshaped_list}")

    # reshaped_list = [[["0", "4"], ["16", "-1"], ["35", "-1"]], [["0", "4"]]]

    # Remove inner lists containing '-1'
    filtered_list = [
        [inner_list for inner_list in sublist if "-1" not in inner_list]
        for sublist in reshaped_list
    ]

    print(filtered_list)

    for pos, val in enumerate(query_answer_list):
        temp = {query_files_list[pos]: filtered_list[pos]}
        query_answer_list[pos] = temp

    print(f"query_answer_list = {query_answer_list}")

    if len(query_answer_list) == 0:
        answer_text = ERROR_TEXT
    else:
        answer_text = ""
        for value in query_answer_list:
            key_value = str(list(value.keys())[0])
            answer_text += f"{key_value}:\n{value[key_value]}\n"
    create_query_answer_textbox.insert("1.0", answer_text)


def clear_query():
    create_query_textbox.delete("1.0", END)
    create_query_answer_textbox.delete("1.0", END)


############################################################################

# Components
# Title
positional_index_title_config = {
    "label_size": "28",
    "label_text": "Positional Index Model",
    "label_background_color": TITLE_BACKGROUND_COLOR,
    "label_foreground_color": TITLE_FOREGROUND_COLOR,
}
positional_index_title = create_label(positional_index_title_config)

# Create Add_New_Document Label
add_new_document_label_config = {
    "label_size": "15",
    "label_text": "Preprocessing:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
add_new_document_label = create_label(add_new_document_label_config)

# Create Add_New_Document button
add_new_document_button_config = {
    "button_size": "15",
    "button_text": "Add New Document",
    "function_name": add_new_document,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
add_new_document_button = create_button(add_new_document_button_config)

# Create Data Table Label
create_data_table_label_config = {
    "label_size": "15",
    "label_text": "First Step:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_data_table_label = create_label(create_data_table_label_config)

# Create Create_Data_Table button
create_data_table_button_config = {
    "button_size": "15",
    "button_text": "Create Data Table",
    "function_name": create_data_table,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
create_data_table_button = create_button(create_data_table_button_config)

# Sort Data Table Label
sort_data_table_label_config = {
    "label_size": "15",
    "label_text": "Second Step:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
sort_data_table_label = create_label(sort_data_table_label_config)

# Create Sort_Data_Table button
sort_data_table_button_config = {
    "button_size": "15",
    "button_text": "Sort Data Table",
    "function_name": sort_data_table,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
sort_data_table_button = create_button(sort_data_table_button_config)

# Create Positional Index List Label
create_positional_index_label_config = {
    "label_size": "15",
    "label_text": "Third Step:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_positional_index_label = create_label(create_positional_index_label_config)

# Create Create_Positional_Index button
create_positional_index_button_config = {
    "button_size": "15",
    "button_text": "Create Postional Index",
    "function_name": create_positional_index,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
create_positional_index_button = create_button(create_positional_index_button_config)

# Create Query Label
create_query_label_config = {
    "label_size": "15",
    "label_text": "Enter Phrase Query:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_query_label = create_label(create_query_label_config)

############################################################################

# Create Query Rules Page
# TODO: Create Query Rules Page
# 1 - use parentheses around every operation
# 2 - Operators like "AND" , "OR" must be used in Capital Case
# 3 - You Should Space Between Operand and Operator:
#   3.1 - Operand: "It's a Word from Matrix's Table"
#   3.2 - Operator: "It's a bitwise operation like 'AND' and 'OR'"


############################################################################

# Create Query Textbox
create_query_textbox_config = {
    "textbox_size": "20",
    "height": 1,
    "width": 22,
    "textbox_background_color": LABEL_BACKGROUND_COLOR,
    "textbox_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_query_textbox = create_textbox(create_query_textbox_config)

############################################################################

# Create Show Query Answer Button
create_show_query_answer_button_config = {
    "button_size": "15",
    "button_text": "Show Query Answer",
    "function_name": show_query_answer,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
create_show_query_answer_button = create_button(create_show_query_answer_button_config)

############################################################################

# Create Clear Query textbox Button
create_clear_query_textbox_button_config = {
    "button_size": "15",
    "button_text": "Clear Query",
    "function_name": clear_query,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
create_clear_query_textbox_button = create_button(
    create_clear_query_textbox_button_config
)

############################################################################

# Create Query Answer Textbox
create_query_answer_textbox_config = {
    "textbox_size": "20",
    "height": 3,
    "width": 30,
    "textbox_background_color": LABEL_BACKGROUND_COLOR,
    "textbox_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_query_answer_textbox = create_textbox(create_query_answer_textbox_config)

############################################################################

# Create Back Button

create_back_button_config = {
    "button_size": "18",
    "button_text": "Main Menu",
    "function_name": return_to_main_menu,
    "button_background_color": POSITIONAL_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": POSITIONAL_BUTTON_FOREGROUND_COLOR,
}
create_back_button = create_button(create_back_button_config)

############################################################################

# Query Examples:
# (Ahmed AND Fathy)
# (Ahmed OR Fathy)
# (NOT Ahmed)
# (NOT (NOT Ahmed))

############################################################################

Models_Data.Positional_Index_Model_Components = [
    {"name": positional_index_title, "PosX": 140, "PosY": 30},
    {"name": add_new_document_label, "PosX": 150, "PosY": 115},
    {"name": add_new_document_button, "PosX": 310, "PosY": 110},
    {"name": create_data_table_label, "PosX": 150, "PosY": 175},
    {"name": create_data_table_button, "PosX": 310, "PosY": 170},
    {"name": sort_data_table_label, "PosX": 150, "PosY": 230},
    {"name": sort_data_table_button, "PosX": 310, "PosY": 230},
    {"name": create_positional_index_label, "PosX": 150, "PosY": 290},
    {"name": create_positional_index_button, "PosX": 310, "PosY": 290},
    {"name": create_query_label, "PosX": 35, "PosY": 350},
    {"name": create_query_textbox, "PosX": 235, "PosY": 345},
    {"name": create_show_query_answer_button, "PosX": 140, "PosY": 410},
    {"name": create_clear_query_textbox_button, "PosX": 360, "PosY": 410},
    {"name": create_query_answer_textbox, "PosX": 80, "PosY": 470},
    {"name": create_back_button, "PosX": 240, "PosY": 590},
]
