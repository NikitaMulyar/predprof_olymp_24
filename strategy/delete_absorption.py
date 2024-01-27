import csv
import os
import random

def absorption(size):
    file = open("../csv_files/SBER.csv", encoding="utf8")
    reader = csv.reader(file, delimiter=";", quotechar='"')
    A = [[] for _ in range(size)]
    i = 0
    for line in reader:
        print(line)
        if i != 0:
            A[i - 1] = str(*line).split(',')  # распаковка
            for j in range(len(A[i - 1])):
                if j != 0: # перевод во float цен
                    A[i - 1][j] = float(A[i - 1][j])
        i += 1
        if (i > size):
            break
    BUY = []
    BUY_FOR_PROJECT = [] # итоговые покупки в формате: цена покупки, дата покупки, объем, процент убыли/прибыли
    SELL = []  # тоже, что BUY_FOR_PROJECT только с продажами в формате: цена, дата, объем
    up = 0
    budget = 0
    for i in range(2, len(A)):
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
            if (A[i - 2][2] < A[i - 2][1]) and (A[i - 1][2] > A[i - 1][1]):  # черная свеча поглощена белой. Следовательно, сегодня покупаем
                d = int(1 + (max_b - min_b) / (max_a - min_a))
                BUY_FOR_PROJECT.append([A[i][1], A[i][0], d, 0])
                BUY.append([A[i][1], A[i][0], d, 0])  # цена покупки, дата покупки, объем, процент прибыли/убыли
                up -= A[i][1] * d
                budget += A[i][1] * d
            elif (A[i - 2][1] < A[i - 2][2]) and (A[i - 1][1] > A[i - 1][2]):  # белая свеча поглощена черной
                value_to_sell = 0
                for j in BUY:
                    if j[3] > 0:
                        up += A[i][1] * j[2]
                        value_to_sell += j[2]
                        BUY.remove(j)
                if value_to_sell != 0:
                    SELL.append([A[i][1], A[i][0], value_to_sell])  # цена продажи, дата продажи, объем
                if (i > 5) and (A[i - 5][2] > (A[i - 1][1] + A[i - 1][2]) / 2) and (abs(A[i - 1][1] - A[i - 1][2]) * 4 < A[i - 1][4] - A[i - 1][3]):
                    d = (A[i - 1][4] - A[i - 1][3]) / (abs(A[i - 1][1] - A[i - 1][2]))
                    BUY.append(A[i][1], A[i][0], d, 0) # молот
                    BUY_FOR_PROJECT.append([A[i][1], A[i][0], d, 0])
                    up -= A[i][1] * d
                    budget += A[i][1] * d
        print(A[i])
        print(A[i][3])
        # print("SELL")
        # print(*SELL, sep='\n')
        print("BUY")
        print(*BUY, sep='\n')
        # print("BUY_FOR_PROJECT")
        # print(*BUY_FOR_PROJECT, sep='\n')
        print()
    file.close()
    print("доход:", up) #вывод дохода
    print("бюджет:", budget) #вывод бюджета


if __name__ == '__main__':
    absorption(100)
