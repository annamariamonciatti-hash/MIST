import random

import itertools

OPS = ["+", "-", "*", "/"]


def clean_div(max_res=9):
    """Restituisce a, b tali che a/b = risultato intero"""
    res = random.randint(1, max_res)
    b = random.randint(1, 9)
    a = res * b
    return a, b, res


import random


def generate_equation(diff):

    mapping = {
        "easy1": ([9, 9], ["+", "-"]),
        "easy2": ([9, 9, 9], ["+", "-"]),
        "med1": ([9, 9, 9, 9], ["+", "-", "*"]),
        "med2": ([9, 9, 99, 99], ["*", "-"]),
        "hard": ([99, 99, 99, 99], ["+", "-", "*", "/"]),
    }

    ints, ops_pool = mapping.get(diff, ([9, 9], ["+"]))

    while True:  # 👈 LOOP DI SICUREZZA

        # numeri
        numbers = [random.randint(1, max_val) for max_val in ints]

        # operatori
        ops = [random.choice(ops_pool) for _ in range(len(numbers) - 1)]

        # costruzione espressione
        expr = str(numbers[0])
        for i in range(len(ops)):
            expr += f" {ops[i]} {numbers[i+1]}"

        # calcolo
        try:
            result = eval(expr)
        except ZeroDivisionError:
            continue

        # 🔴 FILTRI IMPORTANTI
        if not isinstance(result, (int, float)):
            continue

        if result != int(result):  # evita float tipo 2.5
            continue

        result = int(result)

        if 0 <= result <= 9:
            return expr + " = ?", result


def update_difficulty(level, cor, err, stress=False):

    upN, downN = (2, 4) if stress else (5, 5)

    if cor >= upN and level < 4:
        level, cor, err = level + 1, 0, 0
    elif err >= downN and level > 0:
        level, cor, err = level - 1, 0, 0

    levels = ["easy1", "easy2", "med1", "med2", "hard"]
    return levels[level], level, cor, err
