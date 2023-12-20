# Imports
import tkinter as tk
from tkinter import filedialog, END
from Window_Center import window_center
from Stack_Data_Structure import Stack
from GUI_Components import *
from Window_Size_Fit_Contents import set_window_size_to_fit_contents
from Text_File_Processing import (
    open_text_file,
    convert_list_to_string,
    get_file_name,
    unsorted_distinct_list,
)
import re
import Table_Adjustment
import Models_Data
from Back_Button import return_to_main_menu
from Preprocessing import stemming_text, tokenization_and_stemming

############################################################################

# Constants
INVERTED_BUTTON_BACKGROUND_COLOR = "darkcyan"
INVERTED_BUTTON_FOREGROUND_COLOR = "white"
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
ERROR_TEXT = "Query Couldn't be Solved:\nInvalid Operation"

############################################################################

# Functions

# Preprocessing: Add Documents


def add_new_document():
    data_file_path = filedialog.askopenfilenames()
    for file in data_file_path:
        text_file = open_text_file(file)
        text_file[0] = text_file[0].strip()
        text_file[0] = stemming_text(text_file[0])
        text_file_data = convert_list_to_string(text_file).split(" ")
        text_file_data = tokenization_and_stemming(text_file_data)
        Models_Data.Inverted_Index_Model_WORDS += text_file_data
        Models_Data.Inverted_Index_Model_WORDS = unsorted_distinct_list(
            Models_Data.Inverted_Index_Model_WORDS
        )
        current_filename = get_file_name(file)
        if current_filename not in Models_Data.Inverted_Index_Model_FILES_NAME:
            Models_Data.Inverted_Index_Model_FILES_NAME.append(current_filename)
            Models_Data.Inverted_Index_Model_NUMBER_OF_FILES += 1
            Models_Data.Inverted_Index_Model_FILES_DATA.append(text_file)
        else:
            for i in range(0, len(Models_Data.Inverted_Index_Model_FILES_NAME)):
                if Models_Data.Inverted_Index_Model_FILES_NAME[i] == current_filename:
                    Models_Data.Inverted_Index_Model_FILES_DATA[i - 1] = text_file

    print(Models_Data.Inverted_Index_Model_FILES_DATA)


# Step 1: Create Table of every term and it's associated Document
def show_matrix_table():
    table_view = tk.Tk()
    table_view.title(TABLE_WINDOW_TITLE)
    table_view.resizable(width=False, height=False)
    table_view["background"] = TABLE_WINDOW_BACKGROUND_COLOR
    table = Table(table_view, Models_Data.Inverted_Index_Model_MATRIX)

    # Call the function to adjust the window size
    set_window_size_to_fit_contents(table_view)

    table_view.geometry(
        str(Table_Adjustment.TABLE_WINDOW_X_AXIS)
        + "x"
        + str(Table_Adjustment.TABLE_WINDOW_Y_AXIS)
    )
    window_center(table_view)

    # table = ttk.Treeview(table_view, columns=Models_Data.Inverted_Index_Model_FILES_NAME, show="headings")
    # for i in Models_Data.Inverted_Index_Model_FILES_NAME:
    #     table.heading(i, text=i)
    # table.pack()


def create_data_table():
    matrix = [FIRST_STEP_COLUMNS_NAME]
    itr = 1
    for i in Models_Data.Inverted_Index_Model_FILES_DATA:
        row = []
        for word in Models_Data.Inverted_Index_Model_WORDS:
            if word in str(i):
                print(i)
                row.append(word)
                row.append(itr)
                matrix.append(row)
                row = []
        itr += 1

    Models_Data.Inverted_Index_Model_MATRIX = matrix
    # show matrix using tree view
    show_matrix_table()


# Step 2: Sort Table of every term and it's associated Document
def sort_data_table():
    Models_Data.Inverted_Index_Model_MATRIX = Models_Data.Inverted_Index_Model_MATRIX[
        :2
    ] + sorted(Models_Data.Inverted_Index_Model_MATRIX[2:])
    show_matrix_table()


# Step 3: Create Posted List of the Sorted Table
def create_posted_list():
    posted_list = [THIRD_STEP_COLUMNS_NAME]
    i = 1
    while i < len(Models_Data.Inverted_Index_Model_MATRIX):
        term = Models_Data.Inverted_Index_Model_MATRIX[i][0]
        documents = str(Models_Data.Inverted_Index_Model_MATRIX[i][1])
        frequency = 1
        if (
            i + 1 < len(Models_Data.Inverted_Index_Model_MATRIX)
            and term == Models_Data.Inverted_Index_Model_MATRIX[i + 1][0]
        ):
            i += 1
            while (
                i < len(Models_Data.Inverted_Index_Model_MATRIX)
                and term == Models_Data.Inverted_Index_Model_MATRIX[i][0]
            ):
                documents += "," + str(Models_Data.Inverted_Index_Model_MATRIX[i][1])
                frequency += 1
                i += 1

        row = [term, frequency, documents]
        print(row, i)
        posted_list.append(row)
        i += 1

    Models_Data.Inverted_Index_Model_MATRIX = posted_list
    show_matrix_table()


