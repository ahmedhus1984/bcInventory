import mysql.connector

def mysqlConn():
    user=input('enter username: ')
    pwd=input('enter password: ')
    conn=mysql.connector.connect(host='66.96.216.133', user=user, passwd=pwd, db='bcinv')
    if not conn.is_connected():
        print('unable to connect to sql server.')
        exit(1)
    else:
        print('connection success!!!')
        myCursor=mysqlCursor(conn)
        return conn, myCursor

def mysqlCursor(conn):
    myCursor=conn.cursor(buffered=True)
    if not myCursor:
        print('unable to create cursor')
        mysqlConnClose(conn)
        exit(1)
    return myCursor

def mysqlCreateSystems(cursor, table):
    brand, model, serial, hostname, type, shipdate, warrexp, site, location, devdep, status=input('enter brand, model, serial, hostname, type, shipdate, warrexp, site, location, devdep, status seperated by comma:\n').split(',')
    print(brand+'\n'+model+'\n'+serial+'\n'+hostname+'\n'+type+'\n'+shipdate+'\n'+warrexp+'\n'+site+'\n'+location+'\n'+devdep+'\n'+status)
    cursor.execute(f'insert into {table} (brand, model, serial, hostname, type, shipdate, warrexp, site, location, devdep, status) values("{brand}", "{model}", "{serial}", "{hostname}", "{type}", "{shipdate}", "{warrexp}", "{site}", "{location}", "{devdep}", "{status}")')

def mysqlCreateHistLog(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')

def mysqlCreatePrevOwn(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')

def mysqlCreateCurrOwn(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')



def mysqlRead(cursor, table, readParam):
    cursor.execute(f'select * from {table} where hostname=\'{readParam}\'')
    blah=[]
    for i in cursor:
        for j in i:
            blah.append(j)
    blah2=readColumns(cursor, table)
    print()
    for i in range(0, len(blah), 1):
        print(f'{blah2[i]: <12}: {blah[i]}')
    print()

def mysqlDelete(cursor, table, delParam):
    cursor.execute(f'delete from {table} where hostname=\'{delParam}\'')



def readColumns(cursor, table):
    cursor.execute(f'desc {table}')
    blah=[]
    for i in cursor:
        blah.append(i[0])
    return blah

def mysqlConnClose(conn):
    conn.close()

def choiceSelectTables(conn, cursor):
    while True:
        table=input('enter option to view a table; s for systems, h for histlogs, p for prevown, c for currown or x to exit: ')
        match table:
            case 's':
                table='systems'
            case 'h':
                table='histlogs'
            case 'p':
                table='prevown'
            case 'c':
                table='currown'
            case 'x':
                return table
            case _:
                print('wrong choice, only s, h, p, c or x allowed. ')
        choiceSelectCrud(table, conn, cursor)

def choiceSelectCrud(table, conn, cursor):
    while True:
        operation=input('enter c (create), r (read), d (delete), rc(read columns), x (exit): ')
        match operation:
            case 'c':
                match table:
                    case 'systems':
                        mysqlCreateSystems(cursor, table)
                    case 'histlogs':
                        mysqlCreateHistLog(cursor, table)
                    case 'prevown':
                        mysqlCreatePrevOwn(cursor, table)
                    case 'currown':
                        mysqlCreateCurrOwn(cursor, table)
                conn.commit()
            case 'r': 
                readParam=input('enter hostname to read: ')
                mysqlRead(cursor, table, readParam)
            case 'd': 
                delParam=input('enter hostname to delete: ')
                mysqlDelete(cursor, table, delParam)
            case 'rc':
                blah=readColumns(cursor, table)
                print(blah)
            case 'x':
                return operation
            case _:
                print('wrong choice, only c, r, u, d or x is allowed.')

def main():
    conn, myCursor=mysqlConn()
    a=''
    while True:
        a=choiceSelectTables(conn, myCursor)
        if a=='x':
            print('bye!')
            mysqlConnClose(conn)
            return 0


main()