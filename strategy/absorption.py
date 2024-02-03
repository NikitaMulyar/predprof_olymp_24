import csv
import os
import random

def check_buy(A, i, BUY_FOR_PROJECT, BUY, SELL, up=0, budget=0):
    cf = 1
    for j in BUY:  # для каждой купленной акции определяем, какой процент прибыли/убыли она несет к утру сегодняшнего дня
        j[3] = A[i][1] / j[0] * 100 - 100
    for j in BUY:
        if j[3] > 7 or j[3] < -5:
            SELL.append([A[i][1], j[1], j[2]])
            up += A[i][1] * j[2]
            BUY.remove(j)
    min_a = min(A[i - 2][1], A[i - 2][2])
    max_a = max(A[i - 2][1], A[i - 2][2])
    min_b = min(A[i - 1][1], A[i - 1][2])
    max_b = max(A[i - 1][1], A[i - 1][2])
    absort = False
    if (min_b < min_a) and (max_b > max_a): # проверка на то, что вчера произошло поглощение
        absort = True
    if absort:
        if (A[i - 5][3] + A[i - 5][4]) / 2 > (A[i - 1][3] + A[i - 1][4]) / 2:  # тренд нисходящий
            if max_a - min_a == 0: d = 5
            else: d = int(1 + (max_b - min_b) / (max_a - min_a))
            d *= cf
            BUY_FOR_PROJECT.append([A[i][1], A[i][0], d, 0])
            BUY.append([A[i][1], A[i][0], d, 0])  # цена покупки, дата покупки, объем, процент прибыли/убыли
            up -= A[i][1] * d
            budget += A[i][1] * d
        else:  # тренд восходящий
            value_to_sell = 0
            for j in BUY:
                if j[3] > 0:
                    up += A[i][1] * j[2]
                    value_to_sell += j[2]
                    BUY.remove(j)
            if value_to_sell != 0:
                SELL.append([A[i][1], A[i][0], value_to_sell])  # цена продажи, дата продажи, объем
    elif (i > 5) and (abs(A[i - 1][1] - A[i - 1][2]) * 10 < min(A[i - 1][1], A[i - 1][2]) - A[i - 1][4]) and (A[i - 5][2] > (A[i - 1][1] + A[i - 1][2]) / 2):
        if abs(A[i - 1][1] - A[i - 1][2]) == 0: d = 5
        else: d = round((min(A[i - 1][1], A[i - 1][2]) - A[i - 1][4]) / (abs(A[i - 1][1] - A[i - 1][2])))
        d *= cf
        BUY.append([A[i][1], A[i][0], d, 0])  # молот
        BUY_FOR_PROJECT.append([A[i][1], A[i][0], d, 0])
        up -= A[i][1] * d
        budget += A[i][1] * d
    return up, budget


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
    SELL = []  # то же, что BUY_FOR_PROJECT только с продажами в формате: цена, дата, объем
    up = 0
    budget = 0
    for i in range(6, len(A)):
        # print(BUY)
        up, budget = check_buy(A, i, BUY_FOR_PROJECT, BUY, SELL, up, budget)
        # print(BUY)
    up1 = up
    for it in BUY:
        up1 += it[0] * it[2]
    # print("BUY_FOR_PROJECT")
    # print(*SELL, sep='\n')
    # print('!', sep ='\n ')
    # print(*BUY_FOR_PROJECT, sep='\n')
    print("доход:", up)  # вывод дохода
    print("теоритический доход:", up1)  # вывод дохода
    print("доход в процентах: ", round(100 * (up1/budget), 3), "%", sep='')
    print("бюджет:", budget)  # вывод бюджета
    file.close()


if __name__ == '__main__':
    cmp = "AAPL"
    print("компания:", cmp)
    forecast(100, cmp)
    # print(*absorption(cmp))
