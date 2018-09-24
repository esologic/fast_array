from multiprocessing import Value, Array, Lock
from ctypes import c_int


def buffer_insert(lock, count_index, data_index, count_array, data_array, input_values):

    with lock:

        if count_index.value < len(count_array):

            count_array[count_index.value] = len(input_values)
            count_index.value += 1

            for index, value in enumerate(input_values):
                data_array[data_index.value + index] = value
            data_index.value += len(input_values)

        else:
            raise IndexError("Buffer is full, can't add data")


def buffer_extract(lock, count_index, data_index, count_array, data_array):

    with lock:

        if count_index.value > 0:

            number_of_bytes = count_array[0]
            output_bytes = data_array[0:number_of_bytes]

            other_bytes = data_array[number_of_bytes:data_index.value]

            shifted_location = 0
            for b in other_bytes:
                data_array[shifted_location] = b
                shifted_location += 1

            data_index.value -= number_of_bytes

            for i in range(0, len(count_array)):
                try:
                    count_array[i] = count_array[i + 1]
                except IndexError:
                    break

            count_index.value -= 1
        else:
            raise IndexError("Buffer is empty, can't extract data")

        return output_bytes


class FastArrayDataStructures(object):

    def __init__(self, number_of_positions, data_array_c_type, max_data_array_objects):

        self.lock = Lock()
        self.count_index = Value(c_int, 0)
        self.data_index = Value(c_int, 0)
        self.count_array = Array(c_int, number_of_positions)
        self.data_array = Array(data_array_c_type, number_of_positions * max_data_array_objects)
