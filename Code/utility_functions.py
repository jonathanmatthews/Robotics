def flatten(values):
    final_list = []
    for list_value in values:
        if type(list_value) == list:
            [final_list.append(value) for value in list_value]
        else:
            final_list.append(list_value)
    return final_list