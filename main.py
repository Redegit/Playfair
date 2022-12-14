import numpy as np


class Playfair:
    """Класс для кодирования/декодирования при помощи шифра Плейфера"""

    alphabet = [chr(i) for i in range(1040, 1072)]

    @staticmethod
    def find_indexes(bigram: str, matrix: np.array) -> tuple:
        """Поиск индексов элементов биграммы в матрице"""
        i1, i2 = None, None
        for i in range(4):
            for j in range(8):
                if matrix[i][j] == bigram[0]:
                    i1 = (i, j)
                if matrix[i][j] == bigram[1]:
                    i2 = (i, j)

        return i1, i2

    @staticmethod
    def make_matrix(key: str) -> np.array:
        """Создание матрицы шифра на основе ключевого слова и русского алфавита"""

        # Удаление повторов букв из ключа
        unique_key = list(map(lambda x: x.upper(), list(dict.fromkeys(key))))

        # Вычитание ключа из алфавита
        alpha_without_key = [item for item in Playfair.alphabet if item not in frozenset(unique_key)]

        # Получение данных для матрицы (сложение ключа и оставшейся части алфавита)
        matrix_data = unique_key + alpha_without_key

        # Создание матрицы
        matrix = np.array(matrix_data)
        matrix.shape = (4, 8)

        return matrix

    @staticmethod
    def encrypt(message: str, key: str) -> str:
        """Шифрование переданной строки с использованием ключа"""

        # Создание матрицы
        matrix = Playfair.make_matrix(key)

        # Удаление всех символов, не встречающихся в алфавите
        message = message.upper()
        str_list = list(s for s in message if s in Playfair.alphabet)

        # Получение биграмм со всавкой "Ъ" между повторяющимися буквами и в конце сообщения, если число букв нечетное
        bigram_list = []
        while True:
            if len(str_list) > 1:
                l1, l2 = str_list.pop(0), str_list.pop(0)
                if l1 == l2:
                    bigram_list.append(l1 + "Ъ")
                    str_list.insert(0, l2)
                else:
                    bigram_list.append(l1 + l2)
            elif len(str_list) == 1:
                l1, l2 = str_list.pop(0), "Ъ"
                bigram_list.append(l1 + l2)
            else:
                break

        # print(matrix)
        # print(bigram_list)

        # Шифрование сообщения при помощи матрицы
        result_str = ""
        for big in bigram_list:
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
    def decrypt(message: str, key: str) -> str:
        """Дешифрование строки, зашифрованной шифром Плейфера"""

        # Создание матрицы
        matrix = Playfair.make_matrix(key)

        # Получение биграмм
        message = message.upper()
        bigram_list = [message[i] + message[i + 1] for i in range(0, len(message), 2)]

        # print(matrix)
        # print(bigram_list)

        # Дешифровка биграмм при помощи матрицы
        result_str = ""
        for big in bigram_list:
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

            result_str += l1 + l2

        # Удаление лишних "Ъ", если таки есть
        result = ""
        i = 0
        while i < len(result_str) - 2:
            result += result_str[i]
            if (result_str[i + 1] == "Ъ") and (result_str[i] == result_str[i + 2]):
                i += 1
            i += 1

        result += result_str[i:] if result_str[-1] != "Ъ" else result_str[i:-1]

        return result


if __name__ == '__main__':
    # s = input()
    s = "Простой текст для примера ооо qqq"
    print(f"text = {s}")

    keyword = "Криптография"
    print(f"{keyword = }")

    encrypted_text = Playfair.encrypt(s, keyword)
    print(f"{encrypted_text = }")

    decrypted_text = Playfair.decrypt(encrypted_text, keyword)
    print(f"{decrypted_text = }")
