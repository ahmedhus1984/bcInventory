import functions

def main():
    a=''
    while True:
        a=functions.choiceSelectTables()
        if a=='x':
            print('\nbye!')
            return 0

main()



