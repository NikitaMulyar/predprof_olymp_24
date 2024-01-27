import csv
import os
import random


def check_buy(A, i, BUY_FOR_PROJECT=[], BUY=[], SELL=[], up=0, budget=0):
    purch = False
    soll = False
    for j in BUY:  # для каждой купленной акции определяем, какой процент прибыли/убыли она несет к текущему дню
        j[3] = ((A[i - 1][3] + A[i - 1][4]) / 2) / j[0] * 100 - 100
        if j[3] >= 5 or j[3] <= -5:
            SELL.append([A[i][1], A[i][0], j[2]])  # если прибыль/убыль больше 5%, продаем
            # print(1)
    min_a = min(A[i - 2][1], A[i - 2][2])
    max_a = max(A[i - 2][1], A[i - 2][2])
    min_b = min(A[i - 1][1], A[i - 1][2])
    max_b = max(A[i - 1][1], A[i - 1][2])
    absort = False
    if (min_b < min_a) and (max_b > max_a):  # проверка на то, что вчера произошло поглощение
        absort = True
    if absort:
        if (A[i - 2][2] < A[i - 2][1]) and (
                A[i - 1][2] > A[i - 1][1]):  # черная свеча поглощена белой. Следовательно, сегодня покупаем
            d = int(1 + (max_b - min_b) / (max_a - min_a))
            BUY_FOR_PROJECT.append([A[i][1], A[i][0], d, 0])
            BUY.append([A[i][1], A[i][0], d, 0])  # цена покупки, дата покупки, объем, процент прибыли/убыли
            up -= A[i][1] * d
            budget += A[i][1] * d
            purch = True
        elif (A[i - 2][1] < A[i - 2][2]) and (A[i - 1][1] > A[i - 1][2]):  # белая свеча поглощена черной
            value_to_sell = 0
            soll = True
            for j in BUY:
                if j[3] > 0:
                    up += A[i][1] * j[2]
                    value_to_sell += j[2]
                    BUY.remove(j)
            if value_to_sell != 0:
                SELL.append([A[i][1], A[i][0], value_to_sell])  # цена продажи, дата продажи, объем
            if (i > 5) and (A[i - 5][2] > (A[i - 1][1] + A[i - 1][2]) / 2) and (
                    abs(A[i - 1][1] - A[i - 1][2]) * 4 < A[i - 1][4] - A[i - 1][3]):
                d = (A[i - 1][4] - A[i - 1][3]) / (abs(A[i - 1][1] - A[i - 1][2]))
                BUY.append([A[i][1], A[i][0], d, 0])  # молот
                BUY_FOR_PROJECT.append([A[i][1], A[i][0], d, 0])
                purch = True
                up -= A[i][1] * d
                budget += A[i][1] * d
    return [up, budget, purch, soll]


def absorption(sze, cmp):
    st = "../csv_files/" + cmp + ".csv"
    file = open(st, encoding="utf8", mode='r')
    file1 = open(st, encoding="utf8", mode='r')
    l = len(file1.readlines())
    file1.close()
    reader = csv.reader(file, delimiter=",", quotechar='"')
    next(reader)
    A = []
    for i, line in enumerate(reader):
        if i >= l - sze - 1:
            A.append(line)  # распаковка
            for j in range(len(A[-1])):
                if j != 0:  # перевод во float цен
                    A[-1][j] = float(A[-1][j])
    a = check_buy(A, len(A) - 1)
    purch = a[2]
    soll = a[3]
    if purch:
        return 1  # покупать
    elif soll:
        return -1  # продавать
    else:
        return 0  # не трогать


def forecast(sze, cmp):
    st = "../csv_files/" + cmp + ".csv"
    file = open(st, encoding="utf8", mode='r')
    file1 = open(st, encoding="utf8", mode='r')
    l = len(file1.readlines())
    file1.close()
    reader = csv.reader(file, delimiter=",", quotechar='"')
    next(reader)
    A = []
    for i, line in enumerate(reader):
        if i >= l - sze - 1:
            A.append(line)  # распаковка
            for j in range(len(A[-1])):
                if j != 0:  # перевод во float цен
                    A[-1][j] = float(A[-1][j])
    BUY = []
    BUY_FOR_PROJECT = []  # итоговые покупки в формате: цена покупки, дата покупки, объем, процент убыли/прибыли
    SELL = []  # тоже, что BUY_FOR_PROJECT только с продажами в формате: цена, дата, объем
    up = 0
    budget = 0
    for i in range(2, len(A)):
        a = check_buy(A, BUY_FOR_PROJECT, BUY, SELL, i, up, budget)
        up = a[0]
        budget = a[1]
        purch = a[2]
        soll = a[3]
        print(purch, soll)
        print(A[i])
        print(A[i][3])
        # print("SELL")
        # print(*SELL, sep='\n')
        print("BUY")
        print(*BUY, sep='\n')
        # print("BUY_FOR_PROJECT")
        # print(*BUY_FOR_PROJECT, sep='\n')
        print()
    up1 = up
    for it in BUY:
        up1 += it[0] * it[2]
    print("доход:", up)  # вывод дохода
    print("теоритеческий доход:", up1)  # вывод дохода
    print("бюджет:", budget)  # вывод бюджета
    file.close()


if __name__ == '__main__':
    print(absorption(500, "AAPL"))
