import csv
import os

def absorption():
    file = open("../csv_files/YNDX.csv", encoding="utf8")
    reader = csv.reader(file, delimiter=";", quotechar='"')
    A = [[] for i in range(100)]
    i = 0
    for line in reader:
        if i != 0:
            A[i - 1] = str(*line).split(',')[1:] # распаковка и удаление номера вершины
            for j in range(len(A[i - 1])):
                if j!=0 and j!=7: #перевод во float цен
                    A[i - 1][j] = float(A[i - 1][j])
        i+=1
    BUY = [[]] # все цены, которые попадают в этот массив, отмечаются зеленой галочкой на графике
    SELL = [[]] # все цены, которые попадают в этот массив, отмечаются красным ротиком на графике
    for i in range(2, len(A)):
        for j in BUY: # для каждой купленной акции определяем, какой процент прибыли/убыли она несет к текущему дню
            j[3] = ((A[i - 1][3] + A[i - 1][4]) / 2) / j[0] * 100 - 100
            if(j[3] >= 5 or j[3] <= -5): SELL.append(A[i][1], A[i][0], j[2])# если прибыль/убыль больше 5%, продаем
        min_a = min(A[i - 2][1], A[i - 2][2])
        max_a = max(A[i - 2][1], A[i - 2][2])
        min_b = min(A[i - 1][1], A[i - 1][2])
        max_b = max(A[i - 1][1], A[i - 1][2])
        absort = False
        if (min_b < min_a) and (max_b > max_a): # проверка на то, что вчера произошло поглощение
            absort = True
        if absort:
            if (A[i - 2][2] < A[i - 2][1]) and (A[i - 1][2] > A[i - 1][1]): # черная свеча поглощена белой. Следовательно, сегодня покупаем
                BUY.append([A[i][3], A[i][0], 1, 0]) # цена покупки, дата покупки, объем, процент прибыли/убыли
            elif (A[i - 2][1] < A[i - 2][2]) and (A[i - 1][1] > A[i - 1][2]): # белая свеча поглощена черной
                value_to_sell = 0
                for j in BUY:
                    if(j[3] > 0) :
                        value_to_sell += j[2]
                        BUY.remove(j)
                SELL.append(A[i][3], A[i][0], value_to_sell) # цена продажи, дата продажи, объем
    file.close()
    print(SELL)

if __name__ == '__main__':
    absorption()