# Query Processing


def bitwise_operation(operand, operator):
    operation_solution = ""
    match operator:
        case "AND":
            first_word_posted_list = operand[0][1:-1].strip().split(",")
            second_word_posted_list = operand[2][1:-1].strip().split(",")
            answer_posted_list = list(
                set(first_word_posted_list) & set(second_word_posted_list)
            )
            operation_solution = "[" + "".join(str(e) + "," for e in answer_posted_list)
            operation_solution = operation_solution[:-1] + "]"
            print(operation_solution)
        case "OR":
            first_word_posted_list = operand[0][1:-1].strip().split(",")
            second_word_posted_list = operand[2][1:-1].strip().split(",")
            answer_posted_list = sorted(
                list(set(first_word_posted_list) | set(second_word_posted_list))
            )
            operation_solution = "[" + "".join(str(e) + "," for e in answer_posted_list)
            operation_solution = operation_solution[:-1] + "]"
        case "NOT":
            operand = list(operand)
            print(f"operand = {operand}")
            temp = "["
            for i in range(
                1, len(Models_Data.Inverted_Index_Model_FILES_NAME) + 1
            ):  # operand = ['[', '1', ']']
                if str(i) not in operand:
                    temp += str(i) + ","
            temp = temp[:-1] + "]"
            operation_solution = "".join(temp)

    return operation_solution


def solve_operation(start, end):
    global QUERY_STACK, QUERY_TEXT, OPERATIONS
    operation = QUERY_TEXT[start + 1 : end].strip().split(" ")
    check = True
    if len(operation) == 1:
        temp = operation[0][1 : end - 2].strip().split(",")
        print(temp)
        for i in range(0, len(temp)):
            if not str(temp[i]).isnumeric():
                check = False
                break
        if check:
            QUERY_TEXT = QUERY_TEXT.replace(QUERY_TEXT[start : end + 1], operation[0])
    elif len(operation) == 2:
        if operation[0] != "NOT":
            check = False
        temp = operation[1][1 : len(operation[1]) - 1].strip().split(",")
        print(f"temp = {temp}")
        for i in range(0, len(temp)):
            if not str(temp[i]).isnumeric():
                check = False
                break
        if check:
            solution = bitwise_operation(operation[1], OPERATIONS["NOT"])
            QUERY_TEXT = QUERY_TEXT.replace(QUERY_TEXT[start : end + 1], solution)
    elif len(operation) == 3:
        if operation[1] not in OPERATIONS:
            check = False
        first_operand = operation[0][1 : len(operation[0]) - 1].strip().split(",")
        second_operand = operation[2][1 : len(operation[2]) - 1].strip().split(",")
        print(f"first_operand = {first_operand}")
        print(f"second_operand = {second_operand}")
        for i in range(0, len(first_operand)):
            if not str(first_operand[i]).isnumeric():
                print("first_operand_check")
                check = False
                break
        for i in range(0, len(second_operand)):
            if not str(second_operand[i]).isnumeric():
                print("second_operand_check")
                check = False
                break
        if check:
            solution = bitwise_operation(operation, operation[1])
            QUERY_TEXT = QUERY_TEXT.replace(QUERY_TEXT[start : end + 1], solution)
    else:
        check = False

    return check


def query_answer():
    global WORD_START_INDEX, WORD_END_INDEX, QUERY_STACK, QUERY_TEXT
    QUERY_TEXT = create_query_textbox.get("1.0", "end-1c")
    # change Words in Query to binary format
    i = 0
    while i < len(QUERY_TEXT):
        if QUERY_TEXT[i].isalpha():
            # Change Word in query_text to binary number
            word = ""
            WORD_START_INDEX = i
            WORD_END_INDEX = i
            while i < len(QUERY_TEXT) and QUERY_TEXT[i].isalpha():
                WORD_END_INDEX = i
                word += QUERY_TEXT[i]
                i += 1
            orginal_word = word
            if len(word) > 0:
                word = stemming_text(word)
            if word in Models_Data.Inverted_Index_Model_WORDS:
                word_found = False
                total_rows = len(Models_Data.Inverted_Index_Model_MATRIX)
                total_columns = len(Models_Data.Inverted_Index_Model_MATRIX[0])
                temp = ""
                for ind in range(total_rows):
                    for j in range(total_columns):
                        if (
                            j == 0
                            and Models_Data.Inverted_Index_Model_MATRIX[ind][j] == word
                        ):
                            word_found = True
                            temp = (
                                "["
                                + Models_Data.Inverted_Index_Model_MATRIX[ind][j + 2]
                                + "]"
                            )
                            # j += 1
                            # while j < total_columns:
                            #     temp += Models_Data.Inverted_Index_Model_MATRIX[ind][j]
                            #     j += 1
                            # break
                    if word_found:
                        # replace word with temp
                        QUERY_TEXT = re.sub(orginal_word, temp, QUERY_TEXT)
                        i = 0  # start processing quert_text from the beginning
                        break
        i += 1
    print(QUERY_TEXT)
    # Check Query Format
    i, left_brace, right_brace = 0, 0, 0
    while i < len(QUERY_TEXT):
        if QUERY_TEXT[i] == "(":
            QUERY_STACK.push("(")
            left_brace += 1
        elif QUERY_TEXT[i] == ")":
            QUERY_STACK.pop()
            right_brace += 1
        if right_brace > left_brace:
            return ERROR_TEXT
        i += 1

    if not QUERY_STACK.isEmpty() or left_brace != right_brace:
        return ERROR_TEXT

    # Query Processing
    answer = ""
    i = 0
    while i < len(QUERY_TEXT) or not QUERY_STACK.isEmpty():
        match QUERY_TEXT[i]:
            case "(":
                QUERY_STACK.push(i)
            case ")":
                check = solve_operation(QUERY_STACK.top(), i)
                if check:
                    QUERY_STACK.pop()
                else:
                    return ERROR_TEXT
                i = 0
            case _:
                pass
        i += 1
    answer = QUERY_TEXT
    return answer


