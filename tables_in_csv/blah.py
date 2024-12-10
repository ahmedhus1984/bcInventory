import csv

def csvToMysqlCommand(csvFile, table):
    with open(csvFile, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        with open('blah.txt', 'w') as file:
            print()
            for i in csv_reader:
                myLen=len(i)
                file.write(f'insert into {table} values(')
                for j in range(myLen):
                    if(j!=(myLen-1)):
                        file.write('\'' + i[j].strip() + '\'' + ',')
                    else:
                        file.write('\'' + i[j].strip() + '\'')
                file.write(');\n')


def main():
    csvFile=input('enter csv file name: ')
    table=input('enter table name: ')
    try:
        csvToMysqlCommand(csvFile, table)
    except:
        print('unable to open csv file, please check for file spelling error')


main()