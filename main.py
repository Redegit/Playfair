from datetime import time
from time import sleep
from timeit import timeit

import numpy as np


class Playfair:
    alphabet = [chr(i) for i in range(1040, 1072)]

    @staticmethod
    def find_indexes(s: str, matrix: np.array):
        i1, i2 = None, None
        for i in range(4):
            for j in range(8):
                if matrix[i][j] == s[0]:
                    i1 = (i, j)
                if matrix[i][j] == s[1]:
                    i2 = (i, j)
        return i1, i2

    @staticmethod
    def make_matrix(key: str):
        unique_key = list(map(lambda x: x.upper(), list(dict.fromkeys(key))))

        alpha_without_key = [item for item in Playfair.alphabet if item not in frozenset(unique_key)]

        matrix_data = unique_key + alpha_without_key

        matrix = np.array(matrix_data)
        matrix.shape = (4, 8)
        return matrix

    @staticmethod
    def encrypt(string: str, key: str):

        matrix = Playfair.make_matrix(key)

        # print(matrix)

        str_list = list(string.upper().replace(" ", ""))

        # print(len(str_list))
        # print(str_list)

        bigramm_list = []

        while True:
            if len(str_list) > 1:
                l1, l2 = str_list.pop(0), str_list.pop(0)
                if l1 == l2:
                    bigramm_list.append(l1 + "Ъ")
                    str_list.insert(0, l2)
                else:
                    bigramm_list.append(l1 + l2)
            elif len(str_list) == 1:
                l1, l2 = str_list.pop(0), "Ъ"
                bigramm_list.append(l1 + l2)
            else:
                break
        # print(bigramm_list)

        result_str = ""

        for big in bigramm_list:
            i1, i2 = Playfair.find_indexes(big, matrix)

            if i1[0] == i2[0]:
                l1 = matrix[i1[0]][(i1[1] + 1) % 8]
                l2 = matrix[i2[0]][(i2[1] + 1) % 8]
            elif i1[1] == i2[1]:
                l1 = matrix[(i1[0] + 1) % 4][i1[1]]
                l2 = matrix[(i2[0] + 1) % 4][i2[1]]
            else:
                l1 = matrix[i2[0]][i1[1]]
                l2 = matrix[i1[0]][i2[1]]
            result_str += l1 + l2

        return result_str

    @staticmethod
    def decrypt(s: str, key: str):

        matrix = Playfair.make_matrix(key)
        print(matrix)
        bigramm_list = [s[i] + s[i + 1] for i in range(0, len(s), 2)]

        print(s)
        print(bigramm_list)

        result_str = ""

        for big in bigramm_list:
            i1, i2 = Playfair.find_indexes(big, matrix)

            if i1[0] == i2[0]:
                l1 = matrix[i1[0]][(i1[1] - 1)]
                l2 = matrix[i2[0]][(i2[1] - 1)]
            elif i1[1] == i2[1]:
                l1 = matrix[(i1[0] - 1)][i1[1]]
                l2 = matrix[(i2[0] - 1)][i2[1]]
            else:
                l1 = matrix[i2[0]][i1[1]]
                l2 = matrix[i1[0]][i2[1]]

            if l2 == "Ъйсц":
                result_str += l1
            else:
                result_str += l1 + l2

        return result_str


if __name__ == '__main__':
    # s = input()
    s = "Простой текст для примера ооо абя"
    print(f"text = {s}")

    keyword = "Криптография"
    print(f"{keyword = }")

    encrypted_text = Playfair.encrypt(s, keyword)
    print(f"{encrypted_text = }")

    decrypted_text = Playfair.decrypt(encrypted_text, keyword)
    print(f"{decrypted_text = }")
