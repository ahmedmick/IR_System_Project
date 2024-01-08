# Imports

from multiprocessing import Value
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
from Preprocessing import (
    stemming_list,
    stemming_text,
    stemming_word,
    tokenization_and_stemming,
)
import math
from Animations import vector_document_component_motion, vector_query_component_motion
import Buttons_Color

############################################################################

# Constants

Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR = "#363062"
Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR = "white"
Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR = "#940B92"
Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR = "white"
# Document
TF_COLUMNS_NAME = ["Term"]
TF_VALUES = []
WTF_COLUMNS_NAME = ["Term"]
WTF_VALUES = []
DF_COLUMNS_NAME = ["Term", "df"]
DF_VALUES = []
IDF_COLUMNS_NAME = ["Term", "idf"]
IDF_VALUES = []
DF_AND_IDF_COLUMNS_NAME = ["Term", "df", "idf"]
DF_AND_IDF_VALUES = []
TF_IDF_COLUMNS_NAME = ["Term"]
TF_IDF_VALUES = []
LENGTH_COLUMNS_NAME = ["Document", "Length"]
LENGTH_VALUES = []
NORMALIZED_TF_IDF_COLUMNS_NAME = ["Term"]
NORMALIZED_TF_IDF_VALUES = []
# Query
TF_QUERY_COLUMNS_NAME = ["Term", "TF"]
TF_QUERY_VALUES = []
WTF_QUERY_COLUMNS_NAME = ["Term", "W-TF"]
WTF_QUERY_VALUES = []
DF_QUERY_COLUMNS_NAME = ["Term", "DF"]
DF_QUERY_VALUES = []
IDF_QUERY_COLUMNS_NAME = ["Term", "IDF"]
IDF_QUERY_VALUES = []
DF_AND_IDF_QUERY_COLUMNS_NAME = ["Term", "DF", "IDF"]
DF_AND_IDF_QUERY_VALUES = []
TF_IDF_QUERY_COLUMNS_NAME = ["Term", "TF-IDF"]
TF_IDF_QUERY_VALUES = []
LENGTH_QUERY_COLUMNS_NAME = ["#", "Length"]
LENGTH_QUERY_VALUES = []
NORMALIZED_TF_IDF_QUERY_COLUMNS_NAME = ["Term", "Normalized"]
NORMALIZED_TF_IDF_QUERY_VALUES = []
QUERY_TABLE_COLUMNS_NAME = [
    "Term",
    "tf-raw",
    "wtf(1 + log(tf))",
    "df",
    "idf",
    "tf*idf",
    "normalized",
]
QUERY_TABLE_VALUES = []
SIMILARITY_TABLE_COLUMNS_NAME = ["#", "Similarity"]
SIMILARITY_VALUES = []
MATCHED_DOCUMENTS = []

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
BOOLEAN_PHRASE_QUERY_TEXT = ""
ERROR_TEXT = "Query Couldn't be Solved:\nInput is not found"
EMPTY_QUERY_ERROR_TEXT = "Invalid Query:\nEmpty Input"
PHRASE_QUERY_ANSWER_TEXT = ""
BOOLEAN_PHRASE_QUERY_ANSWER_TEXT = ""
Query_Page_Components = []
Document_Page_Components = []

############################################################################

# Functions


# Document functions
# Preprocessing
def add_new_document():
    data_file_path = filedialog.askopenfilenames()
    for file in data_file_path:
        text_file = open_text_file(file)
        text_file[0] = text_file[0].strip()
        text_file[0] = stemming_text(text_file[0])
        text_file_data = convert_list_to_string(text_file).split(" ")
        text_file_data = tokenization_and_stemming(text_file_data)
        Models_Data.Vector_Space_Model_WORDS += text_file_data
        Models_Data.Vector_Space_Model_WORDS = unsorted_distinct_list(
            Models_Data.Vector_Space_Model_WORDS
        )
        Models_Data.Vector_Space_Model_WORDS = sorted(
            Models_Data.Vector_Space_Model_WORDS
        )
        current_filename = get_file_name(file)
        if current_filename not in Models_Data.Vector_Space_Model_FILES_NAME:
            Models_Data.Vector_Space_Model_FILES_NAME.append(current_filename)
            Models_Data.Vector_Space_Model_NUMBER_OF_FILES += 1
            Models_Data.Vector_Space_Model_FILES_DATA.append(text_file)
        else:
            for i in range(0, len(Models_Data.Vector_Space_Model_FILES_NAME)):
                if Models_Data.Vector_Space_Model_FILES_NAME[i] == current_filename:
                    Models_Data.Vector_Space_Model_FILES_DATA[i - 1] = text_file
    if len(Models_Data.Vector_Space_Model_FILES_DATA) > 0:
        change_selected_button_color(
            add_new_document_button,
            Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
            Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
        )
    print(Models_Data.Vector_Space_Model_FILES_DATA)


