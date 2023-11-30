from typing import Union, List, Tuple


def create_bool_list(enabled: Union[List, Tuple], list_length: int):
    result = []
    for i in range(list_length):
        value = i in enabled
        result.append(value)
    return result
