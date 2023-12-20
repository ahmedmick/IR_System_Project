import os
def open_text_file(text_file_path):
    try:
        with open(text_file_path, "r") as txt_file:
            return txt_file.readlines()
    except:
        raise FileExistsError


def convert_list_to_string(data_list):
    return "".join(data_list)


def get_file_name(file_path):
    # partition -> split string to 3 parts -> (filename, '.' , file_extension)
    return os.path.basename(file_path).partition(".")[0]


def unsorted_distinct_list(seq):
    distinct_list = set()
    distinct_list_add_element = distinct_list.add
    return [element for element in seq if not (element in distinct_list or distinct_list_add_element(element))]