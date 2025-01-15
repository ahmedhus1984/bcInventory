import mainLoop

if __name__=='__main__':
    a=''
    while True:
        a=mainLoop.choiceSelectTables()
        if a=='x':
            print('\nbye!')
            exit(1)