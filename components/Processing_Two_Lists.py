import Models_Data


def process_two_lists(required_file, files_name, files_data, first_list, second_list):
    answer_list = []
    required_file_data = ""
    for pos, value in enumerate(files_name):
        if required_file == value:
            required_file_data = files_data[pos][0]
            break

    print(f"second_list = {second_list}")
    for pos, value in enumerate(first_list):
        if value == "-1":
            answer_list.append(value)
            continue
        required_position = int(first_list[pos])
        while required_position < len(required_file_data) and \
        required_file_data[required_position] != " ":
            required_position += 1
        
        print(f"required_position = {required_position}")
        if required_position + 1 < len(required_file_data) and \
        str(required_position + 1) in second_list:
            answer_list.append(str(required_position + 1))
        else:
            answer_list.append("-1")   

    return answer_list