# Show Matrix
def show_matrix_table():
    table_view = tk.Tk()
    table_view.title(TABLE_WINDOW_TITLE)
    table_view.resizable(width=False, height=False)
    table_view["background"] = TABLE_WINDOW_BACKGROUND_COLOR
    table = Table(table_view, Models_Data.Vector_Space_Model_MATRIX)

    # Call the function to adjust the window size
    set_window_size_to_fit_contents(table_view)

    table_view.geometry(
        str(Table_Adjustment.TABLE_WINDOW_X_AXIS)
        + "x"
        + str(Table_Adjustment.TABLE_WINDOW_Y_AXIS)
    )
    window_center(table_view)


# create Term Frequency table
def create_tf_table():
    matrix = [TF_COLUMNS_NAME + Models_Data.Vector_Space_Model_FILES_NAME]
    for word in Models_Data.Vector_Space_Model_WORDS:
        row = [word]
        values = []
        for text in Models_Data.Vector_Space_Model_FILES_DATA:
            if word in str(text[0]).split():
                value = str(text).count(word)
                row.append(str(value))
                values.append(value)
            else:
                row.append("0")
                values.append(0)
        matrix.append(row)
        TF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix
    change_selected_button_color(
        add_new_document_button,
        Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    )
    change_selected_button_color(
        tf_table_button,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
    )
    # show matrix using tree view
    show_matrix_table()


