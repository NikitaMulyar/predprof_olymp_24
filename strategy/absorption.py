import csv
import os

def absorption():
    file = open("../csv_files/YNDX.csv", encoding="utf8")
    reader = csv.reader(file, delimiter=";", quotechar='"')
    print(reader)
    A = [[] for i in range(101)]
    i = 0
    for line in reader:
        if i != 0:
            A[i] = str(*line).split(',')[1:] # распаковка и удаление номера вершины
            for j in range(len(A[i])):
                if j!=0 and j!=7: #перевод во float цен
                    A[i][j] = float(A[i][j])
        i+=1
    BUY = []
    print(A)
    BUY = []
    SELL = []
    for i in range(2, len(A)):
        print(A[i-1])
        min_a = min(A[i-1][3], A[i-1][4])
        max_a = max(A[i-1][3], A[i-1][4])
        min_b = min(A[i][3], A[i][4])
        max_b = max(A[i][3], A[i][4])
        print(min_a, max_a, min_b, max_b)
        absort = False
        if (min_b<min_a) and (max_b>max_a):
            absort = True
        if A[i][3] < A[i][4]:
            color = "white"
        else:
            color = "black"
        if absort:
            if (A[i-1][4] < A[i-1][3]) and (A[i][4] > A[i][3]):
                pass
    file.close()


if __name__ == '__main__':
    absorption()
