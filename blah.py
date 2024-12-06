'''
    with open('haha.csv', 'w', newline='') as blah:
'''

import csv

with open('myfile.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')

    with open('haha.csv', 'w', newline='') as blah:
        csv_writer = csv.writer(blah, delimiter=',')

        for i in csv_reader:
            csv_writer.writerow(i)