def show_query_answer():
    answer = query_answer()
    if answer == ERROR_TEXT:
        create_query_answer_textbox.insert("1.0", ERROR_TEXT)
    elif answer == "]":
        # show answer in tree view
        answer_text = f"Query Answer:\n[]\nFiles:\nNo Files Matched"  # [1,2,3]
        create_query_answer_textbox.insert("1.0", answer_text)
    else:
        # show answer in tree view
        answer_text = f"Query Answer:\n{answer}\nFiles:\n"  # [1,2,3]
        for i in range(1, len(answer) - 1, 2):  #  1 2 3
            print(answer[i])
            answer_text += (
                Models_Data.Inverted_Index_Model_FILES_NAME[int(answer[i]) - 1] + "\n"
            )
        create_query_answer_textbox.insert("1.0", answer_text)


def clear_query():
    create_query_textbox.delete("1.0", END)
    create_query_answer_textbox.delete("1.0", END)


############################################################################

# Components
# Title
inverted_index_title_config = {
    "label_size": "28",
    "label_text": "Inverted Index Model",
    "label_background_color": TITLE_BACKGROUND_COLOR,
    "label_foreground_color": TITLE_FOREGROUND_COLOR,
}
inverted_index_title = create_label(inverted_index_title_config)

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
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
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
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
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
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
}
sort_data_table_button = create_button(sort_data_table_button_config)

# Create Posted List Label
create_posted_list_label_config = {
    "label_size": "15",
    "label_text": "Third Step:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_posted_list_label = create_label(create_posted_list_label_config)

# Create Create_Posted_List button
create_posted_list_button_config = {
    "button_size": "15",
    "button_text": "Create Posted List",
    "function_name": create_posted_list,
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
}
create_posted_list_button = create_button(create_posted_list_button_config)

# Create Query Label
create_query_label_config = {
    "label_size": "15",
    "label_text": "Enter Query:",
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
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
}
create_show_query_answer_button = create_button(create_show_query_answer_button_config)

############################################################################

# Create Clear Query textbox Button
create_clear_query_textbox_button_config = {
    "button_size": "15",
    "button_text": "Clear Query",
    "function_name": clear_query,
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
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

# Create Back Button

create_back_button_config = {
    "button_size": "18",
    "button_text": "Main Menu",
    "function_name": return_to_main_menu,
    "button_background_color": INVERTED_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": INVERTED_BUTTON_FOREGROUND_COLOR,
}
create_back_button = create_button(create_back_button_config)

############################################################################

# Query Examples:
# (Ahmed AND Fathy)
# (Ahmed OR Fathy)
# (NOT Ahmed)
# (NOT (NOT Ahmed))

############################################################################

Models_Data.Inverted_Index_Model_Components = [
    {"name": inverted_index_title, "PosX": 140, "PosY": 30},
    {"name": add_new_document_label, "PosX": 150, "PosY": 115},
    {"name": add_new_document_button, "PosX": 310, "PosY": 110},
    {"name": create_data_table_label, "PosX": 150, "PosY": 175},
    {"name": create_data_table_button, "PosX": 310, "PosY": 170},
    {"name": sort_data_table_label, "PosX": 150, "PosY": 230},
    {"name": sort_data_table_button, "PosX": 310, "PosY": 230},
    {"name": create_posted_list_label, "PosX": 150, "PosY": 290},
    {"name": create_posted_list_button, "PosX": 310, "PosY": 290},
    {"name": create_query_label, "PosX": 80, "PosY": 350},
    {"name": create_query_textbox, "PosX": 230, "PosY": 345},
    {"name": create_show_query_answer_button, "PosX": 140, "PosY": 410},
    {"name": create_clear_query_textbox_button, "PosX": 360, "PosY": 410},
    {"name": create_query_answer_textbox, "PosX": 80, "PosY": 470},
    {"name": create_back_button, "PosX": 240, "PosY": 590},
]