# create Weighted Term Frequency table
def create_wtf_table():
    matrix = [WTF_COLUMNS_NAME + Models_Data.Vector_Space_Model_FILES_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        row = [word]
        values = []
        for y, text in enumerate(Models_Data.Vector_Space_Model_FILES_DATA):
            value = TF_VALUES[x][y]
            if value in [0, 1]:
                row.append(str(value))
                values.append(value)
            else:
                row.append(str(1 + math.log(value, 10)))
                values.append(value)
        matrix.append(row)
        WTF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix
    change_selected_button_color(
        tf_table_button,
        Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    )
    change_selected_button_color(
        wtf_table_button,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
    )
    # show matrix using tree view
    show_matrix_table()


# create Document Frequency table
def create_df_table():
    matrix = [DF_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        row = [word, "0"]
        values = [0]
        for y, text in enumerate(Models_Data.Vector_Space_Model_FILES_DATA):
            value = TF_VALUES[x][y]
            if value > 0:
                values[0] += 1
                row[1] = str(values[0])

        matrix.append(row)
        DF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_table() # remove comment in case you want show df table


# create Inverse Document Frequency table
def create_idf_table():
    matrix = [IDF_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        number_of_documents = Models_Data.Vector_Space_Model_NUMBER_OF_FILES
        document_frequency = DF_VALUES[x][0]

        if document_frequency == 0:
            document_frequency = 1
        value = math.log(number_of_documents / document_frequency, 10)
        value = round(value, 9)
        row = [word, str(value)]
        values = [value]
        matrix.append(row)
        IDF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_table() # remove comment in case you want show df table


# create Document Frequency and Inverse Document Frequency table
def create_df_and_idf_table():
    create_df_table()
    create_idf_table()
    matrix = [DF_AND_IDF_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        row = [word, str(DF_VALUES[x][0]), str(IDF_VALUES[x][0])]
        values = [DF_VALUES[x][0], IDF_VALUES[x][0]]
        matrix.append(row)
        DF_AND_IDF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix
    change_selected_button_color(
        wtf_table_button,
        Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    )
    change_selected_button_color(
        df_and_idf_table_button,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
    )
    # show matrix using tree view
    show_matrix_table()


# create TF-IDF table
def create_tf_idf_table():
    matrix = [TF_IDF_COLUMNS_NAME + Models_Data.Vector_Space_Model_FILES_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        row = [word]
        values = []
        for y, text in enumerate(Models_Data.Vector_Space_Model_FILES_DATA):
            value = WTF_VALUES[x][y] * IDF_VALUES[x][0]
            row.append(str(value))
            values.append(value)

        matrix.append(row)
        TF_IDF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix
    change_selected_button_color(
        df_and_idf_table_button,
        Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    )
    change_selected_button_color(
        tf_idf_table_button,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
    )
    # show matrix using tree view
    show_matrix_table()


# create Document Length table
def create_length_table():
    matrix = [LENGTH_COLUMNS_NAME]
    number_of_rows = len(TF_IDF_VALUES)
    number_of_columns = len(TF_IDF_VALUES[0])
    # Iterate over columns
    for col in range(number_of_columns):
        row_data = [Models_Data.Vector_Space_Model_FILES_NAME[col]]
        values = []
        sum_of_tf_idf_values = 0
        # Iterate over rows
        for row in range(number_of_rows):
            value = TF_IDF_VALUES[row][col]
            sum_of_tf_idf_values += value * value

        sum_of_tf_idf_values = round(math.sqrt(sum_of_tf_idf_values), 9)
        row_data.append(str(sum_of_tf_idf_values))
        values.append(sum_of_tf_idf_values)
        matrix.append(row_data)
        LENGTH_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix
    change_selected_button_color(
        tf_idf_table_button,
        Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    )
    change_selected_button_color(
        length_table_button,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
    )
    # show matrix using tree view
    show_matrix_table()  # remove comment in case you want show df table


# create Normalized TF-IDF table
def create_normalized_tf_idf_table():
    matrix = [
        NORMALIZED_TF_IDF_COLUMNS_NAME + Models_Data.Vector_Space_Model_FILES_NAME
    ]
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        row = [word]
        values = []
        for y, text in enumerate(Models_Data.Vector_Space_Model_FILES_NAME):
            value = round(TF_IDF_VALUES[x][y] / LENGTH_VALUES[y][0], 9)
            row.append(str(value))
            values.append(value)

        matrix.append(row)
        NORMALIZED_TF_IDF_VALUES.append(values)
    Models_Data.Vector_Space_Model_MATRIX = matrix
    change_selected_button_color(
        length_table_button,
        Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
    )
    change_selected_button_color(
        normalized_tf_idf_table_button,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_BACKGROUND_COLOR,
        Buttons_Color.VECTOR_SPACE_SELECTED_BUTTON_FOREGROUND_COLOR,
    )
    # show matrix using tree view
    show_matrix_table()


# Query Page button
def query_page_button():
    global Document_Page_Components
    Document_Page_Components = Models_Data.Vector_Space_Model_Components
    for component in Models_Data.Vector_Space_Model_Components:
        component["name"].place_forget()
    for component in Query_Page_Components:
        vector_query_component_motion(
            component["name"], component["PosX"], component["PosY"]
        )


# Document Page button
def document_page_button():
    for component in Query_Page_Components:
        component["name"].place_forget()
    for component in Document_Page_Components:
        vector_document_component_motion(
            component["name"], component["PosX"], component["PosY"]
        )


#################################################################################
#################################################################################
#################################################################################
#################################################################################
#################################################################################

# Query functions


# Show Matrix
def show_matrix_query_table():
    table_view = tk.Tk()
    table_view.title(TABLE_WINDOW_TITLE)
    table_view.resizable(width=False, height=False)
    table_view["background"] = TABLE_WINDOW_BACKGROUND_COLOR
    table = Table(table_view, Models_Data.Vector_Space_Model_Query_MATRIX)

    # Call the function to adjust the window size
    set_window_size_to_fit_contents(table_view)

    table_view.geometry(
        str(Table_Adjustment.TABLE_WINDOW_X_AXIS)
        + "x"
        + str(Table_Adjustment.TABLE_WINDOW_Y_AXIS)
    )
    window_center(table_view)


# Preprocessing
def clear_all_fields():
    global TF_QUERY_COLUMNS_NAME, TF_QUERY_VALUES, WTF_QUERY_COLUMNS_NAME
    global WTF_QUERY_VALUES, DF_QUERY_COLUMNS_NAME, DF_QUERY_VALUES
    global IDF_QUERY_COLUMNS_NAME, IDF_QUERY_VALUES
    global DF_AND_IDF_QUERY_COLUMNS_NAME, DF_AND_IDF_QUERY_VALUES
    global TF_IDF_QUERY_COLUMNS_NAME, TF_IDF_QUERY_VALUES
    global LENGTH_QUERY_COLUMNS_NAME, LENGTH_QUERY_VALUES
    global NORMALIZED_TF_IDF_QUERY_COLUMNS_NAME, NORMALIZED_TF_IDF_QUERY_VALUES
    global QUERY_TABLE_COLUMNS_NAME, SIMILARITY_TABLE_COLUMNS_NAME
    global SIMILARITY_VALUES, MATCHED_DOCUMENTS

    Models_Data.Vector_Space_Model_Query_FILES_NAME = ["Query"]
    Models_Data.Vector_Space_Model_Query_FILES_DATA = [stemming_text(QUERY_TEXT)]
    Models_Data.Vector_Space_Model_Query_WORDS = []
    Models_Data.Vector_Space_Model_Query_NUMBER_OF_FILES = 1
    Models_Data.Vector_Space_Model_MATRIX = []
    TF_QUERY_COLUMNS_NAME = ["Term", "TF"]
    TF_QUERY_VALUES = []
    WTF_QUERY_COLUMNS_NAME = ["Term", "W-TF"]
    WTF_QUERY_VALUES = []
    DF_QUERY_COLUMNS_NAME = ["Term", "DF"]
    DF_QUERY_VALUES = []
    IDF_QUERY_COLUMNS_NAME = ["Term", "IDF"]
    IDF_QUERY_VALUES = []
    DF_AND_IDF_QUERY_COLUMNS_NAME = ["Term", "DF", "IDF"]
    DF_AND_IDF_QUERY_VALUES = []
    TF_IDF_QUERY_COLUMNS_NAME = ["Term", "TF-IDF"]
    TF_IDF_QUERY_VALUES = []
    LENGTH_QUERY_COLUMNS_NAME = ["#", "Length"]
    LENGTH_QUERY_VALUES = []
    NORMALIZED_TF_IDF_QUERY_COLUMNS_NAME = ["Term", "Normalized"]
    NORMALIZED_TF_IDF_QUERY_VALUES = []
    QUERY_TABLE_COLUMNS_NAME = [
        "Term",
        "tf-raw",
        "wtf(1 + log(tf))",
        "df",
        "idf",
        "tf*idf",
        "normalized",
    ]
    SIMILARITY_TABLE_COLUMNS_NAME = ["#", "Similarity"]
    SIMILARITY_VALUES = []
    MATCHED_DOCUMENTS = []


def preprocessing_query():
    clear_all_fields()
    text_file = Models_Data.Vector_Space_Model_Query_FILES_DATA
    text_file[0] = text_file[0].strip()
    text_file[0] = stemming_text(text_file[0])
    text_file_data = convert_list_to_string(text_file).split(" ")
    text_file_data = tokenization_and_stemming(text_file_data)
    Models_Data.Vector_Space_Model_Query_WORDS = text_file_data
    Models_Data.Vector_Space_Model_Query_WORDS = unsorted_distinct_list(
        Models_Data.Vector_Space_Model_Query_WORDS
    )
    Models_Data.Vector_Space_Model_Query_WORDS = sorted(
        Models_Data.Vector_Space_Model_Query_WORDS
    )


# create Term Frequency table
def create_tf_query_table():
    matrix = [TF_QUERY_COLUMNS_NAME]
    for word in Models_Data.Vector_Space_Model_Query_WORDS:
        row = [word]
        values = []
        value = stemming_text(QUERY_TEXT).count(word)
        row.append(str(value))
        values.append(value)
        matrix.append(row)
        TF_QUERY_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_query_table()  # remove comment in case you want show df table


# create Weighted Term Frequency Query table
def create_wtf_query_table():
    matrix = [WTF_QUERY_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_Query_WORDS):
        row = [word]
        values = []
        for y, text in enumerate(Models_Data.Vector_Space_Model_Query_FILES_DATA):
            value = TF_QUERY_VALUES[x][y]
            if value in [0, 1]:
                row.append(str(value))
                values.append(value)
            else:
                row.append(str(1 + math.log(value, 10)))
                values.append(value)
        matrix.append(row)
        WTF_QUERY_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_query_table()  # remove comment in case you want show df table


# create DF Query table
def create_df_query_table():
    global DF_QUERY_COLUMNS_NAME, DF_QUERY_COLUMNS
    DF_QUERY_COLUMNS_NAME = DF_COLUMNS_NAME
    query_text = stemming_text(QUERY_TEXT)
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        if word in query_text:
            DF_QUERY_VALUES.append(DF_VALUES[x][0])


# create IDF Query table
def create_idf_query_table():
    global IDF_QUERY_COLUMNS_NAME, IDF_QUERY_COLUMNS
    IDF_QUERY_COLUMNS_NAME = IDF_COLUMNS_NAME
    query_text = stemming_text(QUERY_TEXT)
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        if word in query_text:
            IDF_QUERY_VALUES.append(IDF_VALUES[x][0])


# create DF and IDF Frequency Query table
def create_df_and_idf_query_table():
    global DF_QUERY_COLUMNS_NAME, DF_QUERY_VALUES, IDF_QUERY_COLUMNS_NAME, IDF_QUERY_VALUES
    create_df_query_table()
    create_idf_query_table()
    matrix = [DF_AND_IDF_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_Query_WORDS):
        row = [word, str(DF_QUERY_VALUES[x]), str(IDF_QUERY_VALUES[x])]
        values = [DF_QUERY_VALUES[x], IDF_QUERY_VALUES[x]]
        matrix.append(row)
        DF_AND_IDF_QUERY_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_query_table()  # remove comment in case you want show df table


# create TF-IDF Query table
def create_tf_idf_query_table():
    matrix = [TF_IDF_QUERY_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_Query_WORDS):
        row = [word]
        values = []
        for y, text in enumerate(Models_Data.Vector_Space_Model_Query_FILES_DATA):
            value = WTF_QUERY_VALUES[x][y] * IDF_QUERY_VALUES[x]
            row.append(str(value))
            values.append(value)

        matrix.append(row)
        TF_IDF_QUERY_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_query_table()  # remove comment in case you want show df table


# create Document Query Length table
def create_query_length_table():
    matrix = [LENGTH_QUERY_COLUMNS_NAME]
    number_of_rows = len(TF_IDF_QUERY_VALUES)
    number_of_columns = len(TF_IDF_QUERY_VALUES[0])
    # Iterate over columns
    for col in range(number_of_columns):
        row_data = ["Query"]
        values = []
        sum_of_tf_idf_query_values = 0
        # Iterate over rows
        for row in range(number_of_rows):
            value = TF_IDF_QUERY_VALUES[row][col]
            sum_of_tf_idf_query_values += value * value

        sum_of_tf_idf_query_values = round(math.sqrt(sum_of_tf_idf_query_values), 9)
        row_data.append(str(sum_of_tf_idf_query_values))
        values.append(sum_of_tf_idf_query_values)
        matrix.append(row_data)
        LENGTH_QUERY_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix

    # show matrix using tree view
    show_matrix_query_table()  # remove comment in case you want show df table


# create Normalized TF-IDF Query table
def create_normalized_tf_idf_query_table():
    matrix = [NORMALIZED_TF_IDF_QUERY_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_Query_WORDS):
        row = [word]
        values = []
        for y, text in enumerate(Models_Data.Vector_Space_Model_Query_FILES_NAME):
            value = round(TF_IDF_QUERY_VALUES[x][y] / LENGTH_QUERY_VALUES[y][0], 9)
            row.append(str(value))
            values.append(value)

        matrix.append(row)
        NORMALIZED_TF_IDF_QUERY_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix

    # show matrix using tree view
    # show_matrix_query_table() # remove comment in case you want show df table


# Spliting Boolean Phrase Query
def spliting_boolean_phrase_query(query_text):
    return query_text.split('"')


# Solve Boolean Operation
def solver_boolean_operation(operands, operator):
    answer = []
    if operator == "not":
        answer = [
            value
            for value in Models_Data.Vector_Space_Model_FILES_NAME
            if value not in operands
        ]
    elif operator == "and":
        answer = list(set(operands[0]) & set(operands[1]))
    else:  # operator == "or"
        answer = list(set(operands[0]) | set(operands[1]))
    return sorted(answer, key=lambda x: str(x))


# Boolean Phrase Query Solution
def boolean_phrase_query_solver():
    global QUERY_TEXT, BOOLEAN_PHRASE_QUERY_TEXT
    BOOLEAN_PHRASE_QUERY_TEXT = QUERY_TEXT.strip()
    splited_text_list = spliting_boolean_phrase_query(BOOLEAN_PHRASE_QUERY_TEXT)
    splited_text_list = [text.strip() for text in splited_text_list if len(text) > 0]
    splited_text_list = stemming_list(splited_text_list)
    boolean_operators = ["and", "or", "not"]
    query_answers = []
    for text in splited_text_list:
        QUERY_TEXT = text
        print(f"text = {text}")
        if text in boolean_operators:
            query_answers.append(text)
            continue
        preprocessing_query()
        create_tf_query_table()
        create_wtf_query_table()
        create_df_and_idf_query_table()
        create_tf_idf_query_table()
        create_query_length_table()
        create_normalized_tf_idf_query_table()
        create_normalize_product_table()
        create_similarity_table()
        show_query_answer()
        # print(f"Phrase Query Answer Text = {PHRASE_QUERY_ANSWER_TEXT}")
        query_answers.append(PHRASE_QUERY_ANSWER_TEXT)
        # to prepare for the next value
        clear_all_fields()

    print(f"Query Answers: {query_answers}")
    i = 0
    temp_list = []
    # solve NOT Operations to prevent confusion when solving AND & OR operations
    while i < len(query_answers) and len(query_answers) > 1:
        temp_list.append(query_answers[i])
        if isinstance(query_answers[i], str) and query_answers[i] == "not":
            answer = solver_boolean_operation(query_answers[i + 1], query_answers[i])
            temp_list.pop()
            temp_list.append(answer)
            i += 1
        i += 1
    query_answers = temp_list
    print(f"query_answers = {query_answers}")

    i = 0
    temp_list = []
    # solve AND & OR operations
    while i < len(query_answers) and len(query_answers) > 1:
        temp_list.append(query_answers[i])
        if isinstance(query_answers[i], str):
            answer = solver_boolean_operation(
                [query_answers[i - 1], query_answers[i + 1]], query_answers[i]
            )
            temp_list.pop()
            temp_list.pop()
            temp_list.append(answer)
            i += 1
        i += 1
    query_answers = temp_list
    print(f"query_answers = {query_answers}")
    create_query_answer_textbox.delete("1.0", END)
    answer_text = f"The Order of Matched Documents:\n{query_answers}"
    create_query_answer_textbox.insert("1.0", answer_text)


# Create Query Properties table
def create_query_properties_table():
    global QUERY_TEXT
    QUERY_TEXT = create_query_textbox.get("1.0", "end-1c")
    if len(QUERY_TEXT) == 0:
        create_query_answer_textbox.insert("1.0", EMPTY_QUERY_ERROR_TEXT)
        return

    if '"' in QUERY_TEXT:
        boolean_phrase_query_solver()
        return

    preprocessing_query()
    create_tf_query_table()
    create_wtf_query_table()
    create_df_and_idf_query_table()
    create_tf_idf_query_table()
    create_query_length_table()
    create_normalized_tf_idf_query_table()
    matrix = [QUERY_TABLE_COLUMNS_NAME]
    for x, word in enumerate(Models_Data.Vector_Space_Model_Query_WORDS):
        row = [word]
        values = []
        row_data = [
            TF_QUERY_VALUES[x][0],
            WTF_QUERY_VALUES[x][0],
            DF_QUERY_VALUES[x],
            IDF_QUERY_VALUES[x],
            TF_IDF_QUERY_VALUES[x][0],
            NORMALIZED_TF_IDF_QUERY_VALUES[x][0],
        ]
        for y, value in enumerate(row_data):
            row.append(str(value))
            values.append(value)

        matrix.append(row)
        QUERY_TABLE_VALUES.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix
    # show matrix using tree view
    show_matrix_query_table()  # remove comment in case you want show df table


# Get Matched Documents with Query
def get_matched_documents(query_text):
    matched_documents = []
    for index, doc in enumerate(Models_Data.Vector_Space_Model_FILES_DATA):
        if query_text in doc[0]:
            matched_documents.append(Models_Data.Vector_Space_Model_FILES_NAME[index])
    return matched_documents


# Create Normalize Product Query table
def create_normalize_product_table():
    global SIMILARITY_VALUES, MATCHED_DOCUMENTS
    query_text = Models_Data.Vector_Space_Model_Query_FILES_DATA[0]
    matched_documents = get_matched_documents(query_text)
    MATCHED_DOCUMENTS = matched_documents
    matrix = [["Term"] + matched_documents]
    sum = [0.0 for i in matched_documents]
    current_element = 0
    for x, word in enumerate(Models_Data.Vector_Space_Model_WORDS):
        if word in Models_Data.Vector_Space_Model_Query_WORDS:
            row = [word]
            values = []
            current_column = 0
            for y, name in enumerate(Models_Data.Vector_Space_Model_FILES_NAME):
                if name in matched_documents:
                    normalized_term_value = NORMALIZED_TF_IDF_VALUES[x][y]
                    # print(f"current column = {current_column}")
                    value = round(
                        normalized_term_value
                        * NORMALIZED_TF_IDF_QUERY_VALUES[current_element][0],
                        9,
                    )
                    temp = sum[current_column] + value
                    sum[current_column] = round(temp, 9)
                    row.append(str(value))
                    values.append(value)
                    current_column += 1
            current_element += 1
            matrix.append(row)
            QUERY_TABLE_VALUES.append(values)
            print(f"row = {row}")
    QUERY_TABLE_VALUES.append(sum)
    sum = [str(x) for x in sum]
    SIMILARITY_VALUES = sum
    matrix.append(["Sum"] + sum)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix
    print(matrix)
    # show matrix using tree view
    show_matrix_query_table()  # remove comment in case you want show df table


# Create Similarity table
def create_similarity_table():
    matrix = [SIMILARITY_TABLE_COLUMNS_NAME]
    for i, value in enumerate(MATCHED_DOCUMENTS):
        values = [MATCHED_DOCUMENTS[i], SIMILARITY_VALUES[i]]
        matrix.append(values)
    Models_Data.Vector_Space_Model_Query_MATRIX = matrix
    # show matrix using tree view
    show_matrix_query_table()  # remove comment in case you want show df table


# Query Answer
def show_query_answer():
    global PHRASE_QUERY_ANSWER_TEXT
    sorted_matrix = sorted(
        Models_Data.Vector_Space_Model_Query_MATRIX[1:],
        key=lambda x: x[1],
        reverse=True,
    )
    sorted_matched_documents = [value[0] for value in sorted_matrix]
    PHRASE_QUERY_ANSWER_TEXT = sorted_matched_documents
    documents = ""
    for doc in sorted_matched_documents:
        documents += str(doc) + "\n"
    answer_text = f"The Order of Matched Documents:\n{documents}"
    create_query_answer_textbox.insert("1.0", answer_text)


# Clear query
def clear_query():
    create_query_textbox.delete("1.0", END)
    create_query_answer_textbox.delete("1.0", END)


#################################################################################
#################################################################################
#################################################################################
#################################################################################
#################################################################################

# Components
# Title
vector_space_title_config = {
    "label_size": "28",
    "label_text": "Vector Space Model",
    "label_background_color": TITLE_BACKGROUND_COLOR,
    "label_foreground_color": TITLE_FOREGROUND_COLOR,
}
vector_space_title = create_label(vector_space_title_config)

# Document Page
vector_space_document_page_config = {
    "label_size": "20",
    "label_text": "~~Document~~",
    "label_background_color": TITLE_BACKGROUND_COLOR,
    "label_foreground_color": TITLE_FOREGROUND_COLOR,
}
vector_space_document_page = create_label(vector_space_document_page_config)

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
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
add_new_document_button = create_button(add_new_document_button_config)

# Create Term Frequency Table Label
tf_table_label_config = {
    "label_size": "15",
    "label_text": "Term Frequency:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
tf_table_label = create_label(tf_table_label_config)

# Create Term Frequency button
tf_table_button_config = {
    "button_size": "15",
    "button_text": "Create TF Table",
    "function_name": create_tf_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
tf_table_button = create_button(tf_table_button_config)

# Create Weighted Term Frequency Table Label
wtf_table_label_config = {
    "label_size": "15",
    "label_text": "Weighted Term Frequency:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
wtf_table_label = create_label(wtf_table_label_config)

# Create Weighted Term Frequency button
wtf_table_button_config = {
    "button_size": "15",
    "button_text": "Create W-TF Table",
    "function_name": create_wtf_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
wtf_table_button = create_button(wtf_table_button_config)

# Create Document Frequency and Inverse Document Frequency Table Label
df_and_idf_table_label_config = {
    "label_size": "15",
    "label_text": "DF_and_IDF Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
df_and_idf_table_label = create_label(df_and_idf_table_label_config)

# Create Document Frequency and Inverse Document Frequency button
df_and_idf_table_button_config = {
    "button_size": "15",
    "button_text": "Create DF_and_IDF Table",
    "function_name": create_df_and_idf_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
df_and_idf_table_button = create_button(df_and_idf_table_button_config)

# Create Document Frequency and Inverse Document Frequency Table Label
tf_idf_table_label_config = {
    "label_size": "15",
    "label_text": "TF-IDF Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
tf_idf_table_label = create_label(tf_idf_table_label_config)

# Create Document Frequency and Inverse Document Frequency button
tf_idf_table_button_config = {
    "button_size": "15",
    "button_text": "Create TF_IDF Table",
    "function_name": create_tf_idf_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
tf_idf_table_button = create_button(tf_idf_table_button_config)

# Create Length Table Label
length_table_label_config = {
    "label_size": "15",
    "label_text": "Length Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
length_table_label = create_label(length_table_label_config)

# Create Length button
length_table_button_config = {
    "button_size": "15",
    "button_text": "Create Length Table",
    "function_name": create_length_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
length_table_button = create_button(length_table_button_config)

# Create Length Table Label
normalized_tf_idf_table_label_config = {
    "label_size": "15",
    "label_text": "Normalized TF-IDF Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
normalized_tf_idf_table_label = create_label(normalized_tf_idf_table_label_config)

# Create Length button
normalized_tf_idf_table_button_config = {
    "button_size": "15",
    "button_text": "Create Normalized TF-IDF Table",
    "function_name": create_normalized_tf_idf_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
normalized_tf_idf_table_button = create_button(normalized_tf_idf_table_button_config)

# Create Main Menu Button

create_main_menu_button_config = {
    "button_size": "18",
    "button_text": "Main Menu",
    "function_name": return_to_main_menu,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
create_main_menu_button = create_button(create_main_menu_button_config)

# Create Next Button

create_next_button_config = {
    "button_size": "18",
    "button_text": "Query Page",
    "function_name": query_page_button,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
create_next_button = create_button(create_next_button_config)

############################################################################
############################################################################
############################################################################
############################################################################

# Second Page in Vector Space Model

# Query Page
vector_space_query_page_label_config = {
    "label_size": "20",
    "label_text": "~~Query~~",
    "label_background_color": TITLE_BACKGROUND_COLOR,
    "label_foreground_color": TITLE_FOREGROUND_COLOR,
}
vector_space_query_page_label = create_label(vector_space_query_page_label_config)

# Create Query Label
create_query_label_config = {
    "label_size": "15",
    "label_text": "Enter Phrase Query:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_query_label = create_label(create_query_label_config)

# Create Query Textbox
create_query_textbox_config = {
    "textbox_size": "20",
    "height": 1,
    "width": 22,
    "textbox_background_color": LABEL_BACKGROUND_COLOR,
    "textbox_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_query_textbox = create_textbox(create_query_textbox_config)

# Create Query Properties Table Label
query_properties_table_label_config = {
    "label_size": "15",
    "label_text": "Query Properties Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
query_properties_table_label = create_label(query_properties_table_label_config)

# Create Length button
query_properties_table_button_config = {
    "button_size": "15",
    "button_text": "Create query Properties Table",
    "function_name": create_query_properties_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
query_properties_table_button = create_button(query_properties_table_button_config)

# Create Normalize Product Table Label
normalize_product_table_label_config = {
    "label_size": "15",
    "label_text": "Normalize Product Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
normalize_product_table_label = create_label(normalize_product_table_label_config)

# Create Normalize Product Table button
normalize_product_table_button_config = {
    "button_size": "15",
    "button_text": "Create Normalize Product Table",
    "function_name": create_normalize_product_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
normalize_product_table_button = create_button(normalize_product_table_button_config)

# Create Similarity Table Label
similarity_table_label_config = {
    "label_size": "15",
    "label_text": "Similarity Table:",
    "label_background_color": LABEL_BACKGROUND_COLOR,
    "label_foreground_color": LABEL_FOREGROUND_COLOR,
}
similarity_table_label = create_label(similarity_table_label_config)

# Create Similarity Table button
similarity_table_button_config = {
    "button_size": "15",
    "button_text": "Create Similarity Table",
    "function_name": create_similarity_table,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
similarity_table_button = create_button(similarity_table_button_config)

# Create Show Query Answer Button
create_show_query_answer_button_config = {
    "button_size": "15",
    "button_text": "Show Query Answer",
    "function_name": show_query_answer,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
create_show_query_answer_button = create_button(create_show_query_answer_button_config)

# Create Clear Query textbox Button
create_clear_query_textbox_button_config = {
    "button_size": "15",
    "button_text": "Clear Query",
    "function_name": clear_query,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
create_clear_query_textbox_button = create_button(
    create_clear_query_textbox_button_config
)

# Create Query Answer Textbox
create_query_answer_textbox_config = {
    "textbox_size": "20",
    "height": 3,
    "width": 30,
    "textbox_background_color": LABEL_BACKGROUND_COLOR,
    "textbox_foreground_color": LABEL_FOREGROUND_COLOR,
}
create_query_answer_textbox = create_textbox(create_query_answer_textbox_config)

# Create Document Page Button
create_document_button_config = {
    "button_size": "18",
    "button_text": "Document Page",
    "function_name": document_page_button,
    "button_background_color": Buttons_Color.VECTOR_SPACE_BUTTON_BACKGROUND_COLOR,
    "button_foreground_color": Buttons_Color.VECTOR_SPACE_BUTTON_FOREGROUND_COLOR,
}
create_document_button = create_button(create_document_button_config)

############################################################################
############################################################################


Models_Data.Vector_Space_Model_Components = [
    {"name": vector_space_title, "PosX": 130, "PosY": 30},
    {"name": vector_space_document_page, "PosX": 200, "PosY": 100},
    {"name": add_new_document_label, "PosX": 125, "PosY": 165},
    {"name": add_new_document_button, "PosX": 280, "PosY": 160},
    {"name": tf_table_label, "PosX": 110, "PosY": 225},
    {"name": tf_table_button, "PosX": 280, "PosY": 220},
    {"name": wtf_table_label, "PosX": 20, "PosY": 285},
    {"name": wtf_table_button, "PosX": 280, "PosY": 280},
    {"name": df_and_idf_table_label, "PosX": 85, "PosY": 345},
    {"name": df_and_idf_table_button, "PosX": 280, "PosY": 340},
    {"name": tf_idf_table_label, "PosX": 135, "PosY": 405},
    {"name": tf_idf_table_button, "PosX": 280, "PosY": 400},
    {"name": length_table_label, "PosX": 140, "PosY": 465},
    {"name": length_table_button, "PosX": 280, "PosY": 460},
    {"name": normalized_tf_idf_table_label, "PosX": 33, "PosY": 525},
    {"name": normalized_tf_idf_table_button, "PosX": 280, "PosY": 520},
    {"name": create_main_menu_button, "PosX": 80, "PosY": 580},
    {"name": create_next_button, "PosX": 400, "PosY": 580},
]

Query_Page_Components = [
    {"name": vector_space_title, "PosX": 130, "PosY": 30},
    {"name": vector_space_query_page_label, "PosX": 230, "PosY": 100},
    {"name": create_query_label, "PosX": 40, "PosY": 160},
    {"name": create_query_textbox, "PosX": 245, "PosY": 155},
    {"name": query_properties_table_label, "PosX": 40, "PosY": 220},
    {"name": query_properties_table_button, "PosX": 280, "PosY": 215},
    {"name": normalize_product_table_label, "PosX": 40, "PosY": 280},
    {"name": normalize_product_table_button, "PosX": 280, "PosY": 275},
    {"name": similarity_table_label, "PosX": 40, "PosY": 340},
    {"name": similarity_table_button, "PosX": 280, "PosY": 335},
    {"name": create_show_query_answer_button, "PosX": 140, "PosY": 400},
    {"name": create_clear_query_textbox_button, "PosX": 360, "PosY": 400},
    {"name": create_query_answer_textbox, "PosX": 80, "PosY": 460},
    {"name": create_document_button, "PosX": 220, "PosY": 580},
]
