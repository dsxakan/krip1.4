import itertools
from collections import Counter

# Функция шифрования, использующая сложение по модулю 3
def encrypt(key, plaintext):
    return (plaintext + key) % 3

# Функция для атаки на основе предполагаемого сильно вероятного текста
def attack(ciphertext, encryption_table, X, K):
    # Распределение вероятностей шифротекстов P(Y)
    p_y = Counter(ciphertext)

    # Распределение условных вероятностей шифротекстов P(Y|X)
    p_y_given_x = {}
    for x in X:
        p_y_given_x[x] = Counter([encryption_table[x][k] for k in K])

    # Распределение условных вероятностей открытых текстов P(X|Y)
    p_x_given_y = {}
    for y in set(ciphertext):
        p_x_given_y[y] = Counter([x for x in X if encryption_table[x][K[ciphertext.index(y)]] == y])

    # Вывод распределений
    print("Probability Distribution P(Y):", p_y)
    print("\nConditional Probability Distribution P(Y|X):", p_y_given_x)
    print("\nConditional Probability Distribution P(X|Y):", p_x_given_y)

    # Попытка восстановления открытого текста
    most_probable_x = None
    max_probability = 0
    for x in X:
        probability = p_x_given_y[ciphertext[0]][x] * p_y[x]
        if probability > max_probability:
            most_probable_x = x
            max_probability = probability

    print("\nMost Probable Original Message:", most_probable_x)

# Если скрипт выполняется как основная программа
if __name__ == "__main__":
    X = [0, 1, 2]
    K = [0, 1, 2]

    # Создание таблицы шифрования
    encryption_table = {}
    for x, k in itertools.product(X, K):
        y = encrypt(k, x)
        if x not in encryption_table:
            encryption_table[x] = {}
        encryption_table[x][k] = y

    # Вывод таблицы шифрования
    print("Encryption Table:")
    print("X/K |", end="")
    for k in K:
        print(f"  {k}  |", end="")
    print("\n" + "-" * 31)
    for x in X:
        print(f"  {x}  |", end="")
        for k in K:
            print(f"  {encryption_table[x][k]}  |", end="")
        print("\n" + "-" * 31)

    # Проведение атаки
    plaintext = 1  # Предполагаемый сильно вероятный текст
    ciphertext = [encrypt(k, plaintext) for k in K]

    print("\nCiphertexts:", ciphertext)

    # Запуск атаки
    attack(ciphertext, encryption_table, X, K)
