import csv
import os

file = open("../csv_files/YNDX.csv", encoding="utf8")


def compress_csv():
    reader = csv.reader(file, delimiter=";", quotechar='"')

    for line in reader:
        # print(str(*line))
        number, time_begin, open, close, high, low, value, volume, time_end = str(*line).split(',')
        if number:
            print(number, time_begin, open, close, high, low, value, volume, time_end, sep='\n')
    file.close()


compress_csv()
